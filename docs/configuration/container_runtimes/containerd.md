# Containerd

Containerd 2.3.5 is the default runtime. The generated config uses version 4,
the `io.containerd.cri.v1.runtime` plugin, and the runc v2 shim. runc remains the
default OCI runtime. The sandbox image matches Kubernetes 1.37's pause image.

Systemd cgroups and cgroup v2 are required for the current stack:

```yaml
container_runtime: containerd
systemd_cgroup: true
```

Do not switch cgroup drivers on an existing node. Replace legacy cgroupfs nodes
with nodes configured for cgroup v2 and systemd before moving to this stack.
The role chooses amd64 or arm64 downloads from the host facts and verifies the
upstream checksums. `containerd_config` remains available for custom TOML.

## crun support (unreleased)

The locally prepared containerd role adds crun 1.29.1 alongside runc, with
checksum-verified binaries and separate runtime handlers. This is not yet in
the role release pinned by `requirements.yml` or the Blackwell upgrade checkout.
After publishing and installing that role release, select it with:

```yaml
container_runtime: containerd
containerd_default_runtime: crun
systemd_cgroup: true
```

`io.containerd.runc.v2` remains the correct shim type for both executables;
the `crun` handler's `BinaryName` points to crun. The `runc` handler is preserved.
If you override `containerd_config`, configure both handlers and the default
selection in that custom TOML yourself.

First test an explicitly selected pod using this RuntimeClass while keeping
the node default on runc:

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: crun
handler: crun
```

Set `spec.runtimeClassName: crun` on the test pod. This role does not create
RuntimeClass resources or recreate application pods. A default change triggers
the normal containerd restart handler; plan that and subsequent workload
recreation separately from Kubernetes upgrades. Keep both runtimes installed.

crun reports lower startup overhead in its own benchmarks, not a general
application-performance improvement. We retain containerd's upstream runc
default until crun has been tested against the intended workloads. CRI-O already
uses crun by default (`crio_use_crun: true`).

References: [containerd runtime configuration](https://github.com/containerd/containerd/blob/v2.3.5/docs/cri/config.md),
[crun performance](https://github.com/containers/crun#performance).
