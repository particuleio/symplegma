# CoreOS / Container Linux OS

Here are sensible defaults variables to use when deploying
on CoreOS / Container Linux OS.

## Requirements

Python on CoreOS is automaticaly bootstrap with a portable
[Pypy](https://github.com/squeaky-pl/portable-pypy).

## Directly without bastion host

```yaml
{!inventory/sample-coreos/group_vars/all/all.yml!}
```

## With bastion host

```yaml
{!inventory/sample-coreos-bastion/group_vars/all/all.yml!}
```
