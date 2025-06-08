## Ansible Collection: rke2_ansible
This collection includes a number of roles for the creation and management of an RKE2 cluster.

## Description
This collection automates the deployment and management of a bare-metal RKE2 cluster.  It includes roles to install Metallb, Traefik, Cert-Manager, Rancher and Longhorn.  

## Installation
To install the collection from this repository, refer to [Installing a collection from a Git repository](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html).  

```
ansible-galaxy collection install git+https://github.com/wolskies/rke2-ansible.git
```

See the Ansible documentation for more details.  

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
It goes without saying that in the open-source community we all stand on the shoulders of giants.  This collection is both inspired by and leverages the great work of the following giants:
- James Turland (Jim's Garage) [RKE2](https://github.com/JamesTurland/JimsGarage/tree/main/Ansible/Playbooks/RKE2)
- Isaac Blum (Space Terran) [Automate Your RKE2 Cluster with Ansible: Helm, Cert-Manager, Traefik, and Rancher Setup Made Easy](https://github.com/SpaceTerran/ansible-rancher-traefik-ssl)

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

