# Ubuntu

Ubuntu 18.04 is supported since Symplegma `v1.14.0`.
Here are sensible defaults variables to use when deploying on Ubuntu.

## Requirements

To be able to use Ansible, at least `python-minimal` or `python3-minimal`
must be installed.

## Directly without bastion host

```yaml
{!inventory/sample-ubuntu/group_vars/all/all.yml!}
```

## With bastion host

```yaml
{!inventory/sample-ubuntu-bastion/group_vars/all/all.yml!}
```
