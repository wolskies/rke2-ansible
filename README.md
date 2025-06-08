## Ansible Collection: rke2_ansible

This collection includes a number of roles for the creation and management of an RKE2 cluster of bare-metal systems.

## Description

This collection automates the deployment and management of a bare-metal RKE2 cluster.  It includes roles to install Metallb, Traefik, Cert-Manager, Rancher and Longhorn.  While it can be adapted to other distributions, it is currently tailored to Ubuntu Server 24+.

## Installation

To install the collection from this repository, refer to [Installing a collection from a Git repository](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html).  

```
ansible-galaxy collection install git+https://github.com/wolskies/rke2-ansible.git
```

See the Ansible documentation for more details on using collections.

### Basic Requirements

Host systems must meet the basic hardware/software requirements for RKE2 as outlined [here](https://docs.rke2.io/install/requirements).  This collection is written and tested on `amd64` systems, but should work for `arm64/aarch64`.  It is not intended to support Windows.

* Note 1:  The RKE2 deploy role will fail if the host OS is not one of [RKE2's supported variants](https://www.suse.com/suse-rke2/support-matrix/all-supported-versions/rke2-v1-33/).  This behavior can be changed by modifying the default vars for the `deploy-rke2-cluster` role.

* Note 2: The RKE2 deploy role will remove NetworkManager if it is installed.  There is a way to configure NetworkManager to coexist with Canal (default CNI), but I don't need it for my purposes.

* Note 3: The RKE2 role will disable `firewalld` if it is installed.  For the "why" see [RKE2 requirements](https://docs.rke2.io/install/requirements).  There is an option to configure UFW or leverage Calico (part of the default Canal CNI) as a firewall.  

* Note 4: If the firewall is set to UFW, the appropriate firewall rules will be installed, but UFW will be left in the state (enabled/disabled) that it was found in.

* Note 5: If the firewall is set to Calico, a GlobalNetworkPolicy will be created and applied to each host.  This will allow RKE2 required communications, but effectively firewall all other incoming traffic to the cluster. (TBD)

### Inventory

Create the ansible inventory as you would normally do.  The controller nodes must be in the group "servers" while the worker nodes must be in "agents".  My typical inventory setup is:
```
RKE2:
    children:
        servers:
        agents:

servers:
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
    - RKE2
  become: true
  collections:
    - wolskinet.rke2_ansible
  tasks:
    - name: Import roles
      ansible.builtin.import_role:
        name: wolskinet.rke2_ansible.deploy_rke2
```

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap

I am considering additional roles for services to deploy to the cluster including:
    - Postgres
    - ZenML Dashboard
    - MongoDB

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

## Authors and acknowledgment
It goes without saying that in the open-source community we all stand on the shoulders of giants.  This collection is both inspired by and leverages the great work of the following giants:
- James Turland (Jim's Garage) [RKE2](https://github.com/JamesTurland/JimsGarage/tree/main/Ansible/Playbooks/RKE2)
- Isaac Blum (Space Terran) [Automate Your RKE2 Cluster with Ansible: Helm, Cert-Manager, Traefik, and Rancher Setup Made Easy](https://github.com/SpaceTerran/ansible-rancher-traefik-ssl)

## License
GPL-3

## Project status


