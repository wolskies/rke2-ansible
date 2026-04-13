# helm_install

Install Helm 3, the helm-diff plugin, and the `python3-kubernetes` library required by `kubernetes.core` modules.

## What it does

- Installs `curl` and `git` via the distro package manager (APT, DNF, or Zypper).
- Downloads and runs the official `get-helm-3` installer; Helm ends up at `/usr/local/bin/helm`.
- Installs the helm-diff plugin if missing.
- On controller nodes only, installs `python3-kubernetes` via the distro package manager (Debian/Ubuntu, SUSE) or pip (RHEL, fallback).

## Usage

```yaml
- hosts: rke2
  roles:
    - wolskinet.rke2_ansible.helm_install
```

`deploy_rke2` already depends on this role; call it directly only if you want Helm without RKE2.

## Tags

- `helm` — Helm binary install
- `helm-diff` — helm-diff plugin install
- `python3-kubernetes` — controller-only Python library install

## Variables

`helm_version` (default `v3.18.4`) lives in `playbooks/group_vars/all.yaml`. See [`docs/variables.md`](../../docs/variables.md).
