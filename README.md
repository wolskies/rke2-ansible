## Ansible Collection: rke2_ansible

This collection includes a number of roles for the creation and management of an RKE2 cluster of bare-metal systems.

## Description

This collection automates the deployment and management of a bare-metal RKE2 cluster.  It includes roles to install Metallb, Traefik, Cert-Manager, Rancher and Longhorn.  While it can be adapted to other distributions, it is currently tailored to Ubuntu Server 24+.

#### Role: deploy-rke2

Deploys RKE2 on a bare-metal cluster.  Alongside RKE2 this role will configure a virtual IP with `kube-vip` and a load balancer with `metallb`.

#### Role: rancher_install

Deploys Rancher for cluster management, along with the tooling required (Cert Manager and Traefik) for cluster ingress and ACME TLS certificates. The default is setup for Cloudflare's DNS-01 challenge, but it can be modified for your provider.  **Recommend the Cloudflare API Token be put in an ansible vault file (`ansible-vault create secrets.yaml`):
```
---
CF_TOKEN: "your_cloudflare_token_here"
```
Then place the token file in the `group_vars` in your inventory folder.  See the example playbook below.

## Installation

To install the collection from this repository, refer to [Installing a collection from a Git repository](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html).

```
ansible-galaxy collection install git+https://github.com/wolskies/rke2-ansible.git
```

See the Ansible documentation for more details on using collections.

### Basic Requirements

#### Hardware/Software

Host systems must meet the basic hardware/software requirements for RKE2 as outlined [here](https://docs.rke2.io/install/requirements).  This collection is written and tested on `amd64` systems, but should work for `arm64/aarch64`.  It is not intended to support Windows.

#### Kube VIP

Kube VIP needs to know the name of the primary ethernet interface.  The configuration file assumes it's `eth0`.  The best way is to change the name of the primary interface to `eth0` - that can be done in an Ubuntu environment via `/etc/netplan/50-cloud-init.yaml` like this:
```
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
      match:
        macaddress: <insert mac address of primary ethernet interface>
      set-name: eth0
```

#### Installation Notes
* Note 1:  The `deploy_rke2` role will fail if the host OS is not one of [RKE2's supported variants](https://www.suse.com/suse-rke2/support-matrix/all-supported-versions/rke2-v1-33/).  This behavior can be skipped by running the playbook with the `--skip-tags version-check` option.

* Note 2: **The RKE2 deploy role will remove NetworkManager if it is installed**.  There is a way to configure NetworkManager to coexist with Canal (default CNI), but I don't need it for my purposes. This behavior can be skipped using default vars, or by skipping the `config-firewall` tag.

* Note 3: **The RKE2 role will disable `firewalld` if it is installed**.  For the "why" see [RKE2 requirements](https://docs.rke2.io/install/requirements).  Canal can manage firewall rules after installation - see Note 5.  This behavior can be skipped by running the playbook with the `--skip-tags config-firewall` option.

* Note 4: If the firewall is set to UFW, the appropriate firewall rules will be installed, but UFW will be left in the state (enabled/disabled) that it was found in.

* Note 5: (Not Yet Implemented) If the firewall is set to Calico, a GlobalNetworkPolicy will be created and applied to each host.  This will allow RKE2 required communications, but effectively firewall all other incoming traffic to the cluster.

#### Inventory

Create the ansible inventory as you would normally do.  The controller nodes must be in the group "controllers" while the worker nodes must be in "agents".  The playbook should be relatively insensitive to host names, but I recommend a top-level group (I use `rke2`) to kick it off.  My typical inventory setup is:
```
rke2:
    children:
        controllers:
        agents:

controllers:
    hosts:
        kcontrol01:
            ansible_host: 192.168.10.1
        kcontrol02:
            ansible_host: 192.168.10.2
        kcontrol03:
            ansible_host: 192.168.10.3
agents:
    hosts:
        kworker01:
            ansible_host: 192.168.10.4
        kworker02:
            ansible_host: 192.168.10.5
```

## Usage

The role contains a sample playbook in the `playbooks` directory along with a sample `group_vars` to customize role defaults.  Assuming you have installed the role as a collection, a typical deployment playbook would look like:
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
      when: inventory_hostname == (groups['servers'] | first)
      become: false
```

## Support

Obviously happy to help with the role.  For Rancher, Traefik, etc, I recommend going to their sites.  I've put links to useful information where I've been able to find it.

## Roadmap

I am considering additional roles for services to deploy to the cluster including:
    - Postgres
    - ZenML Dashboard
    - MongoDB

## Authors and acknowledgment

It goes without saying that in the open-source community we all stand on the shoulders of giants.  This collection is both inspired by and leverages the great work of the following giants:
- James Turland (Jim's Garage) [RKE2](https://github.com/JamesTurland/JimsGarage/tree/main/Ansible/Playbooks/RKE2)
- Isaac Blum (Space Terran) [Automate Your RKE2 Cluster with Ansible: Helm, Cert-Manager, Traefik, and Rancher Setup Made Easy](https://github.com/SpaceTerran/ansible-rancher-traefik-ssl)

## License
GPL-3

## Project status

WIP