# Containerd

Containerd 2.3.5 is the default runtime. The generated config uses version 4,
the `io.containerd.cri.v1.runtime` plugin, the runc v2 shim, and the separately
pinned runc binary. The sandbox image matches Kubernetes 1.37's pause image.

Systemd cgroups and cgroup v2 are required for the current stack:

```yaml
container_runtime: containerd
systemd_cgroup: true
```

Do not switch cgroup drivers on an existing node. Replace legacy cgroupfs nodes
with nodes configured for cgroup v2 and systemd before moving to this stack.
The role chooses amd64 or arm64 downloads from the host facts and verifies the
upstream checksums. `containerd_config` remains available for custom TOML.
