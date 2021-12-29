# Symplegma

<p align="center">
  <img src="images/logo.png">
</p>

![symplegma:mkdocs](https://github.com/clusterfrak-dynamics/symplegma/workflows/symplegma:mkdocs/badge.svg)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma?ref=badge_shield)

<p align="left">
<a href="https://github.com/cncf/k8s-conformance"><img src="https://github.com/cncf/artwork/raw/master/projects/kubernetes/certified-kubernetes/versionless/color/certified-kubernetes-color.png" alt="Certified Kubernetes" title="Certified Kubernetes" width=75 style="vertical-align:middle;margin:10px 20px" /></a>
<a href="https://landscape.cncf.io/format=card-mode&organization=particule&selected=symplegma"><img src="https://github.com/cncf/artwork/raw/master/other/cncf-landscape/stacked/color/cncf-landscape-stacked-color.png" alt="Certified Kubernetes" title="Certified Kubernetes" width=75 style="vertical-align:middle;margin:10px 20px" /></a>
</p>

Symplegma (from greek *σύμπλεγμα*) is a simple set of [Ansible](https://www.ansible.com/) playbooks to deploy [Kubernetes](https://kubernetes.io/) with [Kubeadm](https://kubernetes.io/docs/setup/independent/high-availability/). It is heavily inspired by [Kubespray](https://github.com/kubernetes-incubator/kubespray) and [OpenStack Ansible](https://docs.openstack.org/openstack-ansible/latest/).

Symplegma is [Kubernetes certified](https://github.com/cncf/k8s-conformance/tree/master/v1.20/symplegma) since `v1.12`. Check out [CNCF Landscape](https://landscape.cncf.io/).

The main goal is to be minimalist with sensible defaults.

## Deploys a Kubernetes cluster

- Deploys vanilla Kubernetes with Kubeadm.
- Supports [Flatcar Linux](https://www.flatcar-linux.org/) / Ubuntu 20.04
- Does not rely on Docker
- Uses CRI compatible runtime:
    - [containerd][cri-containerd] (default)
    - [cri-o][cri-crio]
- Does not depend on cloud provider
- Does not depend on primary master
- Dynamic config
- Always up to date: No deprecated options

[cri-crio]: https://cri-o.io/
[cri-containerd]: https://github.com/containerd/containerd
[cri-docker]: https://docs.docker.com/engine/

## Documentation

Documentation can be found [here](https://particuleio.github.io/symplegma/)

## Roles

- [symplegma-os_bootstrap][role-os_bootstrap]: Configure the hosts OS to support Vanilla Kubernetes
- [symplegma-kubernetes_hosts][role-kubernetes_hosts]: Bootstrap Kubernetes on Linux hosts
- [symplegma-win_kubernetes_hosts][role-symplegma-win_kubernetes_hosts]: Bootstrap Kubernetes on Windows hosts
- [symplegma-kubeadm][role-symplegma-kubeadm]: Bootstrap the Kubernetes Cluster using `kubeadm`
- [symplegma-containerd][role-symplegma-containerd]: Install the [containerd][cri-containerd] CRI
- [symplegma-crio][role-symplegma-crio]: Install the [cri-o][cri-crio] CRI
- [symplegma-win_docker][role-symplegma-win_docker]: Install the [docker][cri-docker] CRI on Windows hosts
- [symplegma-cni][role-symplegma-cni]: Boostrap the hosts to install the CNI
- [symplegma-calico][role-symplegma-calico]: Boostrap and install the Calico CNI
- [symplegma-flannel][role-symplegma-flannel]: Bootstrap and install the Flannel CNI
- [symplegma-win_cni][role-symplegma-win_cni]: Bootstrap Windows hosts to install the CNI

[role-os_bootstrap]: https://github.com/particuleio/symplegma-os_bootstrap.git
[role-kubernetes_hosts]: https://github.com/particuleio/symplegma-kubernetes_hosts
[role-symplegma-kubeadm]: https://github.com/particuleio/symplegma-kubeadm
[role-symplegma-containerd]: https://github.com/particuleio/symplegma-containerd
[role-symplegma-crio]: https://github.com/particuleio/symplegma-crio
[role-symplegma-cni]: https://github.com/particuleio/symplegma-cni
[role-symplegma-calico]: https://github.com/particuleio/symplegma-calico
[role-symplegma-flannel]: https://github.com/particuleio/symplegma-flannel
[role-symplegma-win_cni]: https://github.com/particuleio/symplegma-win_cni
[role-symplegma-win_kubernetes_hosts]: https://github.com/particuleio/symplegma-win_kubernetes_hosts
[role-symplegma-win_docker]: https://github.com/particuleio/symplegma-win_docker

## Roadmap

- [ ] Support [cilium](https://github.com/cilium/cilium) as network plugin
- [ ] Support Kata container on QEMU and Firecracker
- [ ] Support bootstrapping GitOps

## Contributing

Each role is hosted in a separate repository in [particuleio](https://github.com/particuleio). Exhaustive list of roles can be found in `requirements.yml`

## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma?ref=badge_large)
