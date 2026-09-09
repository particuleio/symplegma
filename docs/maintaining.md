# Maintenance and validation

The release inventory was checked against upstream metadata on 2026-09-08.

| Component | Pin | Upstream |
| --- | --- | --- |
| Ansible / ansible-core | 14.3.1 / 2.21.3 | [PyPI](https://pypi.org/project/ansible/) |
| Kubernetes, kubeadm, kubelet, kubectl | 1.37.0 | [Kubernetes releases](https://kubernetes.io/releases/) |
| containerd | 2.3.5 | [Releases](https://github.com/containerd/containerd/releases) |
| CRI-O | 1.36.5 | [Releases](https://github.com/cri-o/cri-o/releases) |
| runc | 1.5.1 | [Releases](https://github.com/opencontainers/runc/releases) |
| crun | 1.29.1 | [Releases](https://github.com/containers/crun/releases) |
| CNI plugins | 1.9.1 | [Releases](https://github.com/containernetworking/plugins/releases) |
| crictl | 1.37.0 | [Releases](https://github.com/kubernetes-sigs/cri-tools/releases) |
| Flannel / Flannel CNI | 0.28.9 / 1.9.1-flannel3 | [Releases](https://github.com/flannel-io/flannel/releases) |
| etcd host tools | 3.7.1 | [Releases](https://github.com/etcd-io/etcd/releases) |
| jq | 1.8.2 | [Releases](https://github.com/jqlang/jq/releases) |
| Flatcar bootstrap Python | 3.14.7, build 20260901 | [Releases](https://github.com/astral-sh/python-build-standalone/releases) |
| Worker API proxy NGINX | 1.31.5-alpine | [NGINX downloads](https://nginx.org/en/download.html) |

Kubeadm selects the supported etcd server, CoreDNS and kube-proxy images. Host
tool versions do not override those images. CRI-O follows Kubernetes minor
versions; the available 1.36.5 release is paired with Kubernetes 1.36.4. Containerd
is the default for Kubernetes 1.37.

## Working on roles

Install [mise](https://mise.jdx.dev/), then run:

```sh
mise install
just setup
just check
```

`requirements.yml` pins published role releases. The installer verifies the
selected revision and refuses to overwrite a mismatched checkout. No patch
overlay is needed. `requirements-main.yml` is for upstream role development.

Mise pins uv, Node and just. uv manages Python from `.python-version` and dependencies
from `pyproject.toml` / `uv.lock`. Use `uv sync --locked --all-groups` and
`uv run --locked ...` if you do not use mise. The `pre-commit-uv` integration uses
uv to create the Python hook environments as well.

Renovate updates role releases, Python dependencies, pre-commit hooks, action
digests and annotated component versions. Coordinate Kubernetes and CRI-O minor
versions, and update binary checksums when changing crun or bootstrap Python.

## Checks

Pre-commit runs file hygiene checks, YAML/JSON/TOML validation, private-key
detection, Ruff, ShellCheck, actionlint, zizmor, ansible-lint and the configuration
tests. CI also checks every playbook against both example inventories on Python
3.12, 3.13 and 3.14. The render tests exercise Ansible's current templating engine,
kubeadm v1beta4, both container runtimes, both architectures and both Flannel
backends.

The OS bootstrap (including Python 3.14.7), Kubernetes binaries, CNI and containerd
Molecule scenarios also pass in disposable Ubuntu 24.04 arm64 containers. CI
runs them on Ubuntu 24.04 amd64 runners. Containerd's real binary validates
native v4 configuration without automatic migration. Kernel modules/sysctls/swap
are excluded from shared-kernel container tests.

These checks do not replace booting disposable Ubuntu and Flatcar clusters.
Before deploying these changes to an existing cluster, test init, repeat init, worker join, HA control
plane replacement, a supported single-minor upgrade, and reset on each runtime.
Respect disruption budgets and investigate a failed upgrade while its node
remains cordoned.

## GitHub Pages

The documentation workflow builds every pull request with `mkdocs build --strict`.
Only the main branch can deploy. Publishing uses the official Pages artifact and
OIDC deployment actions, with write permissions limited to the deployment job.
In repository Settings → Pages, select **GitHub Actions** as the publishing
source when migrating from the former gh-pages branch workflow.

## Role releases

Role releases are signed/tagged from published commits after validation.
The selected releases are listed in `requirements.yml`; changelogs live in
each role repository. Never advance a requirement to a tag that does not exist.

## Sequential Kubernetes upgrades

Skipping Kubernetes minor versions is unsupported. To reach 1.37 from 1.32,
use 1.32 → 1.33 → 1.34 → 1.35 → 1.36 → 1.37, checking health after each step.
The current patch targets (checked 2026-09-09) are 1.32.13, 1.33.13, 1.34.11,
1.35.8, 1.36.4 and 1.37.0. Kubernetes 1.32 and 1.33 are end-of-life, so use them only as
necessary transition steps. See the [kubeadm upgrade guide](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/).

Before applying an upgrade, run the read-only checks:

```sh
just upgrade-check YOUR_INVENTORY v1.33.13
```

This uses SSH and the existing cluster API but does not drain or modify nodes.
It checks Kubernetes minor skew, cgroup v2 and the containerd upgrade path.
Containerd allows sequential minor upgrades and sequential LTS migrations. The
preflight accepts 1.7 or 2.0 LTS → 2.3 LTS; review deprecations, back up runtime
configuration, and inspect [its release policy](https://containerd.io/releases/).
The latest role's native v4 config requires containerd 2.3; older runtime
transition steps need a matching config and must be handled separately.

Also inspect the installed CNI, CSI/storage, admission webhooks, PDBs, kernel
and OS compatibility. Confirm a recoverable etcd snapshot, application-volume
backups, and a maintenance window. The former `upgrade_backup_confirmed` and
`upgrade_maintenance_confirmed` flags only acknowledged these steps; they never
verified a snapshot or a maintenance window and are no longer required.
A single control-plane node has API downtime; workloads without another node
cannot be rescheduled while it is drained. The playbook does not bypass PDBs
and refuses to discard emptyDir data by default.

If drain reports pods with local storage, inspect their emptyDir volumes first.
To explicitly accept permanent deletion of their contents, add
`-e upgrade_drain_delete_emptydir_data=true` to the full upgrade command.
This does not delete PVCs or hostPath directories and does not bypass PDBs.
On a failed upgrade the node stays cordoned; resolve the failure before retrying.

For an explicitly accepted in-place upgrade, add `-e upgrade_skip_drain=true`.
This skips both drain and uncordon, leaving scheduling state unchanged. Runtime,
CNI, Kubernetes and readiness checks still run. It does not cordon or evict
workloads. This departs from the documented drain-based Kubernetes procedure;
runtime and kubelet restarts can still interrupt workloads. Drain remains
enabled by default. If an earlier attempt already cordoned the node, restore its
scheduling explicitly with `kubectl uncordon NODE` once the API is healthy.

After kubelet changes, the playbook checks both the target kubelet version and
the node's Ready condition, then the API's `/readyz` endpoint. These checks and
the normal drain-mode uncordon retry transient API failures (30 retries with a
5-second delay and a 10-second request timeout). A previously reported Ready
condition alone is insufficient while static control-plane pods restart.

Keep `kubeadm_version: "{{ kubernetes_version }}"` in inventory so each minor step
only needs one version override. There is no need to pass `containerd_version`
when the installed runtime already matches the pinned role default. For a
single-node inventory with accepted in-place upgrades, store
`upgrade_skip_drain: true` in its group variables rather than repeating the flag.

`just validate-kubeadm v1.33.13 v1.34.11 v1.35.8 v1.36.4 v1.37.0` validates generated
configuration offline with each actual target binary; it is not a live-cluster
compatibility certificate.

The former Windows CNI, Kubernetes-hosts and Docker repositories are archived
and no longer appear in either requirements file.

On macOS, Ansible's URL lookup can trigger an Objective-C fork error while Python
discovers system proxy settings. The repository's `mise.toml` sets `no_proxy=*`
on macOS, so `mise exec -- ...` and the just recipes avoid that native lookup.
Other operating systems retain their existing proxy exclusions. This bypasses
HTTP proxies for commands in this project's mise environment, not TLS certificate
verification; it does not change global shell settings or the managed node.
See the [Python urllib warning](https://docs.python.org/3.14/library/urllib.request.html).
