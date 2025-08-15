#!/usr/bin/env python3
"""
Fix all meta/main.yml files to satisfy yamllint and ansible-lint requirements
"""
import yaml
import glob
import os
from pathlib import Path

def fix_meta_file(file_path):
    """Fix a single meta/main.yml file"""
    print(f"Processing {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    try:
        # Parse YAML
        data = yaml.safe_load(content)
        
        # Apply user-requested platform changes
        if 'galaxy_info' in data and 'platforms' in data['galaxy_info']:
            for platform in data['galaxy_info']['platforms']:
                # Change RedHat to EL as requested by user
                if platform.get('name') == 'RedHat':
                    platform['name'] = 'EL'
                    platform['versions'] = ['all']
                # Change Rocky versions to 'all' as requested
                elif platform.get('name') == 'Rocky':
                    platform['versions'] = ['all']
                # Change Oracle versions to 'all' as requested  
                elif platform.get('name') == 'Oracle':
                    platform['versions'] = ['all']
        
        # Write back with proper YAML formatting
        with open(file_path, 'w') as f:
            # Write header
            f.write("# SPDX-License-Identifier: GPL-3.0-or-later\n---\n")
            
            # Write galaxy_info section with proper indentation
            f.write("galaxy_info:\n")
            galaxy_info = data['galaxy_info']
            
            for key, value in galaxy_info.items():
                if key == 'platforms':
                    f.write("  platforms:\n")
                    for platform in value:
                        f.write(f"    - name: {platform['name']}\n")
                        f.write("      versions:\n")
                        for version in platform['versions']:
                            f.write(f"        - {version}\n")
                elif key == 'galaxy_tags':
                    f.write("  galaxy_tags:\n")
                    for tag in value:
                        f.write(f"    - {tag}\n")
                elif isinstance(value, str):
                    # Handle multi-line descriptions
                    if '\n' in value or len(value) > 80:
                        f.write(f"  {key}: >\n")
                        lines = value.strip().split('\n')
                        for line in lines:
                            f.write(f"    {line.strip()}\n")
                    else:
                        f.write(f"  {key}: {value}\n")
                else:
                    f.write(f"  {key}: {value}\n")
            
            # Write dependencies section
            if 'dependencies' in data:
                f.write("dependencies:")
                if not data['dependencies']:
                    f.write(" []\n")
                else:
                    f.write("\n")
                    for dep in data['dependencies']:
                        if isinstance(dep, dict):
                            f.write(f"- role: {dep.get('role', '')}\n")
                            if 'when' in dep:
                                f.write(f"  when: {dep['when']}\n")
                        else:
                            f.write(f"- {dep}\n")
            
            # Ensure file ends with newline
            f.write("\n")
            
    except yaml.YAMLError as e:
        print(f"Error processing {file_path}: {e}")
        return False
    
    return True

def main():
    """Process all meta/main.yml files"""
    meta_files = glob.glob("roles/*/meta/main.yml")
    
    if not meta_files:
        print("No meta files found!")
        return
    
    success_count = 0
    for meta_file in meta_files:
        if fix_meta_file(meta_file):
            success_count += 1
    
    print(f"Successfully processed {success_count}/{len(meta_files)} meta files")

if __name__ == "__main__":
    main()