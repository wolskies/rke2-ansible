Role Name
=========

This role deploys Rancher on an existing RKE2 cluster.  Rancher is installed with Cert Mangager for ACME TLS certificates, and Longhorn for storage.

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
rancher_chart_version: 2.12.0
rancher_path: "{{ home_path }}/rancher"

longhorn_chart_ref: longhorn/longhorn
longhorn_chart_version: 1.9.1
longhorn_path: "{{ home_path }}/longhorn"
```

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
    - /home/{{ ansible_user }}/Ansible/inventory/group_vars/secrets.yaml
  become: false
  roles:
    - name: wolskinet.rke2_ansible.deploy_rke2
      become: true
    - name: wolskinet.rke2_ansible.rancher_install
      when: inventory_hostname == (groups['servers'] | first)
      become: false
```

License
-------

GPL-3.0-or-later