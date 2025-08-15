# Comprehensive YAML Lint Fixer

## Overview

The `comprehensive-lint-fix.py` script automatically fixes common YAML formatting issues in Ansible collections based on yamllint and ansible-lint standards.

## Features

- **Removes trailing spaces**: Cleans up whitespace at the end of lines
- **Adds missing newlines at EOF**: Ensures all files end with exactly one newline
- **Fixes indentation issues**: Converts tabs to spaces and ensures consistent 2-space indentation
- **Adds document start markers**: Adds `---` at the beginning of YAML files where missing
- **Fixes comment formatting**: Ensures proper spacing around `#` in comments
- **Fixes YAML structure issues**: Corrects spacing after colons and hyphens in YAML structures
- **Safe operation**: Creates backups by default and validates YAML syntax
- **Dry-run mode**: Preview changes without modifying files

## Installation Requirements

The script requires Python 3.6+ and the PyYAML library:

```bash
pip install PyYAML
```

## Usage

### Basic Usage

```bash
# Preview changes without modifying files (recommended first step)
python3 comprehensive-lint-fix.py --dry-run

# Apply fixes with backup files
python3 comprehensive-lint-fix.py

# Apply fixes without creating backups (not recommended)
python3 comprehensive-lint-fix.py --no-backup
```

### Advanced Usage

```bash
# Process a specific directory
python3 comprehensive-lint-fix.py /path/to/ansible/collection --dry-run

# Use custom backup suffix
python3 comprehensive-lint-fix.py --backup-suffix .bak

# Enable verbose logging
python3 comprehensive-lint-fix.py --verbose
```

### Command Line Options

- `--dry-run`: Show what would be changed without modifying files
- `--backup-suffix SUFFIX`: Custom suffix for backup files (default: `.backup`)
- `--no-backup`: Don't create backup files
- `--verbose`: Enable verbose logging
- `--help`: Show help message and usage examples

## What Gets Fixed

### 1. Trailing Spaces
```yaml
# Before
key: value    
list:
  - item1    
  - item2  

# After
key: value
list:
  - item1
  - item2
```

### 2. Missing Newlines at EOF
Files that don't end with a newline character will have one added.

### 3. Document Start Markers
```yaml
# Before
key: value
list:
  - item1

# After
---
key: value
list:
  - item1
```

### 4. Comment Formatting
```yaml
# Before
key: value#comment
another_key: value  #  comment with extra spaces

# After
key: value # comment
another_key: value # comment with extra spaces
```

### 5. Indentation Issues
```yaml
# Before (using tabs or inconsistent spacing)
key:
	value: something
  another: thing

# After
key:
  value: something
  another: thing
```

### 6. YAML Structure
```yaml
# Before
key:value
list:
  -item1
  -item2

# After
key: value
list:
  - item1
  - item2
```

## Files Processed

The script recursively processes all `.yml` and `.yaml` files while excluding:

- `.cache/`, `.git/`, `.gitlab-ci/`, `.tox/`, `.venv/`
- `molecule/`, `.vagrant/`, `.ansible/`
- `.pytest_cache/`, `__pycache__/`, `.mypy_cache/`
- `tests/output/`, `changelogs/fragments/`
- `*.tar.gz`, `*.pyc`, `*.pyo` files

## Safety Features

1. **Backups**: Original files are backed up before modification (unless `--no-backup` is used)
2. **YAML Validation**: Fixed content is validated to ensure it's still valid YAML
3. **Dry Run Mode**: Preview changes before applying them
4. **Careful Processing**: Skips lines with YAML anchors, references, and complex structures
5. **Error Handling**: Graceful handling of files with advanced YAML features

## Output

The script provides a detailed summary showing:
- Number of files processed and changed
- Breakdown of changes by type
- Specific files and change counts
- Recommended next steps

## Example Output

```
============================================================
YAML LINT FIX SUMMARY
============================================================
Files processed: 96
Files changed: 89
Mode: DRY RUN

Changes by type:
----------------------------------------

Trailing spaces removed: 12 changes in 8 files
Missing newlines at EOF added: 74 changes in 74 files
Document start markers (---) added: 3 changes in 3 files
Comment spacing fixed: 60 changes in 45 files
Indentation issues fixed: 2 changes in 2 files
YAML structure issues fixed: 15 changes in 12 files

============================================================

Recommended next steps:
1. Review the changes made by examining a few modified files
2. Run yamllint and ansible-lint to verify improvements
3. Test your Ansible playbooks to ensure functionality is preserved
4. Commit the formatting improvements to version control
```

## Workflow Recommendations

1. **Before running**: Commit your current changes to version control
2. **Dry run first**: Always use `--dry-run` to preview changes
3. **Review changes**: Examine a few files to ensure the fixes look correct
4. **Run linters**: Execute `yamllint` and `ansible-lint` to verify improvements
5. **Test functionality**: Run your Ansible playbooks to ensure they still work
6. **Commit changes**: Add the formatting improvements to version control

## Backup Management

If you used the default backup behavior, you can:

```bash
# List all backup files
find . -name "*.backup"

# Remove all backup files after verifying changes
find . -name "*.backup" -delete

# Restore a specific file from backup
cp path/to/file.yml.backup path/to/file.yml
```

## Troubleshooting

### YAML Validation Warnings

Some files (like GitLab CI configurations) may use advanced YAML features that trigger validation warnings. These warnings are generally safe to ignore if the files work correctly with their intended tools.

### Large Collections

For very large collections, consider processing subdirectories separately:

```bash
python3 comprehensive-lint-fix.py roles/ --dry-run
python3 comprehensive-lint-fix.py playbooks/ --dry-run
python3 comprehensive-lint-fix.py tests/ --dry-run
```

### Performance

The script is designed to be reasonably fast, but processing many files may take some time. Use `--verbose` to monitor progress on large collections.

## License

GPL-3.0-or-later (same as the parent Ansible collection)