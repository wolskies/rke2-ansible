# rook_install

Deploy the Rook-Ceph operator and a Ceph cluster on an existing RKE2 cluster. Provides RBD block storage; optionally CephFS and RGW object storage.

## What it does

- Preflight checks for kernel modules (`rbd`), LVM, and Ceph client tools (tag `rook-prereqs`).
- Installs the Rook operator via Helm (tag `rook-operator`, when `rook_install_operator: true`).
- Deploys a `CephCluster` and RBD `StorageClass` (tag `rook-cluster`, when `rook_install_cluster: true`).
- Optionally deploys a `CephFilesystem` (tag `rook-filesystem`, when `rook_ceph_enable_filesystem: true`).
- Optionally deploys a `CephObjectStore` (tag `rook-objectstore`, when `rook_ceph_enable_objectstore: true`).

Do not install alongside `longhorn_install`.

## Requirements

- Running RKE2 cluster (`deploy_rke2`) and Helm (`helm_install`).
- Raw storage available on each node. The default `rook_ceph_min_device_capacity: 50Mi` is test-only — raise to `100Gi` or higher for production.
- `rook_ceph_replica_size` defaults to `1` (no redundancy); raise for production.

## Usage

```yaml
- hosts: rke2
  roles:
    - role: wolskinet.rke2_ansible.rook_install
      when: inventory_hostname == groups['controllers'][0]
```

## Tags

`storage-rook`, `rook-prereqs`, `rook-operator`, `rook-cluster`, `rook-filesystem`, `rook-objectstore`.

## Variables

See [`docs/variables.md`](../../docs/variables.md). Key settings: `rook_ceph_version`, `rook_ceph_mon_count`, `rook_ceph_replica_size`, `rook_ceph_min_device_capacity`, `rook_ceph_enable_filesystem`, `rook_ceph_enable_objectstore`.
