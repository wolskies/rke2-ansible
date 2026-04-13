# teardown

Remove RKE2 and every component this collection installs from a set of hosts. Destructive and irreversible — run `--check` first if in doubt.

## What it does

- Downloads the RKE2 install script and runs it; this puts the `rke2-uninstall.sh` helper in place on hosts where it is missing.
- Stops and disables `rke2-server` and `rke2-agent` services.
- Runs `/usr/local/bin/rke2-uninstall.sh`.
- Deletes RKE2 state, systemd units, containerd data, and kubelet directories.
- Removes per-component working directories under `$HOME` (`metallb/`, `cert-manager/`, `traefik/`, `rancher/`, `longhorn/`, kubectl config).
- Deletes UFW rules added by `deploy_rke2` (controller rules on controllers, common rules everywhere).
- Reboots the host at the end.

## Usage

```yaml
- hosts: rke2
  roles:
    - role: wolskinet.rke2_ansible.teardown
      become: true
```

## Tags

- `cleanup-rke2` — stop services, run uninstaller, remove RKE2 artifacts (runs by default via `always`)
- `cleanup-config` — delete per-component `$HOME` directories (runs by default via `always`)
- `cleanup-storage` — clean containerd data, `/var/lib/kubelet`, CNI and run dirs
- `cleanup-firewall` — gather package facts (prerequisite for UFW removal)

## Variables

Reads path variables (`kubectl_config`, `metallb_path`, `cert_manager_path`, `traefik_path`, `rancher_path`, `longhorn_path`) and UFW rule lists (`ufw_rules_common`, `ufw_rules_controllers`) from `playbooks/group_vars/all.yaml` and role `vars/`. See [`docs/variables.md`](../../docs/variables.md).

## Known issue

UFW cleanup is gated on `firewall == 'ufw'`, but the `firewall` variable is not defined anywhere in this collection. As a result, UFW rules silently fail to be removed on a default teardown.
