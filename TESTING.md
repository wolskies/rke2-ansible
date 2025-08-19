# SPDX-License-Identifier: GPL-3.0-or-later

# Testing Guide for RKE2 Ansible Collection

This document provides comprehensive guidance for testing the `wolskinet.rke2_ansible` collection both locally and in CI/CD environments.

## Quick Setup

### Method 1: UV (Recommended)

The collection includes a complete testing framework that can be set up using UV (the fast Python package manager).

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Create and activate virtual environment
uv venv .venv
source .venv/bin/activate

# Install all testing dependencies
uv pip install -r test-requirements.txt

# Verify installation
yamllint --version       # 1.37.1
ansible-lint --version   # 25.8.0
molecule --version       # 25.7.0
ansible --version        # 2.19.0
```

### Method 2: Traditional pip

```bash
# Install testing dependencies
pip install -r test-requirements.txt

# Install the collection locally
ansible-galaxy collection build
ansible-galaxy collection install ./wolskinet-rke2_ansible-*.tar.gz --force
```

### Quick Start Commands

```bash
# Show all available commands
make help

# Quick validation (syntax + build) 
make quick-test

# Lint and syntax checks
make lint

# Unit tests with Molecule
make test-unit

# Integration tests
make test-integration

# Full test suite
make test-all
```

## Linting Configuration

The collection uses a customized ansible-lint configuration to handle specific requirements:

### Ansible-Lint Rules
- **Variable naming exceptions**: The `CF_TOKEN` variable uses uppercase naming for CloudFlare API compatibility
- **Skipped rules**: `var-naming[no-role-prefix]` and `var-naming[pattern]` for specific cases
- **Inline exceptions**: Uses `# noqa: var-naming[pattern]` comments where needed

### Configuration Files
- `.ansible-lint`: Main configuration file with skip rules
- CI pipeline: Dynamically creates configuration during GitLab CI runs

```bash
# Run ansible-lint manually
ansible-lint

# Check specific files
ansible-lint roles/rancher_install/

# Build collection
make build

# Clean up test artifacts
make clean
```

## Testing Tools Included

The `test-requirements.txt` file includes:

- **ansible-core>=2.12** - Core Ansible functionality
- **ansible-lint>=6.0.0** - Ansible best practices linting
- **yamllint>=1.26.0** - YAML syntax and style validation
- **molecule>=6.0.0** - Role testing framework
- **molecule-plugins[docker]>=23.0.0** - Docker driver for Molecule
- **pytest>=7.0.0** - Python testing framework
- **pytest-ansible>=4.0.0** - Ansible-specific pytest features
- **pytest-testinfra>=10.0.0** - Infrastructure testing
- **black>=23.0.0** - Python code formatting
- **isort>=5.0.0** - Python import sorting
- **flake8>=6.0.0** - Python code linting

## Local Testing

### 1. Linting and Syntax Validation

```bash
# YAML linting
yamllint -c .yamllint.yml .

# Ansible linting
ansible-lint roles/ playbooks/

# Syntax checking for all roles
for role in roles/*/; do
  ansible-playbook --syntax-check tests/syntax/test-$(basename $role).yml
done
```

### 2. Unit Testing with Molecule

Test individual roles in isolated containers:

```bash
# Test a specific role
cd roles/helm_install
molecule test

# Test all roles with Molecule scenarios
cd roles/teardown && molecule test
```

#### Available Molecule Scenarios

- **helm_install**: Tests Helm binary installation and functionality
- **teardown**: Tests complete RKE2 cluster cleanup

### 3. Integration Testing

```bash
# Basic integration tests (role interactions)
cd tests/integration
molecule test --scenario-name integration

# Full deployment simulation
molecule test --scenario-name full-deployment
```

### 4. Collection Validation

```bash
# Build and verify collection structure
ansible-galaxy collection build --force
ansible-galaxy collection install wolskinet-rke2_ansible-*.tar.gz --force
ansible-galaxy collection verify wolskinet.rke2_ansible
```

## Testing Framework Structure

```
tests/
├── integration/                 # Cross-role integration tests
│   └── molecule/
│       ├── integration/         # Basic role interaction tests
│       └── full-deployment/     # Complete stack deployment
├── syntax/                      # Syntax validation playbooks
│   ├── test-deploy_rke2.yml
│   ├── test-helm_install.yml
│   └── ...
└── unit/                        # Python unit tests
    ├── __init__.py
    └── test_basic.py

roles/*/molecule/default/        # Individual role tests
├── molecule.yml                 # Test configuration
├── converge.yml                 # Test playbook
└── verify.yml                   # Validation tasks
```

## GitLab CI/CD Pipeline

The collection includes a comprehensive GitLab CI pipeline with the following stages:

### 1. Lint Stage
- **ansible-lint**: Role and playbook linting
- **yaml**: YAML syntax and style validation
- **galaxy**: Collection structure validation

### 2. Unit Test Stage
- **syntax**: Syntax validation for all roles
- **molecule**: Container-based role testing

### 3. Integration Test Stage
- **basic**: Role interaction testing
- **full-stack**: Complete deployment simulation

### 4. Build Stage
- **collection**: Build and validate collection package

### 5. Security Scan Stage
- **ansible-content**: Content security scanning
- **secrets**: Secret detection with TruffleHog

### 6. Deploy Test Stage
- **k8s-cluster**: Kubernetes deployment testing
- **galaxy**: Collection publishing (manual)

## Test Configuration

### Environment Variables

```bash
# Required for CI/CD
export GALAXY_API_KEY="your-galaxy-api-key"

# Optional customization
export ANSIBLE_COLLECTIONS_PATH="${PWD}"
export ANSIBLE_HOST_KEY_CHECKING="False"
export MOLECULE_DRIVER="docker"  # or "podman"
```

### Test Variables

Override default test behavior with these variables:

```yaml
# Skip actual installation in containers
skip_rke2_installation: true
skip_firewall_configuration: true
test_mode: true

# Enable specific test modes
syntax_check_only: true
teardown_dry_run: true
skip_actual_k8s_deployment: true
```

## Testing Best Practices

### 1. Role Testing
- Each role should have its own Molecule scenario
- Test both successful execution and error conditions
- Verify idempotency where applicable
- Include dependency testing for roles with prerequisites

### 2. Integration Testing
- Test role interactions and dependencies
- Validate configuration file generation
- Ensure proper variable inheritance
- Test tag-based selective execution

### 3. Container Limitations
- Some features cannot be tested in containers (systemd services, networking)
- Use test modes and variable overrides to skip unsupported operations
- Focus on configuration generation and validation logic

### 4. Security Testing
- Never commit real secrets or API keys
- Use test certificates and dummy credentials
- Validate that sensitive data is properly templated
- Run security scans on all commits

## Current Test Suite Status

### ✅ Verified Working Features

**Core Testing Infrastructure:**
- **Syntax Tests**: All 8 roles pass Ansible playbook syntax validation (including rke2_upgrade)
- **Collection Build**: Successfully builds 33MB collection package  
- **YAML Linting**: Working (identifies style issues for cleanup)
- **Ansible Linting**: Working with custom configuration (skips var-naming rules for CF_TOKEN)

**Role Testing:**
- **helm_install**: ✅ **100% PASSING** - Full test cycle with mock binary strategy
- **rke2_upgrade**: 🟡 **~70% Pass** - Fails on K8s operations (requires cluster)
- **teardown**: 🟡 **~80% Pass** - Fails on script execution (expected in containers)

**Test Framework:**
- **Molecule scenarios**: 8 role test scenarios (including rke2_upgrade) + 2 integration scenarios
- **Docker integration**: Container-based testing works reliably
- **Dependency management**: Automated installation of required packages
- **Mock strategies**: Proven to work for command-line tools

### 🔄 Known Limitations

- **Kubernetes Operations**: Roles using `kubernetes.core.*` modules need real clusters
- **Binary Execution**: Downloaded scripts can't run in containers without setup
- **WSL2 Issues**: Container tests may fail due to Docker access limitations

## Troubleshooting

### Common Issues

1. **Molecule Docker Issues**
   ```bash
   # Ensure Docker is running and accessible
   docker info
   
   # Clean up old containers
   molecule destroy
   docker system prune -f
   ```

2. **WSL2 and Container Issues**
   When running in WSL2 environments:
   ```bash
   # Skip molecule tests and run other available tests:
   make test-syntax    # ✓ Works in WSL2
   make build         # ✓ Works in WSL2
   
   # Container-dependent tests to skip in WSL2:
   # - make test-unit (molecule tests)
   # - make test-integration (molecule integration tests)
   ```

3. **Collection Import Errors**
   ```bash
   # Rebuild and reinstall collection
   ansible-galaxy collection build --force
   ansible-galaxy collection install ./wolskinet-rke2_ansible-*.tar.gz --force
   ```

4. **Permission Issues**
   ```bash
   # Fix file permissions
   find . -name "*.yml" -exec chmod 644 {} \;
   find . -name "*.py" -exec chmod 644 {} \;
   ```

5. **Virtual Environment Issues**
   ```bash
   # Recreate virtual environment
   rm -rf .venv
   uv venv .venv
   source .venv/bin/activate
   uv pip install -r test-requirements.txt
   ```

6. **Long Build Times**
   The collection build can take 1-2 minutes due to:
   - Large number of files to process
   - Dependency resolution  
   - Metadata validation

### Debug Mode

Enable verbose output for troubleshooting:

```bash
# Molecule with debug output
molecule --debug test

# Ansible with verbose output
ansible-playbook -vvv your-playbook.yml

# GitLab CI debug (add to .gitlab-ci.yml)
variables:
  CI_DEBUG_TRACE: "true"
```

## Test Development Tools

The collection includes automation tools to help fix and enhance tests:

### Molecule Test Fixes

```bash
# Automatically apply fixes to all roles
./fix-molecule-tests.sh

# Or apply manually using templates:
cp .github/templates/molecule-prepare.yml roles/NEW_ROLE/molecule/default/prepare.yml
```

### Test Templates

- **`.github/templates/molecule-prepare.yml`**: Standard container preparation
- **`.github/templates/test-mode-defaults.yml`**: Test mode variable examples

### Individual Role Testing

```bash
# Test specific roles that are working
cd roles/helm_install && molecule test    # ✅ Fully functional
cd roles/teardown && molecule test        # 🟡 Partial (script execution fails)
```

## Contributing Tests

When contributing to the collection:

1. **Add role tests**: Every new role should include a Molecule scenario
2. **Use templates**: Apply standard prepare.yml and test mode variables
3. **Update integration tests**: Add new roles to integration test scenarios
4. **Syntax validation**: Create syntax test playbooks for new roles
5. **Documentation**: Update this guide with new testing procedures
6. **CI/CD**: Ensure new tests are included in the GitLab CI pipeline

### Test Naming Conventions

- Role tests: `roles/ROLE_NAME/molecule/default/`
- Syntax tests: `tests/syntax/test-ROLE_NAME.yml`
- Integration scenarios: `tests/integration/molecule/SCENARIO_NAME/`
- Python tests: `tests/unit/test_COMPONENT.py`

## Performance Testing

For performance validation in CI/CD:

```bash
# Time role execution
time ansible-playbook test-playbook.yml

# Monitor resource usage
docker stats $(docker ps -q) &
molecule test
```

## Coverage Reports

Generate test coverage reports:

```bash
# Ansible role coverage
ansible-playbook --list-tasks test-playbook.yml

# Python test coverage
pytest --cov=plugins/ tests/unit/
```

This testing framework ensures the RKE2 Ansible Collection maintains high quality, security, and reliability across all supported environments and use cases.