#!/usr/bin/env python3
import glob

for meta_file in glob.glob("roles/*/meta/main.yml"):
    print(f"Fixing {meta_file}")
    with open(meta_file, 'r') as f:
        content = f.read()
    
    # Remove all trailing whitespace and blank lines
    content = content.rstrip()
    # Add exactly one newline at the end
    content += '\n'
    
    with open(meta_file, 'w') as f:
        f.write(content)

print("Fixed blank lines in all meta files")