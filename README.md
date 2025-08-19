## Ansible Collection: rke2_ansible

[![GitLab CI](https://img.shields.io/badge/GitLab%20CI-passed-brightgreen?logo=gitlab)](https://your-gitlab-instance.com/your-group/rke2-ansible/-/pipelines)

This collection includes a number of roles for the creation and management of an RKE2 cluster of bare-metal systems.

> **Note**: This is a synced repository. Primary development and CI/CD occurs on GitLab self-hosted. See [CI-CD.md](CI-CD.md) for details.

## Description

This collection automates the deployment and management of a bare-metal RKE2 cluster with Rancher for comprehensive cluster management through a web interface. The core workflow consists of three primary roles: `deploy_rke2` for cluster setup, `helm_install` for package management, and `rancher_install` for the management platform. Once Rancher is installed, additional charts and features are typically managed through the Rancher GUI.

For added convenience, optional storage roles (`longhorn_install` and `rook_install`) are included if you prefer automated storage deployment over managing through Rancher.

While it can be adapted to other distributions, it is currently tested and optimized for Ubuntu Server 20.04+, RHEL/Rocky/Oracle Linux 8.7+, SLES 15 SP3+, and Amazon Linux 2/2023. Both AMD64 and ARM64 architectures are supported.

## Core Roles

### deploy_rke2
Deploys RKE2 on a bare-metal cluster. Alongside RKE2 this role will configure a virtual IP with `kube-vip` and a load balancer with `MetalLB`. This forms the foundation of your Kubernetes cluster.

### helm_install
Installs Helm package manager and required dependencies for managing Kubernetes applications. Essential for Rancher installation and managing other Kubernetes workloads.

### rancher_install
Deploys Rancher for cluster management, along with the required tooling (Cert Manager and Traefik) for cluster ingress and ACME TLS certificates. Once installed, you'll manage additional charts and cluster features through the Rancher web interface.

The default setup uses Cloudflare's DNS-01 challenge, but can be modified for your provider. **Recommend storing the Cloudflare API Token in an ansible vault file (`ansible-vault create secrets.yaml`):
```yaml
---
CF_TOKEN: "your_cloudflare_token_here"
```
Place the encrypted token file in the `group_vars` in your inventory folder. The role automatically maps `CF_TOKEN` to `cf_token` for template usage.

## Optional Convenience Roles

These roles are provided for automated deployment, but you can also manage these components through the Rancher GUI after the core setup is complete:

### longhorn_install
Deploys Longhorn distributed block storage system for persistent volumes. Can alternatively be installed via Rancher's Apps & Marketplace.

### rook_install  
Deploys Rook-Ceph distributed storage system as an alternative to Longhorn. Can alternatively be installed via Rancher's Apps & Marketplace.

## Additional Roles

### rke2_upgrade
Upgrades RKE2 clusters following the official manual upgrade process. Safely upgrades control plane nodes first, then worker nodes with optional draining.

### mysql_operator
Deploys MySQL Operator for Kubernetes to manage MySQL database instances.

### teardown
Provides complete cleanup and removal of RKE2 clusters and all associated components.

## Installation

To install the collection from this repository, refer to [Installing a collection from a Git repository](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html).

```
ansible-galaxy collection install git+https://github.com/wolskinet/rke2-ansible.git
```

See the Ansible documentation for more details on using collections.

### Basic Requirements

#### Hardware/Software

Host systems must meet the basic hardware/software requirements for RKE2 as outlined [here](https://docs.rke2.io/install/requirements). This collection is tested on both `amd64` and `arm64/aarch64` architectures. It is not intended to support Windows.

**Supported Operating Systems:**
- Ubuntu Server 20.04, 22.04, 24.04, 25.04
- RHEL/Rocky/Oracle Linux 8.7, 8.8, 8.9, 9.1, 9.2, 9.3, 9.4, 9.5
- SUSE Linux Enterprise Server 15 SP3, SP4, SP5, SP6
- Amazon Linux 2, Amazon Linux 2023

#### Component Versions

| Component | Version | Purpose |
|-----------|---------|---------|
| RKE2 | v1.31.11+rke2r1 | Kubernetes distribution |
| Helm | v3.18.4 | Package manager |
| Kube-VIP | v0.9.1 | Virtual IP for HA |
| MetalLB | v0.15.2 | Load balancer |
| Cert-Manager | v1.18.2 | Certificate management |
| Traefik | v37.0.0 | Ingress controller |
| Rancher | v2.11.3 | Cluster management |
| Longhorn | v1.9.1 | Block storage |
| Rook-Ceph | v1.17.7 | Distributed storage |
| MySQL Operator | v8.4.3 | Database management |

#### Network Configuration

**Default Network Ranges** (customizable via variables):
- **Management Network**: `192.168.100.0/24`
- **Virtual IP (VIP)**: `192.168.100.30`
- **Load Balancer Range**: `192.168.100.240-192.168.100.254`
- **Primary Interface**: `eth0` (required for Kube-VIP)

**Required Ports** (automatically configured via UFW):
- **6443**: Kubernetes API server
- **9345**: RKE2 supervisor API
- **10250**: Kubelet API
- **2379-2381**: etcd client/peer communication
- **30000-32767**: NodePort services range

#### Kube VIP Interface Configuration

Kube VIP needs to know the name of the primary ethernet interface. The configuration file assumes it's `eth0`. The best way is to change the name of the primary interface to `eth0` - that can be done in an Ubuntu environment via `/etc/netplan/50-cloud-init.yaml` like this:
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

* Note 5: **ARM64 Version Compatibility**: When deploying on ARM64/aarch64 systems, verify that the specified RKE2 version has ARM64 container images available. If you encounter "image not found" errors during deployment, you can check image availability using:
  ```bash
  curl -s "https://registry.hub.docker.com/v2/repositories/rancher/rke2-runtime/tags/?page_size=100" | grep "v1.32.8"
  ```
  Look for entries containing "linux-arm64". If ARM64 images aren't available for your desired version, use a stable release like `v1.32.7+rke2r1` or `v1.31.11+rke2r1` which have confirmed ARM64 support.

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
            ansible_host: 192.168.100.11
        kcontrol02:
            ansible_host: 192.168.100.12
        kcontrol03:
            ansible_host: 192.168.100.13
agents:
    hosts:
        kworker01:
            ansible_host: 192.168.100.14
        kworker02:
            ansible_host: 192.168.100.15
```

## Security Considerations

⚠️ **Important**: This collection includes default credentials that **MUST** be changed for production deployments:

- **Cloudflare API Token**: Store in ansible vault file (see rancher_install role documentation)

**Best Practices:**
1. Use `ansible-vault` to encrypt sensitive variables
2. Change all default passwords before production deployment
3. Review and customize network ranges for your environment
4. Ensure proper firewall rules are configured (automatically handled via UFW)
5. Use strong TLS certificates (Let's Encrypt integration included)

## Usage

The collection contains a sample playbook in the `playbooks` directory along with sample `group_vars` to customize role defaults. 

### Recommended Workflow: Core Deployment with Rancher Management

This is the recommended approach - deploy the core infrastructure and then manage additional components through Rancher's GUI:

```yaml
---
- name: Deploy RKE2 Cluster with Rancher Management
  hosts: rke2
  vars_files:
    - /home/user/Ansible/inventory/group_vars/secrets.yaml
  become: false
  roles:
    # Install Helm on all nodes
    - role: wolskinet.rke2_ansible.helm_install
      become: false

    # Install RKE2 cluster on all nodes
    - role: wolskinet.rke2_ansible.deploy_rke2
      become: true

    # Install Rancher management platform (first controller only)
    - role: wolskinet.rke2_ansible.rancher_install
      when: inventory_hostname == (groups['controllers'] | first)
      become: false
      tags: rancher
```

After deployment, access Rancher at `https://rancher.yourdomain.com` and use the **Apps & Marketplace** to install:
- Longhorn (Storage)
- Prometheus + Grafana (Monitoring)
- Additional applications as needed

### Alternative: Full Automated Deployment

If you prefer to deploy storage automatically via Ansible (instead of through Rancher GUI):

```yaml
---
- name: Deploy RKE2 Cluster with Automated Storage
  hosts: rke2
  vars_files:
    - /home/user/Ansible/inventory/group_vars/secrets.yaml
  become: false
  roles:
    # Core components
    - role: wolskinet.rke2_ansible.helm_install
      become: false
    - role: wolskinet.rke2_ansible.deploy_rke2
      become: true
    - role: wolskinet.rke2_ansible.rancher_install
      when: inventory_hostname == (groups['controllers'] | first)
      become: false
      tags: rancher

    # Optional: Automated storage deployment (choose ONE)
    # Longhorn - distributed block storage
    - role: wolskinet.rke2_ansible.longhorn_install
      when: inventory_hostname == (groups['controllers'] | first)
      become: false
      tags: longhorn
      
    # OR Rook/Ceph - distributed storage alternative
    # - role: wolskinet.rke2_ansible.rook_install
    #   when: inventory_hostname == (groups['controllers'] | first)
    #   become: false
    #   tags: rook
```

### Minimal Deployment (RKE2 only)
```yaml
---
- name: Deploy Minimal RKE2 Cluster
  hosts: rke2
  become: false
  roles:
    - role: wolskinet.rke2_ansible.helm_install
    - role: wolskinet.rke2_ansible.deploy_rke2
      become: true
```

## Troubleshooting

### Common Issues

**Network Configuration:**
- Ensure VIP (`192.168.100.30`) is not already in use
- Verify primary interface is named `eth0` or update `vip_interface` variable
- Check that load balancer range doesn't conflict with existing IPs

**Firewall Issues:**
- UFW rules are automatically configured, but verify no conflicting rules exist
- If using a different firewall, disable it or configure RKE2 ports manually
- NetworkManager conflicts with Canal CNI - role removes it by default

**Storage Problems:**
- Only deploy one storage solution (Longhorn OR Rook for block storage)
- Ensure nodes have sufficient disk space (Rook requires 5Ti minimum device capacity)
- Verify storage classes are created properly after deployment

**Certificate Issues:**
- Cloudflare API token must be valid and have DNS edit permissions
- Check cert-manager logs if certificates fail to issue
- Verify domain configuration matches `traefik_domain` variable

### Getting Help

- Check role-specific README files for detailed configuration options
- Review logs: `kubectl logs -n <namespace> <pod-name>`
- For RKE2 issues, see [official documentation](https://docs.rke2.io)
- For component-specific issues (Rancher, Traefik, etc.), refer to their official documentation

## Support

Happy to help with the collection. For component-specific issues (Rancher, Traefik, etc.), I recommend referring to their official documentation. Links to useful information are provided where available.

## Roadmap

### Current Features ✅
- ✅ RKE2 cluster deployment with HA
- ✅ Multiple storage solutions (Longhorn, Rook/Ceph)
- ✅ MySQL Operator for database management
- ✅ Rancher management platform
- ✅ Complete teardown capabilities

### Future Enhancements 🚧
- **Additional Database Operators**: PostgreSQL, MongoDB operators
- **Monitoring Stack**: Prometheus, Grafana, AlertManager
- **Service Mesh**: Istio or Linkerd integration  
- **Backup Solutions**: Velero for cluster backups
- **Security Enhancements**: Pod Security Standards, Network Policies
- **Additional CNI Options**: Cilium, Calico support
- **GitOps Integration**: ArgoCD or Flux deployment

## Authors and acknowledgment

It goes without saying that in the open-source community we all stand on the shoulders of giants.  This collection is both inspired by and leverages the great work of the following giants:
- James Turland (Jim's Garage) [RKE2](https://github.com/JamesTurland/JimsGarage/tree/main/Ansible/Playbooks/RKE2)
- Isaac Blum (Space Terran) [Automate Your RKE2 Cluster with Ansible: Helm, Cert-Manager, Traefik, and Rancher Setup Made Easy](https://github.com/SpaceTerran/ansible-rancher-traefik-ssl)

## License
GPL-3

## Project status

WIP