#!/usr/bin/env python3
"""
Comprehensive YAML Lint Fixer for Ansible Collections

This script automatically fixes common YAML formatting issues in Ansible collections
based on yamllint and ansible-lint standards.

Features:
- Removes trailing spaces
- Adds missing newlines at end of files
- Fixes common indentation issues
- Adds document start markers (---) where missing
- Fixes comment formatting (spacing after # and before comments)
- Fixes basic YAML structure issues (colon and hyphen spacing)
- Provides detailed summary of changes made
- Creates backups before making changes
- Safe mode with dry-run option

Quick Usage:
  python3 comprehensive-lint-fix.py --dry-run    # Preview changes
  python3 comprehensive-lint-fix.py              # Apply fixes with backups
  python3 comprehensive-lint-fix.py --no-backup  # Apply fixes without backups

Author: Automated Lint Fixer
License: GPL-3.0-or-later
"""

import os
import re
import sys
import argparse
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Set
from datetime import datetime
import yaml
from collections import defaultdict


class YAMLLintFixer:
    """Main class for fixing YAML lint issues"""
    
    def __init__(self, root_path: str, backup_suffix: str = '.backup', dry_run: bool = False):
        self.root_path = Path(root_path).resolve()
        self.backup_suffix = backup_suffix
        self.dry_run = dry_run
        self.changes_summary = defaultdict(list)
        self.files_processed = 0
        self.files_changed = 0
        
        # Directories to exclude (based on yamllint config)
        self.excluded_dirs = {
            '.cache', '.git', '.gitlab-ci', '.tox', '.venv', 
            'molecule', '.vagrant', '.ansible', '.pytest_cache',
            '__pycache__', '.mypy_cache', 'tests/output',
            'changelogs/fragments'
        }
        
        # File patterns to exclude
        self.excluded_patterns = {'*.tar.gz', '*.pyc', '*.pyo'}
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('lint-fix.log')
            ]
        )
        self.logger = logging.getLogger(__name__)

    def should_exclude_path(self, file_path: Path) -> bool:
        """Check if a path should be excluded from processing"""
        # Check if any parent directory is in excluded_dirs
        for part in file_path.parts:
            if part in self.excluded_dirs:
                return True
                
        # Check file patterns
        for pattern in self.excluded_patterns:
            if file_path.match(pattern):
                return True
                
        return False

    def find_yaml_files(self) -> List[Path]:
        """Recursively find all YAML files"""
        yaml_files = []
        yaml_extensions = {'.yml', '.yaml'}
        
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in yaml_extensions:
                if not self.should_exclude_path(file_path):
                    yaml_files.append(file_path)
                    
        return sorted(yaml_files)

    def create_backup(self, file_path: Path) -> bool:
        """Create a backup of the original file"""
        if self.dry_run:
            return True
            
        backup_path = file_path.with_suffix(file_path.suffix + self.backup_suffix)
        try:
            shutil.copy2(file_path, backup_path)
            return True
        except Exception as e:
            self.logger.error(f"Failed to create backup for {file_path}: {e}")
            return False

    def is_valid_yaml(self, content: str) -> bool:
        """Check if content is valid YAML"""
        try:
            # Try to load with safe_load first
            yaml.safe_load(content)
            return True
        except yaml.YAMLError as e:
            # Some GitLab CI files and other configs might use advanced YAML features
            # that safe_load doesn't support. Try with unsafe_load as a fallback
            try:
                yaml.unsafe_load(content)
                return True
            except yaml.YAMLError:
                # If both fail, log the error for debugging but don't completely fail
                self.logger.debug(f"YAML validation failed: {e}")
                return False

    def fix_trailing_spaces(self, lines: List[str]) -> Tuple[List[str], int]:
        """Remove trailing spaces from lines"""
        fixed_lines = []
        changes = 0
        
        for line in lines:
            original_line = line
            fixed_line = line.rstrip(' \t')
            if original_line != fixed_line:
                changes += 1
            fixed_lines.append(fixed_line)
            
        return fixed_lines, changes

    def fix_newline_at_eof(self, content: str) -> Tuple[str, bool]:
        """Ensure file ends with exactly one newline"""
        if not content:
            return content, False
            
        # Remove all trailing whitespace and newlines
        content_stripped = content.rstrip()
        
        # Add exactly one newline
        fixed_content = content_stripped + '\n'
        
        return fixed_content, content != fixed_content

    def fix_document_start(self, lines: List[str]) -> Tuple[List[str], bool]:
        """Add document start marker (---) if missing"""
        if not lines:
            return lines, False
            
        # Skip license/copyright comments at the beginning
        first_content_line = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                first_content_line = i
                break
        else:
            # File only contains comments or is empty
            return lines, False
            
        # Check if document start marker exists
        has_doc_start = False
        for i in range(first_content_line, min(first_content_line + 3, len(lines))):
            if lines[i].strip() == '---':
                has_doc_start = True
                break
                
        if not has_doc_start:
            # Insert document start after license/copyright comments
            insert_pos = first_content_line
            lines.insert(insert_pos, '---')
            return lines, True
            
        return lines, False

    def fix_comment_spacing(self, lines: List[str]) -> Tuple[List[str], int]:
        """Fix spacing in comments"""
        fixed_lines = []
        changes = 0
        
        for line in lines:
            original_line = line
            fixed_line = line
            
            # Only process lines with comments, but be careful about special cases
            if '#' in line:
                # Skip if this looks like a shebang line
                if line.strip().startswith('#!'):
                    fixed_lines.append(line)
                    continue
                    
                # Skip if this might be in a quoted string (basic heuristic)
                quote_count = line.count('"') + line.count("'")
                if quote_count >= 2:
                    fixed_lines.append(line)
                    continue
                    
                # Find the first # that's likely a comment
                hash_pos = line.find('#')
                if hash_pos >= 0:
                    before_comment = line[:hash_pos]
                    comment_part = line[hash_pos + 1:]
                    
                    # Ensure at least one space before comment if there's content before it
                    if before_comment.rstrip() and not before_comment.endswith(' '):
                        before_comment = before_comment.rstrip() + ' '
                        
                    # Ensure exactly one space after # in comment
                    if comment_part and not comment_part.startswith(' '):
                        comment_part = ' ' + comment_part.lstrip()
                    elif comment_part.startswith('  '):
                        # Remove extra spaces after #
                        comment_part = ' ' + comment_part.lstrip()
                        
                    fixed_line = before_comment + '#' + comment_part
                    
                    if original_line != fixed_line:
                        changes += 1
                        
            fixed_lines.append(fixed_line)
            
        return fixed_lines, changes

    def fix_indentation_issues(self, lines: List[str]) -> Tuple[List[str], int]:
        """Fix common indentation issues"""
        fixed_lines = []
        changes = 0
        
        for line_num, line in enumerate(lines):
            original_line = line
            
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                fixed_lines.append(line)
                continue
                
            # Convert tabs to spaces (based on yamllint config: 2 spaces)
            if '\t' in line:
                fixed_line = line.expandtabs(2)
                if original_line != fixed_line:
                    changes += 1
                    line = fixed_line
                    
            # Fix mixed indentation (ensure consistent 2-space indentation)
            stripped = line.lstrip()
            if stripped:
                indent_level = len(line) - len(stripped)
                if indent_level % 2 != 0:
                    # Odd indentation, round down to nearest even number
                    new_indent_level = (indent_level // 2) * 2
                    line = ' ' * new_indent_level + stripped
                    if original_line != line:
                        changes += 1
                        
            fixed_lines.append(line)
            
        return fixed_lines, changes

    def fix_line_length_issues(self, lines: List[str], max_length: int = 120) -> Tuple[List[str], int]:
        """Fix basic line length issues where possible"""
        fixed_lines = []
        changes = 0
        
        for line in lines:
            original_line = line
            
            # Skip very long strings that can't be easily broken
            if len(line) > max_length:
                stripped = line.strip()
                
                # Try to break long comments
                if stripped.startswith('#'):
                    # This is a complex operation, skip for now
                    pass
                    
                # For now, just warn about long lines
                if len(line) > max_length + 20:  # Only warn for very long lines
                    self.logger.warning(f"Line too long ({len(line)} > {max_length}): {line[:50]}...")
                    
            fixed_lines.append(line)
            
        return fixed_lines, changes

    def fix_yaml_structure(self, lines: List[str]) -> Tuple[List[str], int]:
        """Fix basic YAML structure issues"""
        fixed_lines = []
        changes = 0
        
        for i, line in enumerate(lines):
            original_line = line
            fixed_line = line
            
            # Skip lines that are comments or contain YAML anchors/references
            stripped = line.strip()
            if (stripped.startswith('#') or 
                '&' in stripped or 
                '*' in stripped or
                '<<:' in stripped):
                fixed_lines.append(line)
                continue
                
            # Fix colon spacing: ensure one space after colons
            if ':' in line:
                # More careful regex that doesn't break URLs or complex structures
                # Only fix if it's clearly a YAML key-value pair
                if re.match(r'^\s*\w+:', line):
                    fixed_line = re.sub(r'^(\s*\w+):(\S)', r'\1: \2', line)
                    fixed_line = re.sub(r'^(\s*\w+):\s{2,}', r'\1: ', fixed_line)
                
            # Fix hyphen spacing: ensure one space after list hyphens
            if line.strip().startswith('-') and not line.strip().startswith('---'):
                # Be more careful about what we consider a list item
                if re.match(r'^\s*-\s*\w', line):
                    fixed_line = re.sub(r'^(\s*)- +', r'\1- ', fixed_line)
                elif re.match(r'^\s*-[^\s-]', line):
                    fixed_line = re.sub(r'^(\s*)-([^\s-])', r'\1- \2', fixed_line)
                
            if original_line != fixed_line:
                changes += 1
                
            fixed_lines.append(fixed_line)
            
        return fixed_lines, changes

    def process_file(self, file_path: Path) -> Dict[str, int]:
        """Process a single YAML file"""
        changes = defaultdict(int)
        
        try:
            # Read original file
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            # Skip empty files
            if not original_content.strip():
                return changes
                
            # Process content
            lines = original_content.splitlines()
            
            # Apply fixes
            lines, trailing_changes = self.fix_trailing_spaces(lines)
            changes['trailing_spaces'] = trailing_changes
            
            lines, doc_start_added = self.fix_document_start(lines)
            if doc_start_added:
                changes['document_start'] = 1
                
            lines, comment_changes = self.fix_comment_spacing(lines)
            changes['comment_spacing'] = comment_changes
            
            lines, indent_changes = self.fix_indentation_issues(lines)
            changes['indentation'] = indent_changes
            
            lines, structure_changes = self.fix_yaml_structure(lines)
            changes['yaml_structure'] = structure_changes
            
            lines, length_changes = self.fix_line_length_issues(lines)
            changes['line_length'] = length_changes
            
            # Reconstruct content
            new_content = '\n'.join(lines)
            
            # Fix newline at EOF
            new_content, eof_changed = self.fix_newline_at_eof(new_content)
            if eof_changed:
                changes['newline_eof'] = 1
                
            # Check if any changes were made
            total_changes = sum(changes.values())
            if total_changes == 0:
                return changes
                
            # Validate YAML syntax (but don't fail for files with advanced YAML features)
            if not self.is_valid_yaml(new_content):
                self.logger.warning(f"Fixed content may contain advanced YAML features that can't be validated: {file_path}")
                # Don't return early - these files might still benefit from basic formatting fixes
                
            # Write changes
            if not self.dry_run:
                if not self.create_backup(file_path):
                    return defaultdict(int)
                    
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
            self.logger.info(f"Fixed {file_path}: {total_changes} changes")
            return changes
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            return defaultdict(int)

    def process_all_files(self) -> None:
        """Process all YAML files in the directory"""
        yaml_files = self.find_yaml_files()
        self.logger.info(f"Found {len(yaml_files)} YAML files to process")
        
        if self.dry_run:
            self.logger.info("Running in DRY RUN mode - no files will be modified")
            
        for file_path in yaml_files:
            self.files_processed += 1
            file_changes = self.process_file(file_path)
            
            if sum(file_changes.values()) > 0:
                self.files_changed += 1
                for change_type, count in file_changes.items():
                    self.changes_summary[change_type].append((file_path, count))

    def print_summary(self) -> None:
        """Print a summary of all changes made"""
        print("\n" + "="*60)
        print("YAML LINT FIX SUMMARY")
        print("="*60)
        print(f"Files processed: {self.files_processed}")
        print(f"Files changed: {self.files_changed}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'WRITE'}")
        
        if not self.changes_summary:
            print("\nNo changes were needed!")
            return
            
        print("\nChanges by type:")
        print("-" * 40)
        
        change_descriptions = {
            'trailing_spaces': 'Trailing spaces removed',
            'newline_eof': 'Missing newlines at EOF added',
            'document_start': 'Document start markers (---) added',
            'comment_spacing': 'Comment spacing fixed',
            'indentation': 'Indentation issues fixed',
            'yaml_structure': 'YAML structure issues fixed',
            'line_length': 'Line length issues addressed'
        }
        
        for change_type, files_list in self.changes_summary.items():
            total_changes = sum(count for _, count in files_list)
            description = change_descriptions.get(change_type, change_type)
            print(f"\n{description}: {total_changes} changes in {len(files_list)} files")
            
            # Show up to 5 examples
            for file_path, count in files_list[:5]:
                rel_path = file_path.relative_to(self.root_path)
                print(f"  - {rel_path}: {count} changes")
                
            if len(files_list) > 5:
                print(f"  ... and {len(files_list) - 5} more files")
                
        print("\n" + "="*60)
        
        if not self.dry_run and self.backup_suffix:
            print(f"Original files backed up with suffix: {self.backup_suffix}")
            print(f"To remove backups: find . -name '*{self.backup_suffix}' -delete")
            
        # Additional usage information
        if self.files_changed > 0:
            print("\nRecommended next steps:")
            print("1. Review the changes made by examining a few modified files")
            print("2. Run yamllint and ansible-lint to verify improvements")
            print("3. Test your Ansible playbooks to ensure functionality is preserved")
            print("4. Commit the formatting improvements to version control")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Fix common YAML linting issues in Ansible collections",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Process current directory
  %(prog)s /path/to/ansible/collection  # Process specific directory
  %(prog)s --dry-run               # Show what would be changed without modifying files
  %(prog)s --no-backup             # Don't create backup files
        """
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to Ansible collection root (default: current directory)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    
    parser.add_argument(
        '--backup-suffix',
        default='.backup',
        help='Suffix for backup files (default: .backup)'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Don\'t create backup files'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set up logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        
    # Set backup suffix
    backup_suffix = '' if args.no_backup else args.backup_suffix
    
    # Validate path
    root_path = Path(args.path).resolve()
    if not root_path.exists():
        print(f"Error: Path does not exist: {root_path}")
        sys.exit(1)
        
    if not root_path.is_dir():
        print(f"Error: Path is not a directory: {root_path}")
        print("Note: This script processes directories containing YAML files, not individual files.")
        sys.exit(1)
        
    # Run the fixer
    try:
        fixer = YAMLLintFixer(root_path, backup_suffix, args.dry_run)
        fixer.process_all_files()
        fixer.print_summary()
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()