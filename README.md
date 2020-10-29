# Symplegma

<p align="center">
  <img src="images/logo.png">
</p>

![symplegma:mkdocs](https://github.com/clusterfrak-dynamics/symplegma/workflows/symplegma:mkdocs/badge.svg)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma?ref=badge_shield)

<p align="left">
<a href="https://github.com/cncf/k8s-conformance"><img src="https://github.com/cncf/artwork/raw/master/projects/kubernetes/certified-kubernetes/1.19/color/certified-kubernetes-1.19-color.png" alt="Certified Kubernetes" title="Certified Kubernetes" width=75 style="vertical-align:middle;margin:10px 20px" /></a>
<a href="https://landscape.cncf.io/format=card-mode&organization=particule&selected=symplegma"><img src="https://github.com/cncf/artwork/raw/master/other/cncf-landscape/stacked/color/cncf-landscape-stacked-color.png" alt="Certified Kubernetes" title="Certified Kubernetes" width=75 style="vertical-align:middle;margin:10px 20px" /></a>
</p>

Symplegma (from greek *σύμπλεγμα*) is a simple set of [Ansible](https://www.ansible.com/) playbooks to deploy [Kubernetes](https://kubernetes.io/) with [Kubeadm](https://kubernetes.io/docs/setup/independent/high-availability/). It is heavily inspired by [Kubespray](https://github.com/kubernetes-incubator/kubespray) and [OpenStack Ansible](https://docs.openstack.org/openstack-ansible/latest/).

Symplegma is [Kubernetes certified](https://github.com/cncf/k8s-conformance/tree/master/v1.15/symplegma) since `v1.12`. Check out [CNCF Landscape](https://landscape.cncf.io/).

The main goal is to be minimalist with sensible defaults.

## Deploys a Kubernetes cluster

- Deploys vanilla Kubernetes with Kubeadm.
- Supports [Flatcar Linux](https://www.flatcar-linux.org/) / Ubuntu 20.04
- Does not rely on Docker
- Uses CRI compatible runtime (containerd by default)
- Does not depend on cloud provider
- Does not depend on primary master
- Dynamic config
- Always up to date: No deprecated options

## Documentation

Documentation can be found [here](https://clusterfrak-dynamics.github.io/symplegma/)

## Roadmap

- [ ] Support [cri-o](http://cri-o.io/) as runtime
- [ ] Support [cilium](https://github.com/cilium/cilium) as network plugin
- [ ] Support Fedora CoreOS
- [ ] Support Centos
- [ ] Support bootstrapping GitOps

## Contributing

Each role is hosted in a separate repository in [particuleio](https://github.com/particuleio). Exhaustive list of roles can be found in `requirements.yml`

## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fclusterfrak-dynamics%2Fsymplegma?ref=badge_large)
