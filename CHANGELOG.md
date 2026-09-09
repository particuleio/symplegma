# Changelog

## v3.0.0 — Linux modernization and sequential upgrades

This is a breaking refresh of v2.0.0, the Kubernetes 1.24-era release.
Release preparation date: 2026-09-09.

### Breaking changes

- Retire Windows workers and their roles. Inventories must be Linux-only.
- Require Ansible 14 / ansible-core 2.21 and Python 3.12–3.14 on the controller.
  The repository selects Python 3.14.7 through uv.
- Target amd64/arm64 Linux hosts with cgroup v2 and systemd cgroups; review
  existing hosts before using the refreshed roles. Do not change the cgroup
  driver on an existing node as part of this upgrade.
- Move kubeadm configuration to v1beta4 and containerd configuration to v4.
  Review custom templates and overrides. The containerd role requires 2.3+.
- Remove legacy OpenStack provisioning and refresh the AWS examples.
- Install networking providers other than Flannel independently. Existing CNI,
  storage and admission-webhook compatibility remains the operator's responsibility.

### Component baseline

- Kubernetes, kubeadm, kubelet and kubectl: 1.37.0.
- containerd: 2.3.5; runc: 1.5.1 (the default OCI runtime for containerd).
  Install crun 1.29.1 alongside it and opt in using `containerd_default_runtime: crun`.
- Optional CRI-O: 1.36.5 with crun 1.29.1; pair it with Kubernetes 1.36.4.
- CNI plugins: 1.9.1; Flannel: 0.28.9; crictl follows the target Kubernetes minor.
- Ansible: 14.3.1; ansible-core: 2.21.3; controller Python: 3.14.7.
- Host tools include etcd 3.7.1 and jq 1.8.2. Kubeadm selects the cluster's etcd,
  CoreDNS and kube-proxy images; host-tool pins do not override those images.

### Upgrade fixes

- Validate Kubernetes minor-version skew, runtime upgrade paths and cgroup
  prerequisites before changing nodes. Accept containerd 1.7/2.0 LTS to 2.3 LTS
  migrations as well as sequential minor transitions; runtime deprecations and
  configuration compatibility still need review.
- Upgrade kubeadm and the control plane before installing the target kubelet.
- Require the target kubelet version and Ready node condition, then check API
  `/readyz`. Retry transient API failures with bounded requests instead of
  trusting a previously reported Ready condition during restarts.
- Retry uncordon in the normal drain-based workflow.
- Add explicit `upgrade_skip_drain=true` for accepted in-place upgrades. It skips
  both drain and uncordon, leaving scheduling state unchanged. Restarts can still
  interrupt workloads; this differs from Kubernetes' documented drain procedure.
- Keep emptyDir deletion opt-in using `upgrade_drain_delete_emptydir_data=true`.
  The drain workflow does not bypass PodDisruptionBudgets.
- Remove the manual `upgrade_backup_confirmed` and `upgrade_maintenance_confirmed`
  gates: these were acknowledgements, not verification. Backups and an approved
  maintenance window remain essential.
- Replace `upgrade_ready_timeout` with 30 retries, a 5-second delay and a
  10-second request timeout for each final API operation.
- Avoid the macOS Ansible worker crash caused by fork-unsafe system proxy
  discovery: mise sets `no_proxy=*` on macOS only. This bypasses HTTP proxies in
  the project environment, not TLS verification, and does not affect managed nodes.

### Tooling and validation

- Use mise, uv and just for pinned tools, locked Python dependencies and common
  development commands; no virtualenv activation is required.
- Modernize CI with SHA-pinned actions, limited permissions and Python
  3.12/3.13/3.14 validation. Publish documentation through GitHub Pages artifacts
  and OIDC.
- Add pre-commit checks including ansible-lint, ShellCheck, actionlint, zizmor,
  Ruff, file hygiene and rendered-configuration tests.
- Verify downloads and published role revisions; preserve existing mismatched
  role checkouts instead of silently overwriting them.
- Add regression tests for runtime transitions, drain options and readiness.
  These checks are not a full-cluster conformance certification.
- Verify containerd and CRI-O installation, OCI binaries and effective
  configuration in disposable Ubuntu 24.04 containers. CRI-O now interprets
  string boolean overrides such as `crio_use_crun=false` correctly.

### Pinned role releases

| Role | Release |
| --- | --- |
| symplegma-os_bootstrap | v2.0.0 |
| symplegma-kubernetes_hosts | v1.37.0-rel.0 |
| symplegma-kubeadm | v1.37.0-rel.0 |
| symplegma-containerd | v2.3.5-rel.1 |
| symplegma-crio | v1.36.5-rel.1 |
| symplegma-cni | v1.9.1-rel.0 |
| symplegma-flannel | v0.28.9-rel.0 |

Optional containerd/crun support is included, but runc remains containerd's
default. This release does not switch Blackwell to crun or CRI-O.

### Migration notes

Do not apply the 1.37 defaults directly to a 1.24 or 1.32 cluster. Upgrade one
minor at a time, confirming API, node, network, storage and workload health after
each step. From 1.32 the prepared sequence is 1.33.13 → 1.34.11 → 1.35.8 →
1.36.4 → 1.37.0. Older end-of-life releases are transition steps, not destinations.

Keep `kubeadm_version: "{{ kubernetes_version }}"` in inventory and override
`kubernetes_version` for each step. Do not rerun initialization against an old
inventory version after upgrading; reconcile the inventory with the final version.
Back up etcd, application volumes and runtime configuration before starting.

See [maintenance and upgrade guidance](docs/maintaining.md) and the upstream
[kubeadm upgrade guide](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/).

## Earlier releases

Historical notes are available in the
[GitHub releases](https://github.com/particuleio/symplegma/releases).
