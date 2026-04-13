# rke2_upgrade

In-place RKE2 cluster upgrade following the [manual upgrade process](https://docs.rke2.io/upgrades/manual_upgrade).

## What it does

- Asserts the host OS is in the supported list (skip with `--skip-tags version-check`).
- Upgrades control-plane nodes one at a time: download binary → stop RKE2 → replace binary → start RKE2 → wait for Ready.
- Upgrades worker nodes one at a time: optional cordon + drain → download → stop → replace → start → wait for Ready → uncordon.

Runs against hosts in the `controllers` and `workers` inventory groups.

> **Group-name mismatch**: `deploy_rke2` expects the worker group to be named `agents`; `rke2_upgrade` expects `workers`. Either rename your inventory group between lifecycle stages or add workers to both groups.

## Requirements

- Existing RKE2 cluster deployed with `deploy_rke2`.
- `kubernetes.core` and `python3-kubernetes` (installed by `helm_install`) for drain/uncordon.

## Usage

```yaml
- hosts: all
  become: true
  roles:
    - wolskinet.rke2_ansible.rke2_upgrade
```

Or use the bundled playbook, which also prints cluster status before and after:

```bash
ansible-playbook -i inventory playbooks/upgrade-rke2.yml
```

## Tags

- `rke2-upgrade` — run the full upgrade
- `rke2-upgrade-controllers` — control-plane only
- `rke2-upgrade-workers` — workers only
- `version-check` — OS/arch validation only

## Variables

See [`docs/variables.md`](../../docs/variables.md). Key settings: `rke2_version` (target), `upgrade_drain_nodes`, `upgrade_drain_timeout`, `upgrade_drain_grace_period`, `node_ready_timeout`.
