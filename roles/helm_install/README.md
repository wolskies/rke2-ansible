Role Name
=========

A straightforward role to install Helm package manager via the `get-helm-3.sh` script, and helm-diff

Requirements
------------

See https://helm.sh/docs/helm/helm_install/

While the role itself doesn't require the python3-kubernetes package, using the role later requires it to be installed.  Therefore the role installs that package also.

Role Variables
--------------

There are no variables that may be changed in the role.  The following variables are used:

 - `ansible_user_id` - used to set ownership of files
 - `ansible_user_dir` - used to set location of `.local/share` file paths

Dependencies
------------

None


