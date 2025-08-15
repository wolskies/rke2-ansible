# CI/CD Pipeline Documentation

This document explains the dual CI/CD setup for the RKE2 Ansible Collection.

## 🏗️ Architecture Overview

```
GitLab Self-Hosted (Primary)     GitHub (Sync)
├── Full test suite              ├── Community validation
├── Security scanning            ├── Fast feedback 
├── Molecule tests               ├── Collection verification
├── Deployment tests             └── Release automation
└── Manual Galaxy publish       
```

## 🔄 Repository Sync Setup

- **Primary**: GitLab self-hosted (development & full CI)
- **Secondary**: GitHub (community & releases)
- **Sync**: Automatic via GitLab CI job

## 🚀 GitLab CI Pipeline (Primary)

### **Configuration Files:**
- `.gitlab-ci.yml` - Original comprehensive pipeline
- `.gitlab-ci-self-hosted.yml` - Optimized for self-hosted runners

### **Pipeline Stages:**

#### **1. Lint Stage**
```yaml
# Fast parallel linting
- YAML validation (yamllint)
- Ansible best practices (ansible-lint) 
- Syntax checking (all roles)
```

#### **2. Unit Test Stage**
```yaml
# Quick validation tests
- Python unit tests
- Role syntax validation
- Collection build test
```

#### **3. Integration Test Stage** (Manual)
```yaml
# Resource-intensive tests
- Molecule testing (Docker)
- Multi-role integration
- Full deployment simulation
```

#### **4. Security Scan Stage**
```yaml
# Security validation
- Secret scanning (TruffleHog)
- Ansible content scanning
- Dependency vulnerability checks
```

#### **5. Sync Stage** (Manual)
```yaml
# Repository synchronization  
- Push to GitHub
- Tag synchronization
- Force-with-lease safety
```

#### **6. Deploy Stage** (Manual)
```yaml
# Release automation
- Ansible Galaxy publishing
- Version tagging
- Artifact management
```

## 📋 GitHub Actions (Secondary)

### **Workflows:**

#### **1. `tests-sync.yml` - Main Validation**
```yaml
# Fast validation for synced content
- Pre-flight checks (lint, syntax, unit tests)
- Collection build & verification
- Community compliance tests
- Results summary with status
```

#### **2. `tests.yml` - Community Standard**
```yaml
# Official Ansible community workflows
- ansible-content-actions integration
- Standard Galaxy compatibility
- Community best practices validation
```

#### **3. `release.yml` - Release Automation**
```yaml
# Automated releases from GitHub
- Triggered on GitHub releases
- Galaxy publishing
- Community distribution
```

#### **4. `sync-status.yml` - User Communication**
```yaml
# Auto-documentation for contributors
- Adds sync notices to PRs/Issues
- Explains dual-CI setup
- Guides contribution process
```

## ⚡ Self-Hosted Optimizations

### **GitLab Runner Configuration:**
```yaml
# Performance optimizations
tags: [docker, linux, self-hosted]
cache: 
  - UV package cache
  - Virtual environments
  - Molecule cache
variables:
  FF_USE_FASTZIP: "true"
  CACHE_COMPRESSION_LEVEL: "fast"
```

### **Package Management:**
- **UV**: Fast Python package installation
- **Shared caches**: Reduced download times
- **Incremental builds**: Cache virtual environments

## 🔧 Configuration Variables

### **GitLab CI Variables (Required):**
```yaml
GALAXY_API_KEY: "your-ansible-galaxy-api-key"
GITHUB_DEPLOY_KEY: "ssh-private-key-for-github-push"
```

### **GitHub Secrets (Required):**
```yaml
ANSIBLE_GALAXY_API_KEY: "your-ansible-galaxy-api-key"
```

## 📊 Pipeline Triggers

### **GitLab CI:**
- **Merge Requests**: Full validation pipeline
- **Main Branch**: Full pipeline + security scans
- **Tags**: Release pipeline
- **Manual**: Molecule tests, sync, deployment

### **GitHub Actions:**
- **Pull Requests**: Fast validation
- **Main Branch**: Validation + community tests
- **Releases**: Galaxy publishing
- **Issues/PRs**: Auto-documentation

## 🐛 Troubleshooting

### **Common Issues:**

#### **GitLab CI:**
```bash
# Runner connectivity
gitlab-runner verify

# Docker-in-Docker issues
docker info

# Cache issues
gitlab-runner exec docker --cache-dir /cache
```

#### **GitHub Actions:**
```bash
# Workflow debugging
gh run list
gh run view <run-id>

# Secret verification
gh secret list
```

### **Performance Tuning:**

#### **Self-Hosted Runners:**
```yaml
# .gitlab-ci-self-hosted.yml optimizations
- Use local Docker registry mirror
- Increase runner concurrent jobs
- Optimize cache retention policies
```

## 📈 Monitoring

### **Pipeline Health:**
- **GitLab**: Pipeline success rates, duration trends
- **GitHub**: Action completion rates, community compliance
- **Artifacts**: Collection build success, security scan results

### **Sync Health:**
- **Manual verification**: Compare commit hashes
- **Automated checks**: GitLab sync job status
- **Community feedback**: GitHub PR/Issue activity

## 🔄 Workflow Examples

### **Development Workflow:**
1. **Development**: Work in GitLab (primary)
2. **Testing**: GitLab CI validates changes
3. **Review**: GitLab merge request process
4. **Sync**: Manual trigger to push to GitHub
5. **Community**: GitHub provides public visibility

### **Release Workflow:**
1. **Tag**: Create release tag in GitLab
2. **Build**: GitLab CI builds collection
3. **Test**: Full validation pipeline
4. **Publish**: Manual Galaxy publish from GitLab
5. **Sync**: Push tag to GitHub
6. **Distribute**: GitHub release for community

This dual-CI setup provides robust testing with self-hosted control while maintaining community engagement through GitHub.