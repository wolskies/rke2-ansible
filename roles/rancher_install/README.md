# Rancher Install Role

This role deploys Rancher on an existing RKE2 cluster. Rancher is installed with Cert Manager for ACME TLS certificates and Traefik for ingress. Storage must be provided separately (see longhorn_install or rook_install roles).

Requirements
------------

* Ansible 2.9.17 or later
* Kubernetes.core ansible collection
* Running RKE2 cluster (see `wolskinet.rke2_ansible.deploy_rke2`)

Role Variables
--------------
```
home_path: /home/{{ ansible_user }}
traefik_domain: example

kubectl_config: "{{ home_path }}/.kube/config"

helm_version: v3.18.4

cert_manager_chart_ref: jetstack/cert-manager
cert_manager_chart_version: v1.18.2
cert_manager_path: "{{ home_path }}/cert-manager"
cert_manager_email: your_email@your_domain.com

traefik_chart_ref: traefik/traefik
traefik_chart_version: 37.0.0
traefik_path: "{{ home_path }}/traefik"

rancher_chart_ref: rancher-stable/rancher
rancher_chart_version: 2.11.3
rancher_path: "{{ home_path }}/rancher"

longhorn_chart_ref: longhorn/longhorn
longhorn_chart_version: 1.9.1
longhorn_path: "{{ home_path }}/longhorn"

# Cloudflare API Token for Let's Encrypt DNS-01 challenge
cf_token: "{{ CF_TOKEN }}"
```

## Required Secrets

This role requires a Cloudflare API token for Let's Encrypt certificate generation. Store this in an encrypted ansible-vault file:

**secrets.yaml** (encrypt with `ansible-vault create secrets.yaml`):
```yaml
---
CF_TOKEN: "your_cloudflare_api_token_here"
```

The role maps `CF_TOKEN` from your vault file to the `cf_token` variable used in templates.

Dependencies
------------

None

Example Playbook
----------------
```
---
- name: Deploy RKE2 Cluster
  hosts:
    - rke2
  vars_files:
    - /home/user/Ansible/inventory/group_vars/secrets.yaml
  become: false
  roles:
    - name: wolskinet.rke2_ansible.deploy_rke2
      become: true
    - name: wolskinet.rke2_ansible.rancher_install
      when: inventory_hostname == (groups['controllers'] | first)
      become: false
```

## License

GPL-3.0-or-later

## Author Information

Ed Wolski / wolskinet