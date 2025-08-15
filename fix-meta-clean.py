#!/usr/bin/env python3
"""
Apply user-requested platform changes and fix formatting for all meta files
"""
import yaml
import glob
import os

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
                # Update Ubuntu versions to use codenames instead of numbers
                elif platform.get('name') == 'Ubuntu':
                    # Map version numbers to codenames
                    version_map = {
                        '24.04': 'noble',
                        '22.04': 'jammy', 
                        '20.04': 'focal'
                    }
                    new_versions = []
                    for version in platform.get('versions', []):
                        if version in version_map:
                            new_versions.append(version_map[version])
                        else:
                            new_versions.append(version)
                    platform['versions'] = new_versions
                # Update Debian versions to use codenames
                elif platform.get('name') == 'Debian':
                    version_map = {
                        '13': 'trixie',
                        '12': 'bookworm',
                        '11': 'bullseye'
                    }
                    new_versions = []
                    for version in platform.get('versions', []):
                        if version in version_map:
                            new_versions.append(version_map[version])
                        else:
                            new_versions.append(version)
                    platform['versions'] = new_versions
        
        # Write back with proper YAML formatting
        with open(file_path, 'w') as f:
            # Write header
            f.write("# SPDX-License-Identifier: GPL-3.0-or-later\n---\n")
            
            # Write galaxy_info section with proper indentation
            f.write("galaxy_info:\n")
            galaxy_info = data['galaxy_info']
            
            # Write basic info fields
            for key in ['role_name', 'author', 'description', 'company', 'license', 'min_ansible_version']:
                if key in galaxy_info:
                    value = galaxy_info[key]
                    if isinstance(value, str) and ('\n' in value or len(value) > 80):
                        # Handle multi-line descriptions
                        f.write(f"  {key}: >\n")
                        lines = value.strip().split('\n')
                        for line in lines:
                            f.write(f"    {line.strip()}\n")
                    else:
                        f.write(f"  {key}: {value}\n")
            
            f.write("\n")  # Add blank line before platforms
            
            # Write platforms section
            if 'platforms' in galaxy_info:
                f.write("  platforms:\n")
                for platform in galaxy_info['platforms']:
                    f.write(f"    - name: {platform['name']}\n")
                    f.write("      versions:\n")
                    for version in platform['versions']:
                        f.write(f"        - {version}\n")
            
            f.write("\n")  # Add blank line before galaxy_tags
            
            # Write galaxy_tags section
            if 'galaxy_tags' in galaxy_info:
                f.write("  galaxy_tags:\n")
                for tag in galaxy_info['galaxy_tags']:
                    f.write(f"    - {tag}\n")
            
            f.write("\n")  # Add blank line before dependencies
            
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