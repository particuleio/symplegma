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

Skipping Kubernetes minor versions is unsupported. To reach 1.36 from 1.32,
use 1.32 → 1.33 → 1.34 → 1.35 → 1.36, checking health after each step.
The current patch targets (checked 2026-09-09) are 1.32.13, 1.33.13, 1.34.11,
1.35.8 and 1.36.4. Kubernetes 1.32 and 1.33 are end-of-life, so use them only as
necessary transition steps. See the [kubeadm upgrade guide](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/).

Before applying an upgrade, run the read-only checks:

```sh
just upgrade-check YOUR_INVENTORY v1.33.13
```

This uses SSH and the existing cluster API but does not drain or modify nodes.
It checks Kubernetes minor skew, cgroup v2 and the containerd upgrade path.
Containerd also requires sequential minor upgrades, with a documented exception
for 1.7 LTS → 2.3 LTS; inspect [its release policy](https://containerd.io/releases/).
The latest role's native v4 config requires containerd 2.3; older runtime
transition steps need a matching config and must be handled separately.

Also inspect the installed CNI, CSI/storage, admission webhooks, PDBs, kernel
and OS compatibility. Confirm a recoverable etcd snapshot, application-volume
backups, and a maintenance window. Full upgrade execution requires explicit
`upgrade_backup_confirmed=true` and `upgrade_maintenance_confirmed=true`.
A single control-plane node has API downtime; workloads without another node
cannot be rescheduled while it is drained. The playbook does not bypass PDBs
or discard emptyDir data.

`just validate-kubeadm v1.33.13 v1.34.11 v1.35.8 v1.36.4` validates generated
configuration offline with each actual target binary; it is not a live-cluster
compatibility certificate.

The former Windows CNI, Kubernetes-hosts and Docker repositories are archived
and no longer appear in either requirements file.

On macOS, Ansible's URL lookup can trigger an Objective-C fork error.
For affected commands, prefix with `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`,
as described in the [Ansible FAQ](https://docs.ansible.com/projects/ansible-core/2.18/reference_appendices/faq.html#running-on-macos-as-a-control-node).
