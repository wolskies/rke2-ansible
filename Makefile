# SPDX-License-Identifier: GPL-3.0-or-later
# Makefile for RKE2 Ansible Collection Testing

.PHONY: help install-deps lint test-unit test-integration test-all build clean

# Default target
help: ## Show this help message
	@echo "RKE2 Ansible Collection - Testing Commands"
	@echo "==========================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install-deps: ## Install testing dependencies
	@echo "Installing testing dependencies..."
	pip install -r test-requirements.txt
	ansible-galaxy collection install community.docker kubernetes.core community.general

lint: ## Run linting and syntax checks
	@echo "Running YAML linting..."
	yamllint -c .yamllint.yml .
	@echo "Running Ansible linting..."
	ansible-lint roles/ playbooks/
	@echo "Running syntax checks..."
	@for role in roles/*/; do \
		echo "Testing syntax for role: $$(basename $$role)"; \
		ansible-playbook --syntax-check tests/syntax/test-$$(basename $$role).yml || exit 1; \
	done

test-unit: ## Run unit tests with Molecule
	@echo "Running Molecule unit tests..."
	@for role in deploy_rke2 helm_install longhorn_install minio_install mysql_operator rancher_install rook_install teardown; do \
		echo "Testing role: $$role"; \
		cd roles/$$role && molecule test && cd ../..; \
	done

test-integration: ## Run integration tests
	@echo "Running integration tests..."
	cd tests/integration && molecule test --scenario-name integration
	@echo "Running full deployment tests..."
	cd tests/integration && molecule test --scenario-name full-deployment

test-syntax: ## Run syntax validation only
	@echo "Running syntax validation..."
	@for role in roles/*/; do \
		echo "Testing syntax for role: $$(basename $$role)"; \
		ansible-playbook --syntax-check tests/syntax/test-$$(basename $$role).yml || exit 1; \
	done

test-all: lint test-unit test-integration ## Run all tests
	@echo "All tests completed successfully!"

build: ## Build the collection
	@echo "Building collection..."
	ansible-galaxy collection build --force
	@echo "Verifying collection..."
	ansible-galaxy collection install wolskinet-rke2_ansible-*.tar.gz --force
	ansible-galaxy collection verify wolskinet.rke2_ansible

security-scan: ## Run security scans
	@echo "Running security scans..."
	@command -v trufflehog >/dev/null 2>&1 && trufflehog filesystem --directory=. --json > secrets-scan.json || echo "TruffleHog not installed, skipping secret scan"
	@pip list | grep -q ansible-content-scanner && ansible-content-scanner scan . || echo "ansible-content-scanner not installed, skipping content scan"

clean: ## Clean up test artifacts
	@echo "Cleaning up test artifacts..."
	find . -name "*.tar.gz" -delete
	find . -name ".molecule" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	docker system prune -f 2>/dev/null || true

install-local: build ## Install collection locally
	@echo "Installing collection locally..."
	ansible-galaxy collection install wolskinet-rke2_ansible-*.tar.gz --force

molecule-destroy: ## Destroy all Molecule instances
	@echo "Destroying Molecule instances..."
	@for role in deploy_rke2 helm_install longhorn_install minio_install mysql_operator rancher_install rook_install teardown; do \
		cd roles/$$role && molecule destroy && cd ../..; \
	done
	cd tests/integration && molecule destroy --scenario-name integration
	cd tests/integration && molecule destroy --scenario-name full-deployment

# Development helpers
dev-setup: install-deps install-local ## Set up development environment
	@echo "Development environment ready!"

quick-test: test-syntax build ## Quick validation (syntax + build)
	@echo "Quick test completed!"

# CI/CD helpers
ci-test: lint test-unit ## Run CI-appropriate tests
	@echo "CI tests completed!"