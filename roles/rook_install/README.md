# Ansible Role: rook_ceph

This role installs and configures [Rook](https://rook.io) to deploy a full Ceph storage system on a Kubernetes cluster.

## Features

- Preflight checks (kernel, Kubernetes, RBD, LVM)
- Installs Rook Ceph operator via Helm
- Creates CephCluster and RBD StorageClass
- Optional: Deploy CephFilesystem and CephObjectStore
- Optional: Set StorageClasses as default

## Requirements

- Helm 3 installed
- `kubernetes.core` collection
- Kubernetes cluster running (v1.28–v1.33)

## Role Variables

See `defaults/main.yml` for full configuration options.

## Example Playbook

```yaml
- hosts: localhost
  roles:
    - role: rook_ceph

