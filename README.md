## Ansible Collection: rke2_ansible

This collection includes a number of roles for the creation and management of an RKE2 cluster of bare-metal systems.

## Description

This collection automates the deployment and management of a bare-metal RKE2 cluster.  It includes roles to install Metallb, Traefik, Cert-Manager, Rancher and Longhorn.  While it can be adapted to other distributions, it is currently tailored to Ubuntu Server 24+

## Installation

To install the collection from this repository, refer to [Installing a collection from a Git repository](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html).  

```
ansible-galaxy collection install git+https://github.com/wolskies/rke2-ansible.git
```

See the Ansible documentation for more details on using collections.

### Basic Requirements

Host systems must meet the basic hardware/software requirements for RKE2 as outlined [here](https://docs.rke2.io/install/requirements).  This collection is written and tested on `amd64` systems, but should work for `arm64/aarch64`.  It is not intended to support Windows.

* Note 1:  The RKE2 deploy role will fail if the host OS is not one of [RKE2's supported variants](https://www.suse.com/suse-rke2/support-matrix/all-supported-versions/rke2-v1-33/).  This behavior can be changed by modifying the default vars for the `deploy-rke2-cluster` role.*

* Note 2: The RKE2 deploy role will remove NetworkManager if it is installed, and disable `firewalld` if it is installed.  Details are in the RKE2 requirements.  UFW will have the appropriate firewall rules included, but will be left in the state (enabled/disabled) that it was found in.*

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

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
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

