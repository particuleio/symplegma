# Flatcar

Here are sensible defaults variables to use when deploying
on Flatcar.

## Requirements

Set `bootstrap_python: true` to install checksum-verified CPython 3.14.7 from
[python-build-standalone](https://github.com/astral-sh/python-build-standalone).
The bootstrap runs before fact gathering, supports amd64 and arm64, and selects
`/opt/bin/python`. It replaces the obsolete Python 3.6 / PyPy bootstrap.
Use a current Flatcar stable image with cgroup v2.

## Sample configuration

```yaml
{!inventory/flatcar/group_vars/all/all.yml!}
```
