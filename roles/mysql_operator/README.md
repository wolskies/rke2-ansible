# MySQL Operator Role

This role deploys the MySQL Operator for Kubernetes on an existing RKE2 cluster. The MySQL Operator enables easy deployment and management of MySQL databases in Kubernetes.

## Requirements

- Ansible 2.12 or later
- kubernetes.core ansible collection
- Running RKE2 cluster (see `wolskinet.rke2_ansible.deploy_rke2`)
- Helm 3.x installed (see `wolskinet.rke2_ansible.helm_install`)

## Role Variables

### General Configuration
```yaml
home_path: /home/{{ ansible_user }}
traefik_domain: example
kubectl_config: "{{ home_path }}/.kube/config"
```

### MySQL Operator Configuration
```yaml
mysql_operator_chart_ref: mysql-operator/mysql-operator
mysql_operator_chart_version: "8.4.3"
mysql_operator_path: "{{ home_path }}/mysql-operator"
```

### Component Installation Controls
```yaml
mysql_install_operator: true
```

## Tags

The role provides the following tags for selective execution:

- `database-mysql` - All MySQL operator components
- `mysql_operator` - MySQL operator deployment

## Dependencies

- `wolskinet.rke2_ansible.helm_install` - Helm must be installed
- `wolskinet.rke2_ansible.deploy_rke2` - RKE2 cluster must be running

## Example Playbook

```yaml
---
- name: Deploy MySQL Operator on RKE2
  hosts: controllers
  become: false
  roles:
    - name: wolskinet.rke2_ansible.mysql_operator
      when: inventory_hostname == (groups['controllers'] | first)
```

### Selective Installation Examples

```bash
# Install MySQL operator
ansible-playbook mysql-operator.yaml --tags "mysql-operator"

# Skip MySQL operator installation
ansible-playbook site.yaml --skip-tags "database-mysql"
```

## Usage After Installation

After the MySQL operator is installed, you can create MySQL instances using custom resources:

```yaml
apiVersion: mysql.oracle.com/v2
kind: InnoDBCluster
metadata:
  name: mycluster
  namespace: default
spec:
  secretName: mypwds
  tlsUseSelfSigned: true
  instances: 3
  router:
    instances: 1
```

## Security Considerations

- The operator manages MySQL credentials through Kubernetes secrets
- Configure appropriate RBAC policies for MySQL resources
- Use TLS encryption for MySQL connections in production
- Regularly update the operator to receive security patches

## License

GPL-3.0-or-later

## Author Information

Ed Wolski  
wolskinet