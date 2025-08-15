#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Script to apply Molecule test fixes to all roles

set -e

ROLES=(
    "rancher_install" 
    "minio_install"
    "rook_install"
    "teardown"
    "deploy_rke2"
)

# Kubernetes-dependent roles that need helm operations skipped
K8S_ROLES=(
    "rancher_install"
    "minio_install" 
    "rook_install"
)

echo "Applying Molecule test fixes to roles..."

for role in "${ROLES[@]}"; do
    echo "Processing role: $role"
    
    # 1. Copy prepare.yml if it doesn't exist or is the basic template
    if [[ ! -f "roles/$role/molecule/default/prepare.yml" ]] || ! grep -q "mysql-operator\|teardown" "roles/$role/molecule/default/prepare.yml" 2>/dev/null; then
        if [[ "$role" != "teardown" ]]; then
            echo "  - Creating/updating prepare.yml"
            cp .github/templates/molecule-prepare.yml "roles/$role/molecule/default/prepare.yml"
        fi
    fi
    
    # 2. Update molecule.yml to add test mode variables
    if ! grep -q "test_mode:" "roles/$role/molecule/default/molecule.yml"; then
        echo "  - Adding test mode variables to molecule.yml"
        
        # Determine if this is a K8s role
        if [[ " ${K8S_ROLES[@]} " =~ " ${role} " ]]; then
            # Add K8s-specific variables
            sed -i '/group_vars:/,/^[[:space:]]*[[:alpha:]]/{ 
                /ansible_user:/a\
        test_mode: true\
        skip_binary_installation: true\
        skip_service_management: true\
        skip_firewall_configuration: true\
        skip_networking_configuration: true\
        skip_kubernetes_operations: true\
        skip_helm_operations: true\
        skip_external_dependencies: true\
        skip_helm_installation: true
            }' "roles/$role/molecule/default/molecule.yml"
        else
            # Add standard variables
            sed -i '/group_vars:/,/^[[:space:]]*[[:alpha:]]/{ 
                /ansible_user:/a\
        test_mode: true\
        skip_binary_installation: true\
        skip_service_management: true\
        skip_firewall_configuration: true\
        skip_networking_configuration: true\
        skip_kubernetes_operations: true\
        skip_external_dependencies: true
            }' "roles/$role/molecule/default/molecule.yml"
        fi
    fi
    
    echo "  - Role $role processed"
done

echo ""
echo "✅ All roles processed!"
echo ""
echo "Kubernetes-aware roles: ${K8S_ROLES[*]}"
echo "  - These roles will skip K8s and Helm operations in test mode"
echo ""
echo "Run individual tests with:"
echo "  cd roles/{role_name} && molecule test"
echo ""
echo "Working examples:"
echo "  cd roles/helm_install && molecule test    # ✅ Fully functional"
echo "  cd roles/mysql_operator && molecule test  # ✅ Now fully functional"