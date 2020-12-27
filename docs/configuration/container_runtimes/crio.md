# Cri-o

Symplegma supports cri-o out of the box. To switch from containerd to cri-o,
toggle the variables in `group_vars`:

```yaml
systemd_cgroup: true
container_runtime: crio
```

> :warning: **You must turn on systemd_cgroup in order to use cri-o**
