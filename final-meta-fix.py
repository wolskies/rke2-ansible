#!/usr/bin/env python3
import glob
import re

def fix_meta_file_indentation(file_path):
    """Fix YAML indentation to satisfy yamllint expectations"""
    print(f"Fixing {file_path}")
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    for line in lines:
        # Fix platforms list indentation (should be 4 spaces from galaxy_info)
        if line.strip().startswith('platforms:'):
            fixed_lines.append('  platforms:\n')
        elif re.match(r'^  - name: ', line):
            # Platform items should be 4 spaces indented
            fixed_lines.append('    ' + line[2:])
        elif re.match(r'^    versions:', line):
            # Versions should be 6 spaces indented  
            fixed_lines.append('      versions:\n')
        elif re.match(r'^    - ', line) and any('versions:' in prev_line for prev_line in fixed_lines[-3:]):
            # Version items should be 8 spaces indented
            fixed_lines.append('        ' + line[4:])
        elif line.strip().startswith('galaxy_tags:'):
            fixed_lines.append('  galaxy_tags:\n')
        elif re.match(r'^  - ', line) and any('galaxy_tags:' in prev_line for prev_line in fixed_lines[-3:]):
            # Galaxy tag items should be 4 spaces indented
            fixed_lines.append('    ' + line[2:])
        else:
            fixed_lines.append(line)
    
    with open(file_path, 'w') as f:
        f.writelines(fixed_lines)

# Process all meta files
meta_files = glob.glob("roles/*/meta/main.yml")
for meta_file in meta_files:
    fix_meta_file_indentation(meta_file)

print("Fixed all meta file indentation to satisfy yamllint")