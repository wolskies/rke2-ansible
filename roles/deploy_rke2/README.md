# Deploy RKE2 Role

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
rke2_version: "v1.31.11+rke2r1"
metallb_version: v0.15.2

rke2_install_dir: "/usr/local/bin"
kube_vip_noinstall: false
metallb_noinstall: false
disable_networkmanager: true
firewall: ufw
rke2_os: "linux"

vip_interface: "eth0"
vip: 192.168.100.30
management_network: "192.168.100.0/24"
lb_range: 192.168.100.240-192.168.100.254
lb_pool_name: first-pool
```
Tags
----

The role provides the following tags to control execution:

**Core Tags:**
- `version-check` - OS and architecture validation
- `config-firewall` - Firewall and network preparation  
- `rke2` - RKE2 binary installation and core cluster setup
- `rke2-bootstrap` - Initial cluster bootstrap (first controller only)
- `rke2-servers` - Additional controller node setup
- `rke2-agents` - Agent/worker node setup

**Network Components:**
- `rke2-network` - All networking components
- `kube-vip` - Virtual IP configuration for HA
- `metallb` - Load balancer installation

**Usage Examples:**
```bash
# Install only RKE2 core without networking
ansible-playbook deploy-rke2.yaml --tags "rke2" --skip-tags "rke2-network"

# Skip firewall configuration
ansible-playbook deploy-rke2.yaml --skip-tags "config-firewall"

# Only bootstrap the first controller
ansible-playbook deploy-rke2.yaml --tags "rke2-bootstrap" --limit "controllers[0]"
```

Example Playbook
----------------
```
- name: Deploy RKE2 Cluster
  hosts:
    - rke2
  vars_files:
    - /home/{{ ansible_user }}/Ansible/inventory/group_vars/secrets.yaml
  become: false
  roles:
    - name: wolskinet.rke2_ansible.deploy_rke2
      become: true
```
## License

GPL-3.0-or-later

## Author Information

Ed Wolski / wolskinet
