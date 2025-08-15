# SPDX-License-Identifier: GPL-3.0-or-later

# Testing Guide for RKE2 Ansible Collection

This document provides comprehensive guidance for testing the `wolskinet.rke2_ansible` collection both locally and in CI/CD environments.

## Quick Start

### Prerequisites

```bash
# Install testing dependencies
pip install -r test-requirements.txt

# Install the collection locally
ansible-galaxy collection build
ansible-galaxy collection install ./wolskinet-rke2_ansible-*.tar.gz --force
```

### Run All Tests

```bash
# Lint and syntax checks
make lint

# Unit tests with Molecule
make test-unit

# Integration tests
make test-integration

# Full test suite
make test-all
```

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
cd roles/mysql_operator && molecule test
cd roles/teardown && molecule test
```

#### Available Molecule Scenarios

- **helm_install**: Tests Helm binary installation and functionality
- **mysql_operator**: Tests MySQL Operator deployment (with Helm dependency)
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

2. **Collection Import Errors**
   ```bash
   # Rebuild and reinstall collection
   ansible-galaxy collection build --force
   ansible-galaxy collection install ./wolskinet-rke2_ansible-*.tar.gz --force
   ```

3. **Permission Issues**
   ```bash
   # Fix file permissions
   find . -name "*.yml" -exec chmod 644 {} \;
   find . -name "*.py" -exec chmod 644 {} \;
   ```

4. **Dependency Issues**
   ```bash
   # Update test dependencies
   pip install -r test-requirements.txt --upgrade
   ```

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

## Contributing Tests

When contributing to the collection:

1. **Add role tests**: Every new role should include a Molecule scenario
2. **Update integration tests**: Add new roles to integration test scenarios
3. **Syntax validation**: Create syntax test playbooks for new roles
4. **Documentation**: Update this guide with new testing procedures
5. **CI/CD**: Ensure new tests are included in the GitLab CI pipeline

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