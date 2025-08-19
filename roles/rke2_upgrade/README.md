# RKE2 Upgrade Role

This role performs manual upgrades of RKE2 clusters following the official upgrade process.

## Requirements

- An existing RKE2 cluster deployed with the `deploy_rke2` role
- Ansible 2.15 or higher
- SSH access to all cluster nodes
- kubectl configured with cluster access

## Role Variables

```yaml
# Target RKE2 version to upgrade to
rke2_version: "v1.31.11+rke2r1"

# RKE2 installation directory (same as deploy_rke2)
rke2_install_dir: "/usr/local/bin"

# Operating system (linux)
rke2_os: "linux"

# User configuration
ansible_user: "{{ ansible_user_id }}"

# Upgrade strategy
upgrade_drain_nodes: true
upgrade_drain_timeout: 300
upgrade_drain_grace_period: 30
upgrade_drain_delete_emptydir_data: true
```

## Dependencies

None. This role is designed to work with clusters deployed using the `deploy_rke2` role.

## Example Playbook

```yaml
---
- name: Upgrade RKE2 cluster
  hosts: all
  become: true
  gather_facts: true
  vars:
    rke2_version: "v1.31.11+rke2r1"
  roles:
    - wolskinet.rke2_ansible.rke2_upgrade
```

## Upgrade Process

The role follows the official RKE2 manual upgrade process:

1. Upgrades control plane nodes one at a time:
   - Downloads new RKE2 binary
   - Stops RKE2 service
   - Replaces binary
   - Starts RKE2 service
   - Waits for node to be ready

2. Upgrades worker nodes one at a time:
   - Optionally drains the node
   - Downloads new RKE2 binary
   - Stops RKE2 service
   - Replaces binary
   - Starts RKE2 service
   - Waits for node to be ready
   - Uncordons the node if it was drained

## Tags

- `rke2-upgrade`: Run the complete upgrade process
- `rke2-upgrade-controllers`: Upgrade only control plane nodes
- `rke2-upgrade-workers`: Upgrade only worker nodes

## License

GPL-3.0-or-later

## Author Information

Ed Swallow - WolskiNet