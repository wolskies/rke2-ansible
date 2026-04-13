# wolskinet.rke2_ansible

Ansible collection for deploying and managing a bare-metal RKE2 Kubernetes cluster with Rancher.

The core workflow is `helm_install` → `deploy_rke2` → `rancher_install`. Once Rancher is up, additional applications (monitoring, extra storage, etc.) are typically installed through the Rancher GUI. Storage can also be deployed directly via `longhorn_install` or `rook_install`.

## Supported platforms

- Ubuntu Server 20.04, 22.04, 24.04
- Debian 11, 12
- Rocky / RHEL / Oracle Linux 8, 9
- SUSE Linux Enterprise Server 15 SP3+
- Amazon Linux 2, 2023

Both `amd64` and `arm64` are supported. Primary testing is on Debian/Ubuntu; other distributions are best-effort (Rocky currently hangs at API server readiness).

## Requirements

- Ansible core 2.15+
- Python 3.7+ on managed hosts
- Collections declared in `requirements.yml` (`community.docker`, `kubernetes.core`, `community.general`)
- Hosts must meet the [RKE2 requirements](https://docs.rke2.io/install/requirements)

## Installation

```bash
git clone https://github.com/wolskinet/rke2-ansible.git
cd rke2-ansible
ansible-galaxy collection install -r requirements.yml
ansible-galaxy collection install . --force
```

## Quick start

Copy the secrets template into your inventory, encrypt it, and set the Cloudflare API token (used by cert-manager for Let's Encrypt DNS-01):

```bash
cp playbooks/group_vars/secrets.yaml.example inventory/group_vars/secrets.yaml
ansible-vault encrypt inventory/group_vars/secrets.yaml
```

Inventory must define `controllers` and `agents` groups, typically under a top-level `rke2` group:

```yaml
rke2:
  children:
    controllers:
    agents:
controllers:
  hosts:
    kcontrol01: { ansible_host: 192.168.100.11 }
    kcontrol02: { ansible_host: 192.168.100.12 }
    kcontrol03: { ansible_host: 192.168.100.13 }
agents:
  hosts:
    kworker01: { ansible_host: 192.168.100.14 }
```

Deploy:

```bash
ansible-playbook -i inventory playbooks/deploy-rke2.yaml --ask-vault-pass
```

## Roles

### Cluster deployment

- [`deploy_rke2`](roles/deploy_rke2/README.md) — install RKE2 on controllers and agents; configure kube-vip (HA virtual IP) and MetalLB (load balancer).
- [`helm_install`](roles/helm_install/README.md) — install Helm, the helm-diff plugin, and the `python3-kubernetes` library needed by `kubernetes.core` modules. Pulled in automatically by `deploy_rke2`.
- [`rancher_install`](roles/rancher_install/README.md) — install cert-manager, Traefik, and Rancher. Uses Cloudflare DNS-01 for Let's Encrypt certificates.

### Storage (optional)

Pick one; do not install both.

- [`longhorn_install`](roles/longhorn_install/README.md) — Longhorn distributed block storage.
- [`rook_install`](roles/rook_install/README.md) — Rook-Ceph block, filesystem, and object storage.

### Lifecycle

- [`rke2_upgrade`](roles/rke2_upgrade/README.md) — upgrade RKE2 in place following the manual upgrade process (controllers first, then workers, with optional drain).
- [`teardown`](roles/teardown/README.md) — remove RKE2 and all components this collection installs, including UFW rules.

## Variables

All user-facing variables live in `playbooks/group_vars/all.yaml`. For a flat alphabetical listing, see [`docs/variables.md`](docs/variables.md). Regenerate after edits with:

```bash
python3 scripts/gen_docs.py
```

## Notes

- **OS check**: `deploy_rke2` aborts on unsupported distributions. Skip with `--skip-tags version-check`.
- **NetworkManager**: `deploy_rke2` removes NetworkManager because RKE2's default CNI (Canal) conflicts with it. Disable with `disable_networkmanager: false` or skip via `--skip-tags config-firewall`.
- **firewalld**: disabled if present. UFW rules are configured automatically when UFW is already installed.
- **SELinux** (RHEL/Rocky/Oracle): the role installs `container-selinux` and sets SELinux to permissive during install to avoid kube-vip networking issues.
- **ARM64**: verify your chosen RKE2 version has arm64 container images published before deploying. `v1.31.11+rke2r1` and `v1.32.7+rke2r1` are known to have arm64 images.
- **Interface name**: `vip_interface` defaults to `eth0` and auto-detects the default-route interface when `eth0` is absent.

## Acknowledgments

This collection draws on earlier Ansible work by James Turland ([Jim's Garage](https://github.com/JamesTurland/JimsGarage/tree/main/Ansible/Playbooks/RKE2)) and Isaac Blum ([Space Terran](https://github.com/SpaceTerran/ansible-rancher-traefik-ssl)).

## License

GPL-3.0-or-later — see [`LICENSE`](LICENSE).
