# CRI-O

The newest published stable CRI-O release is 1.36.5. CRI-O and Kubernetes should
use the same minor release, so configure the current CRI-O stack as follows:

```yaml
container_runtime: crio
kubernetes_version: v1.36.4
kubeadm_version: "{{ kubernetes_version }}"
crio_version: v1.36.5
systemd_cgroup: true
crio_use_crun: true
```

Use containerd for Kubernetes 1.37 until CRI-O publishes a matching release.
Preflight checks reject mismatched minor versions before changing a host.

The role verifies the CRI-O bundle, uses its companion conmon, conmonrs and pinns,
and installs independently pinned runc 1.5.1 and crun 1.29.1. Set
`crio_use_crun: false` to select runc. The Kubernetes hosts role owns crictl,
so the bundled copy does not replace the selected crictl version.

When overriding `crun_version`, also supply `crun_checksum` for the selected
architecture from the upstream release metadata. Both runtimes use systemd
cgroups by default. Existing nodes must not switch cgroup drivers in place.
