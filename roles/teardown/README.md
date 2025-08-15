# Teardown Role

This role provides a complete teardown and cleanup of RKE2 clusters and associated components. It safely removes RKE2 installations, configuration files, and firewall rules while preserving data when needed.

## Requirements

- Ansible 2.12 or later
- Running RKE2 cluster to be removed
- Appropriate sudo/root access on target nodes

## Role Variables

### General Configuration
```yaml
home_path: /home/{{ ansible_user }}
```

### RKE2 Configuration
```yaml
rke2_install_dir: "/usr/local/bin"
rke2_version: "v1.33.3+rke2r1"
```

### Component Paths
```yaml
kubectl_config: "{{ home_path }}/.kube/config"
metallb_path: "{{ home_path }}/metallb"
cert_manager_path: "{{ home_path }}/cert-manager"
traefik_path: "{{ home_path }}/traefik"
rancher_path: "{{ home_path }}/rancher"
longhorn_path: "{{ home_path }}/longhorn"
minio_operator_path: "{{ home_path }}/minio-operator"
minio_tenant_path: "{{ home_path }}/minio-tenant"
mysql_operator_path: "{{ home_path }}/mysql-operator"
```

## Tags

The role provides the following tags for selective cleanup:

- `cleanup-rke2` - Remove RKE2 cluster and binaries
- `cleanup-config` - Remove configuration files and directories
- `cleanup-storage` - Remove storage-related components (DirectPV, etc.)
- `always` - Tasks that always run (RKE2 and config cleanup)

## Dependencies

None - this role is designed to clean up after other roles.

## Example Playbook

```yaml
---
- name: Complete RKE2 Teardown
  hosts: rke2
  become: true
  roles:
    - name: wolskinet.rke2_ansible.teardown
```

### Selective Cleanup Examples

```bash
# Complete teardown (everything)
ansible-playbook teardown.yaml

# Remove only configuration files, keep RKE2 cluster running
ansible-playbook teardown.yaml --tags "cleanup-config" --skip-tags "cleanup-rke2"

# Remove only storage components
ansible-playbook teardown.yaml --tags "cleanup-storage"

# Remove everything except storage data
ansible-playbook teardown.yaml --skip-tags "cleanup-storage"
```

## What Gets Removed

### RKE2 Cluster Components (`cleanup-rke2`)
- RKE2 services and containers
- RKE2 binary files
- RKE2 system configurations
- Container runtime data

### Configuration Files (`cleanup-config`)
- kubectl configuration
- Component configuration directories:
  - MetalLB configurations
  - cert-manager configurations  
  - Traefik configurations
  - Rancher configurations
  - Longhorn configurations
  - MinIO operator and tenant configurations
  - MySQL operator configurations

### Storage Components (`cleanup-storage`)
- DirectPV binary
- Storage driver configurations

### Firewall Rules
- UFW rules for RKE2 controllers
- UFW rules for RKE2 agents
- Network policies (if configured)

## Safety Considerations

⚠️ **WARNING**: This role performs destructive operations that cannot be undone.

### Before Running Teardown:
1. **Backup important data** - Especially persistent volumes and databases
2. **Export important configurations** - Save any custom Kubernetes resources
3. **Verify inventory** - Ensure you're targeting the correct hosts
4. **Test with `--check`** - Run in check mode first to see what would be removed

### What is NOT Removed:
- User data in persistent volumes (unless the storage backend is removed)
- External resources created outside the cluster
- DNS records or external load balancers
- Certificates stored outside the cluster

## Recovery

After teardown, you can redeploy using the same playbooks:

```bash
# After teardown, redeploy fresh cluster
ansible-playbook deploy-rke2.yaml
ansible-playbook rancher-install.yaml  # if needed
```

## License

GPL-3.0-or-later

## Author Information

Ed Wolski  
wolskinet