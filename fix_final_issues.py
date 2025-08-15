#!/usr/bin/env python3
"""Fix the final remaining linting issues"""

# Fix trailing spaces in GitLab CI
with open('.gitlab-ci.yml', 'r') as f:
    content = f.read()

# Remove trailing spaces from all lines
lines = content.splitlines()
fixed_lines = [line.rstrip() for line in lines]
content = '\n'.join(fixed_lines) + '\n'

with open('.gitlab-ci.yml', 'w') as f:
    f.write(content)

print("Fixed trailing spaces in .gitlab-ci.yml")

# Fix the syntax error in self-hosted CI
with open('.gitlab-ci-self-hosted.yml', 'r') as f:
    content = f.read()

# Find and fix any remaining job naming issues
content = content.replace('lint: ansible:', 'lint:ansible:')
content = content.replace('lint: yaml:', 'lint:yaml:')

with open('.gitlab-ci-self-hosted.yml', 'w') as f:
    f.write(content)

print("Fixed syntax issues in .gitlab-ci-self-hosted.yml")

# Fix GitHub workflow line length
with open('.github/workflows/tests-sync.yml', 'r') as f:
    lines = f.readlines()

# Find and fix the long line around line 165
for i, line in enumerate(lines):
    if len(line.strip()) > 120 and 'uses:' in line or 'with:' in line:
        # Split long lines appropriately
        if 'uses: actions/' in line:
            parts = line.split('uses: ')
            if len(parts) == 2:
                indent = len(parts[0])
                lines[i] = parts[0] + 'uses: >\n' + ' ' * (indent + 2) + parts[1]

with open('.github/workflows/tests-sync.yml', 'w') as f:
    f.writelines(lines)

print("Fixed line length in GitHub workflow")
print("All issues fixed!")