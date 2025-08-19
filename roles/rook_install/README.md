# Rook-Ceph Install Role

This role installs and configures [Rook](https://rook.io) to deploy a full Ceph distributed storage system on a Kubernetes cluster. Rook provides block, object, and shared filesystem storage with self-healing capabilities.

## Features

- **Preflight checks**: Validates kernel, Kubernetes, RBD, and LVM requirements
- **Rook Operator**: Installs Rook-Ceph operator v1.17.7 via Helm
- **Ceph Cluster**: Deploys Ceph v18.2.2 cluster with configurable settings
- **Block Storage**: Creates RBD StorageClass for persistent volumes
- **Optional Components**:
  - CephFilesystem for shared filesystem storage
  - CephObjectStore for S3-compatible object storage
- **Monitoring**: Optional Ceph dashboard integration

## Requirements

- Ansible 2.12 or later
- kubernetes.core ansible collection
- Running RKE2 cluster (see `wolskinet.rke2_ansible.deploy_rke2`)
- Helm 3.x installed (see `wolskinet.rke2_ansible.helm_install`)
- **Minimum 50MB raw storage capacity** per node (suitable for testing)

## Role Variables

### General Configuration
```yaml
home_path: /home/{{ ansible_user }}
kubectl_config: "{{ home_path }}/.kube/config"
rook_ceph_namespace: rook-ceph
```

### Ceph Cluster Configuration
```yaml
rook_ceph_operator_chart_version: "1.17.7"
rook_ceph_version: "v18.2.2"
rook_ceph_min_device_capacity: "50Mi"
rook_ceph_mon_count: 3
rook_ceph_replica_size: 1
```

### Storage Classes
```yaml
rook_ceph_storage_class_name: rook-ceph-block
rook_ceph_make_storage_class_default: true
```

### Optional Components
```yaml
rook_ceph_enable_filesystem: false  # CephFS shared storage
rook_ceph_enable_objectstore: false # S3-compatible object storage
```

## Tags

The role provides the following tags for selective execution:

- `storage-rook` - All Rook-Ceph components
- `rook-operator` - Rook operator only
- `rook-cluster` - Ceph cluster deployment

## Dependencies

- `wolskinet.rke2_ansible.helm_install` - Helm must be installed
- `wolskinet.rke2_ansible.deploy_rke2` - RKE2 cluster must be running

## Example Playbook

```yaml
---
- name: Deploy Rook-Ceph on RKE2
  hosts: controllers
  become: false
  roles:
    - name: wolskinet.rke2_ansible.rook_install
      when: inventory_hostname == (groups['controllers'] | first)
```

### Selective Installation Examples

```bash
# Install complete Rook-Ceph system
ansible-playbook rook-install.yaml --tags "storage-rook"

# Install only the operator
ansible-playbook rook-install.yaml --tags "rook-operator"
```

## Important Notes

⚠️ **Storage Requirements**: Each node must have at least 50MB of raw storage capacity available for Ceph (testing configuration). For production deployments, increase `rook_ceph_min_device_capacity` to appropriate values (e.g., "100Gi" or higher).

⚠️ **Production Considerations**: 
- Default replica size is 1 (no redundancy) - increase for production
- Monitor cluster performance and adjust replica count based on node count
- Consider enabling monitoring for production deployments

## Alternative to Longhorn

This role provides an alternative to the `longhorn_install` role. Do not install both storage solutions simultaneously as they may conflict.

## License

GPL-3.0-or-later

## Author Information

Ed Wolski  
wolskinet

