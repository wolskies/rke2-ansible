# Helm Install Role

A straightforward role to install Helm package manager via the `get-helm-3.sh` script, helm-diff plugin, and the python3-kubernetes library required by other roles that use kubernetes.core modules. The python3-kubernetes library is only installed on controller nodes to optimize deployment efficiency.

## Requirements

See https://helm.sh/docs/helm/helm_install/

While the role itself doesn't require the python3-kubernetes package, using the role later requires it to be installed. Therefore the role installs that package also.

## Role Variables

There are no configurable variables for this role. The following variables are used internally:

- `ansible_user_id` - used to set ownership of files
- `ansible_user_dir` - used to set location of `.local/share` file paths

The role uses the following default versions:

```yaml
helm_version: "v3.18.4"
```

## Dependencies

None

## Example Playbook

```yaml
---
- name: Install Helm package manager
  hosts: controllers
  become: true
  gather_facts: true
  roles:
    - wolskinet.rke2_ansible.helm_install
```

## Tags

- `helm`: Run the complete helm installation

## License

GPL-3.0-or-later

## Author Information

Ed Wolski / wolskinet