# rancher_install

Install cert-manager, Traefik, and Rancher on an existing RKE2 cluster. Cert-manager issues Let's Encrypt wildcard certificates via the Cloudflare DNS-01 challenge.

## What it does

- **cert-manager** (tag `cert-manager`, runs when `rke2_install_certbot: true`): adds the Jetstack Helm repo, installs cert-manager with CRDs, applies a `ClusterIssuer` for Cloudflare DNS-01 in either `staging` or `production`.
- **Traefik** (tag `traefik`, runs when `rke2_install_traefik: true`): installs Traefik from its Helm chart and applies a wildcard `Certificate` via cert-manager.
- **Rancher** (tag `rancher`): installs the Rancher `rancher-stable` Helm chart into the `cattle-system` namespace.

Should run on the first controller only.

## Requirements

- Running RKE2 cluster (see `deploy_rke2`).
- Helm and `kubernetes.core` dependencies (see `helm_install`).
- Cloudflare API token with `Zone:Zone:Read` and `Zone:DNS:Edit`, passed as the vault variable `CF_TOKEN`. The role maps it to `cf_token` for the ClusterIssuer template.

Store the token in an ansible-vault file:

```yaml
# inventory/group_vars/secrets.yaml  (encrypted with ansible-vault)
CF_TOKEN: "your_cloudflare_token"
```

## Usage

```yaml
- hosts: rke2
  vars_files:
    - inventory/group_vars/secrets.yaml
  roles:
    - role: wolskinet.rke2_ansible.rancher_install
      when: inventory_hostname == groups['controllers'][0]
```

## Tags

`cert-manager`, `traefik`, `rancher`.

## Variables

See [`docs/variables.md`](../../docs/variables.md). Key settings: `traefik_domain`, `letsencrypt_env`, `cert_manager_email`, `cf_token`, `rancher_chart_version`.
