#!/usr/bin/env python3
"""Fix all job names with spaces in GitLab CI files"""

# Fix the self-hosted CI file
with open('.gitlab-ci-self-hosted.yml', 'r') as f:
    content = f.read()

# Fix all job names with spaces
content = content.replace('security: secrets:', 'security:secrets:')
content = content.replace('sync: github:', 'sync:github:')
content = content.replace('release: galaxy:', 'release:galaxy:')
content = content.replace('test: molecule:full:', 'test:molecule:full:')

with open('.gitlab-ci-self-hosted.yml', 'w') as f:
    f.write(content)

print("Fixed all job names in .gitlab-ci-self-hosted.yml")