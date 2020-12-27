# Containerd

Symplegma supports `containerd` out of the box with no extra configuration. It
is the default runtime.

## Cgroup configuration

To ensure compatibility with older cluster, containerd use `cgroupfs` as default
cgroup. To enable `systemd` with cgroupv2 on new cluster, simply toggle the variable in
`group_vars`:

```yaml
systemd_cgroup: true
```
