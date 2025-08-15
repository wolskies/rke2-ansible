# Longhorn Install Role

This role deploys Longhorn distributed block storage system on an existing RKE2 Kubernetes cluster. Longhorn provides persistent storage for Kubernetes workloads with features like snapshots, backups, and high availability.

## Requirements

- Ansible 2.12 or later
- kubernetes.core ansible collection
- Running RKE2 cluster (see `wolskinet.rke2_ansible.deploy_rke2`)
- Helm 3.x installed (see `wolskinet.rke2_ansible.helm_install`)

## Role Variables

### General Configuration
```yaml
home_path: /home/{{ ansible_user }}
kubectl_config: "{{ home_path }}/.kube/config"
```

### Longhorn Configuration
```yaml
longhorn_chart_ref: longhorn-stable/longhorn
longhorn_chart_version: "1.9.1"
longhorn_path: "{{ home_path }}/longhorn"
longhorn_namespace: longhorn-system
```

### Component Installation Controls
```yaml
longhorn_install_system: true
```

### Storage Configuration
```yaml
longhorn_create_default_storage_class: true
longhorn_storage_class_name: longhorn
longhorn_replica_count: 3
```

## Tags

The role provides the following tags for selective execution:

- `longhorn` - All Longhorn components
- `storage-longhorn` - Longhorn storage system

## Dependencies

- `wolskinet.rke2_ansible.helm_install` - Helm must be installed
- `wolskinet.rke2_ansible.deploy_rke2` - RKE2 cluster must be running

## Example Playbook

```yaml
---
- name: Deploy Longhorn on RKE2
  hosts: controllers
  vars_files:
    - /home/{{ ansible_user }}/Ansible/inventory/group_vars/secrets.yaml
  become: false
  roles:
    - name: wolskinet.rke2_ansible.longhorn_install
      when: inventory_hostname == (groups['controllers'] | first)
```

### Selective Installation Examples

```bash
# Install Longhorn storage
ansible-playbook longhorn-install.yaml --tags "longhorn"

# Install as part of storage setup
ansible-playbook longhorn-install.yaml --tags "storage-longhorn"
```

## Security Considerations

- Longhorn creates a `longhorn-system` namespace with appropriate RBAC
- Consider backup strategies for persistent volume data
- Review storage class configurations for production deployments

## License

GPL-3.0-or-later

## Author Information

Ed Wolski  
wolskinet