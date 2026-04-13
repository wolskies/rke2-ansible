# longhorn_install

Deploy Longhorn distributed block storage on an existing RKE2 cluster.

## What it does

- Adds the `longhorn-stable` Helm repository.
- Creates the `longhorn-system` namespace.
- Installs Longhorn from its Helm chart and waits for readiness.

Run from the first controller: `when: inventory_hostname == groups['controllers'][0]`.

## Requirements

- Running RKE2 cluster (`deploy_rke2`) and Helm (`helm_install`).
- Nodes must satisfy the [Longhorn prerequisites](https://longhorn.io/docs/latest/deploy/install/#installation-requirements): `open-iscsi`, `nfs-common`, a filesystem that supports `fiemap`, etc.

## Usage

```yaml
- hosts: rke2
  roles:
    - role: wolskinet.rke2_ansible.longhorn_install
      when: inventory_hostname == groups['controllers'][0]
```

## Tags

`longhorn`, `storage-longhorn`.

## Variables

See [`docs/variables.md`](../../docs/variables.md). Key settings: `longhorn_chart_version`, `longhorn_namespace`, `longhorn_replica_count`, `longhorn_storage_class_name`.
