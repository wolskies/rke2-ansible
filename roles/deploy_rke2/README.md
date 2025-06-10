Role Name
=========

Role to install and start a bare metal RKE2 cluster with kube-vip and Metallb.

Requirements
------------

* Ansible 2.9.17 or later
* Kubernetes.core ansible collection

Role Variables
--------------

The following variables, with their defaults are settable in the defaults folder:
```
kube_vip_version: "v0.9.1"
rke2_version: "v1.33.1+rke2r1"
metallb_version: v0.15.2

rke2_install_dir: "/usr/local/bin"
kube_vip_noinstall: false
metallb_noinstall: false
disable_networkmanager: true
firewall: ufw
os: "linux"

vip_interface: "eth0"
vip: 192.168.100.30
management_network: "192.168.100.0/24"
lb_range: 192.168.100.240-192.168.100.254
lb_pool_name: first-pool
```
Tags
----

The role provides the following tags to control execution:

version-check
config-firewall
rke2
kube-vip
metallb

Example Playbook
----------------

- name: Deploy RKE2 Cluster
  hosts:
    - rke2
  vars_files:
    - /home/ed/Ansible/inventory/group_vars/secrets.yaml
  become: false
  roles:
    - name: wolskinet.rke2_ansible.deploy_rke2
      become: true

License
-------

GPL-3.0-or-later
