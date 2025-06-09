Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

home_path: /home/{{ ansible_user }}
traefik_domain: example

kubectl_config: "{{ home_path }}/.kube/config"

# https://github.com/helm/helm/releases
helm_version: v3.18.2

cert_manager_chart_ref: jetstack/cert-manager
# https://github.com/cert-manager/cert-manager/releases
cert_manager_chart_version: v1.15.0
cert_manager_path: "{{ home_path }}/cert-manager"
cert_manager_email: your_email@your_domain.com

traefik_chart_ref: traefik/traefik
# https://github.com/traefik/traefik-helm-chart/releases
traefik_chart_version: 28.3.0
traefik_path: "{{ home_path }}/traefik"

# https://github.com/rancher/rancher/releases
rancher_chart_ref: rancher/rancher
rancher_chart_version: 2.11.2
rancher_path: "{{ home_path }}/rancher"

longhorn_chart_ref: longhorn/longhorn
longhorn_chart_version: 1.9.0
longhorn_path: "{{ home_path }}/longhorn"

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
    - /home/ed/Ansible/inventory/group_vars/secrets.yaml
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

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
