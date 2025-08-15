#!/usr/bin/env python3
import yaml
import glob
import os

def fix_meta_file(file_path):
    """Fix indentation in meta/main.yml files"""
    print(f"Processing {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Parse and rewrite YAML to ensure proper indentation
    try:
        data = yaml.safe_load(content)
        
        # Update platforms to use EL instead of RedHat as requested
        if 'galaxy_info' in data and 'platforms' in data['galaxy_info']:
            for platform in data['galaxy_info']['platforms']:
                if platform.get('name') == 'RedHat':
                    platform['name'] = 'EL'
                    platform['versions'] = ['all']
                elif platform.get('name') == 'Rocky':
                    platform['versions'] = ['all']
                elif platform.get('name') == 'Oracle':
                    platform['versions'] = ['all']
        
        # Write back with proper indentation
        with open(file_path, 'w') as f:
            f.write("# SPDX-License-Identifier: GPL-3.0-or-later\n")
            f.write("---\n")
            yaml.dump(data, f, default_flow_style=False, indent=2, sort_keys=False)
            
    except yaml.YAMLError as e:
        print(f"Error processing {file_path}: {e}")

# Process all meta files
meta_files = glob.glob("roles/*/meta/main.yml")
for meta_file in meta_files:
    fix_meta_file(meta_file)

print("Fixed indentation in all meta files")