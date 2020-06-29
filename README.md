# Symplegma

<p align="center">
  <img src="images/logo.png">
</p>

[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma?ref=badge_shield)


Symplegma (from greek *σύμπλεγμα*) is a simple set of [Ansible](https://www.ansible.com/) playbooks to deploy [Kubernetes](https://kubernetes.io/) with [Kubeadm](https://kubernetes.io/docs/setup/independent/high-availability/). It is heavily inspired by [Kubespray](https://github.com/kubernetes-incubator/kubespray) and [OpenStack Ansible](https://docs.openstack.org/openstack-ansible/latest/).

Symplegma is [Kubernetes certified](https://github.com/cncf/k8s-conformance/tree/master/v1.15/symplegma) since `v1.12`. Check out [CNCF Landscape](https://landscape.cncf.io/).
<p align="center">
<img src="https://raw.githubusercontent.com/cncf/artwork/master/projects/kubernetes/certified-kubernetes/versionless/color/certified-kubernetes-color.png" alt="Certified Kubernetes" title="Certified Kubernetes" width=150/>
</p>

The main goal is to be minimalist with sensible defaults.

## Deploys a Kubernetes cluster

- Deploys vanilla Kubernetes with Kubeadm.
- Supports [Container Linux OS](https://coreos.com/os/docs/latest/) / [Flatcar Linux](https://www.flatcar-linux.org/) / Ubuntu
- Does not rely on Docker
- Uses CRI compatible runtime (containerd by default)
- Does not depend on cloud provider
- Does not depend on primary master

## Documentation

Documentation can be found [here](https://clusterfrak-dynamics.github.io/symplegma/)

## Roadmap

- [X] Provide Terraform infrastructure files for AWS
- [X] Provide Terraform infrastructure files for OpenStack
- [ ] Support OpenStack Cloud provider
- [X] Support AWS Cloud provider
- [ ] Support [cri-o](http://cri-o.io/) as runtime
- [ ] Support [cilium](https://github.com/cilium/cilium) as network plugin

## Contributing

Each role is hosted in a separate repository :

- [symplegma-os_bootstrap](https://github.com/clusterfrak-dynamics/symplegma-os_bootstrap)
- [symplegma-containerd](https://github.com/clusterfrak-dynamics/symplegma-containerd)
- [symplegma-cni](https://github.com/clusterfrak-dynamics/symplegma-cni)
- [symplegma-kubernetes_hosts](https://github.com/clusterfrak-dynamics/symplegma-kubernetes_hosts)
- [symplegma-kubeadm](https://github.com/clusterfrak-dynamics/symplegma-kubeadm)
- [symplegma-calico](https://github.com/clusterfrak-dynamics/symplegma-calico)

## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma?ref=badge_large)
