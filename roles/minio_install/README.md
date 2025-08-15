# MinIO Install Role

This role deploys MinIO object storage on an existing RKE2 Kubernetes cluster. It includes the MinIO Operator, DirectPV storage driver, and MinIO tenant deployment with optional cert-manager integration.

## Requirements

- Ansible 2.12 or later
- kubernetes.core ansible collection
- Running RKE2 cluster (see `wolskinet.rke2_ansible.deploy_rke2`)
- Helm 3.x installed (see `wolskinet.rke2_ansible.helm_install`)

## Role Variables

### General Configuration
```yaml
home_path: /home/{{ ansible_user }}
traefik_domain: example
kubectl_config: "{{ home_path }}/.kube/config"
```

### MinIO Operator Configuration
```yaml
minio_operator_path: "{{ home_path }}/minio-operator"
minio_operator_namespace: minio-operator
```

### MinIO Tenant Configuration
```yaml
minio_tenant_path: "{{ home_path }}/minio-tenant"
minio_tenant_namespace: minio-tenant
minio_tenant_name: "minio"
minio_root_user: "minio"
minio_root_password: "minio123"
minio_servers: 4
minio_volumes_per_server: 1
minio_capacity_per_tenant: "1Ti"
```

### DirectPV Storage Driver
```yaml
minio_csi_driver_name: "directpv-min-io"
direct_pv_version: "4.1.5"
```

### Console Access
```yaml
console_access_key: "console"
console_secret_key: "console123"
minio_browser: "on"
```

### Component Installation Controls
```yaml
minio_install_operator: true
minio_install_tenant: true
minio_install_directpv: true
```

## Tags

The role provides the following tags for selective execution:

- `storage-minio` - All MinIO components
- `minio-operator` - MinIO operator deployment only
- `minio-tenant` - MinIO tenant deployment only
- `minio-directpv` - DirectPV storage driver only

## Dependencies

- `wolskinet.rke2_ansible.helm_install` - Helm must be installed
- `wolskinet.rke2_ansible.deploy_rke2` - RKE2 cluster must be running

## Example Playbook

```yaml
---
- name: Deploy MinIO on RKE2
  hosts: controllers
  vars_files:
    - /home/{{ ansible_user }}/Ansible/inventory/group_vars/secrets.yaml
  become: false
  roles:
    - name: wolskinet.rke2_ansible.minio_install
      when: inventory_hostname == (groups['controllers'] | first)
```

### Selective Installation Examples

```bash
# Install only the MinIO operator
ansible-playbook minio-install.yaml --tags "minio-operator"

# Install everything except DirectPV
ansible-playbook minio-install.yaml --skip-tags "minio-directpv"

# Install operator and tenant, skip DirectPV
ansible-playbook minio-install.yaml --tags "minio-operator,minio-tenant"
```

## Security Considerations

- Change default passwords in production deployments
- Use `ansible-vault` for sensitive variables like `minio_root_password`
- Consider using cert-manager for TLS certificate management
- Store console credentials securely

## License

GPL-3.0-or-later

## Author Information

Ed Wolski  
wolskinet