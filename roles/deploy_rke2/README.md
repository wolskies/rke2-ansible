# deploy_rke2

Install and start an RKE2 cluster on bare-metal hosts. Configures kube-vip (HA virtual IP) and MetalLB (load balancer).

## What it does

- Asserts the host OS is in the supported list (skip with `--skip-tags version-check`).
- Removes NetworkManager unless `disable_networkmanager: false` — Canal CNI conflicts with it.
- Disables firewalld; configures UFW rules if UFW is installed.
- On RHEL / Rocky / Oracle: installs `container-selinux` and sets SELinux permissive during install.
- Downloads the RKE2 binary for the host's architecture (amd64 or arm64).
- Bootstraps the first controller, joins additional controllers, then joins agents.
- Installs kube-vip as a static pod when `rke2_install_kubevip: true`.
- Installs MetalLB from the first controller when `rke2_install_metallb: true`.

## Requirements

- Inventory groups `controllers` and `agents`.
- Ansible 2.15+; collections `kubernetes.core`, `community.general`.
- Pulls `helm_install` in as a role dependency.

## Usage

```yaml
- hosts: rke2
  become: false
  roles:
    - role: wolskinet.rke2_ansible.deploy_rke2
      become: true
```

## Tags

- `version-check` — OS / arch validation only
- `config-firewall` — NetworkManager / firewalld / UFW setup
- `rke2` — binary install and cluster configuration
- `rke2-bootstrap`, `rke2-servers`, `rke2-agents` — per-phase
- `kube-vip`, `metallb`, `rke2-network` — networking components

## Variables

See [`docs/variables.md`](../../docs/variables.md) for the full list. Defaults live in `playbooks/group_vars/all.yaml`.
