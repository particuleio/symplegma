# Symplegma

<p align="center">
  <img src="images/logo.png">
</p>

[![Documentation](https://github.com/particuleio/symplegma/actions/workflows/mkdocs.yml/badge.svg)](https://github.com/particuleio/symplegma/actions/workflows/mkdocs.yml)
[![CI](https://github.com/particuleio/symplegma/actions/workflows/ci.yml/badge.svg)](https://github.com/particuleio/symplegma/actions/workflows/ci.yml)

<p align="left">
<a href="https://github.com/cncf/k8s-conformance"><img src="https://github.com/cncf/artwork/raw/master/projects/kubernetes/certified-kubernetes/versionless/color/certified-kubernetes-color.png" alt="Certified Kubernetes" title="Certified Kubernetes" width=75 style="vertical-align:middle;margin:10px 20px" /></a>
<a href="https://landscape.cncf.io/format=card-mode&organization=particule&selected=symplegma"><img src="https://github.com/cncf/artwork/raw/master/other/cncf-landscape/stacked/color/cncf-landscape-stacked-color.png" alt="Certified Kubernetes" title="Certified Kubernetes" width=75 style="vertical-align:middle;margin:10px 20px" /></a>
</p>

Symplegma (from greek *σύμπλεγμα*) is a simple set of [Ansible](https://www.ansible.com/) playbooks to deploy [Kubernetes](https://kubernetes.io/) with [Kubeadm](https://kubernetes.io/docs/setup/independent/high-availability/). It is heavily inspired by [Kubespray](https://github.com/kubernetes-incubator/kubespray) and [OpenStack Ansible](https://docs.openstack.org/openstack-ansible/latest/).

Historical releases have [Kubernetes conformance results](https://github.com/cncf/k8s-conformance/tree/master/v1.20/symplegma). The refreshed stack has not yet been submitted for conformance certification.

The main goal is to be minimalist with sensible defaults.

Flannel is included. Install other cluster networking providers independently;
legacy Calico/operator roles are no longer part of the supported requirements.

## Deploys a Kubernetes cluster

- Deploys vanilla Kubernetes with Kubeadm.
- Targets current stable [Flatcar Linux](https://www.flatcar.org/) and Ubuntu 24.04 / 26.04, on amd64 and arm64 with cgroup v2.
- Requires Python 3.12 or newer on the Ansible controller.
- Windows workers are retired.
- Does not rely on Docker
- Uses CRI compatible runtime:
    - [containerd][cri-containerd] (default)
    - [cri-o][cri-crio]
- Does not depend on cloud provider
- Does not depend on primary master
- Dynamic config
- Pins component versions for reproducible installations

[cri-crio]: https://cri-o.io/
[cri-containerd]: https://github.com/containerd/containerd

## Install and validate

```sh
mise install
just setup
just check
```

Mise pins uv, Node and just; uv selects Python from `.python-version`, resolves the
Ansible/development/documentation groups in `pyproject.toml`, and reproduces them
from `uv.lock`. No virtualenv activation is needed. Without mise, use
`uv sync --locked --all-groups` and `uv run --locked` before each command.

The install script fetches the exact published roles in `requirements.yml`.
It preserves existing role checkouts and refuses mismatched revisions; no
local compatibility patches or virtualenv activation are needed.

The default stack is Kubernetes / kubeadm / kubelet / kubectl **1.37.0**,
containerd **2.3.5**, runc **1.5.1**, CNI plugins **1.9.1**, and crictl **1.37.0**.
CRI-O **1.36.5** with crun **1.29.1** is also available, paired with Kubernetes
**1.36.4** until CRI-O publishes its 1.37 series. Ansible is pinned to **14.3.1**
and ansible-core **2.21.3**. See [the release inventory](https://particuleio.github.io/symplegma/maintaining/).

Existing clusters must follow Kubernetes' sequential minor upgrade policy.
`symplegma-upgrade.yml` drains each node, upgrades control planes before worker
kubelets, waits for readiness, then uncordons. A failed upgrade leaves the node
cordoned. An explicit `-e upgrade_skip_drain=true` skips eviction for an accepted
in-place upgrade, without guaranteeing workload availability; readiness checks
still run, but both drain and uncordon are skipped so scheduling state is left
unchanged. This is not a direct upgrade path from the former 1.24 defaults.

See [the v3.0.0 changelog and migration notes](https://github.com/particuleio/symplegma/blob/main/CHANGELOG.md) before upgrading an
existing deployment.

## Documentation

Documentation is generated using [mkdocs][mkdocs] and the sources are located in the [`docs/`](https://github.com/particuleio/symplegma/tree/main/docs) directory.

It is available online at [particuleio.github.io/symplegma](https://particuleio.github.io/symplegma/).

[mkdocs]: https://www.mkdocs.org/

## Roles

- [symplegma-os_bootstrap][role-os_bootstrap]: Configure the hosts OS to support Vanilla Kubernetes
- [symplegma-kubernetes_hosts][role-kubernetes_hosts]: Bootstrap Kubernetes on Linux hosts
- [symplegma-kubeadm][role-symplegma-kubeadm]: Bootstrap the Kubernetes Cluster using `kubeadm`
- [symplegma-containerd][role-symplegma-containerd]: Install the [containerd][cri-containerd] CRI
- [symplegma-crio][role-symplegma-crio]: Install the [cri-o][cri-crio] CRI
- [symplegma-cni][role-symplegma-cni]: Boostrap the hosts to install the CNI
- [symplegma-flannel][role-symplegma-flannel]: Bootstrap and install the Flannel CNI

[role-os_bootstrap]: https://github.com/particuleio/symplegma-os_bootstrap.git
[role-kubernetes_hosts]: https://github.com/particuleio/symplegma-kubernetes_hosts
[role-symplegma-kubeadm]: https://github.com/particuleio/symplegma-kubeadm
[role-symplegma-containerd]: https://github.com/particuleio/symplegma-containerd
[role-symplegma-crio]: https://github.com/particuleio/symplegma-crio
[role-symplegma-cni]: https://github.com/particuleio/symplegma-cni
[role-symplegma-flannel]: https://github.com/particuleio/symplegma-flannel

## Roadmap

- [ ] Support [cilium](https://github.com/cilium/cilium) as network plugin
- [ ] Support Kata container on QEMU and Firecracker
- [ ] Support bootstrapping GitOps

## Contributing

Each role is hosted in a separate repository in [particuleio](https://github.com/particuleio).
`requirements.yml` pins their published releases. `scripts/install-roles.py`
installs and verifies those revisions; local clones remain editable
under `roles/`. See [maintenance and validation](https://particuleio.github.io/symplegma/maintaining/).

## License
