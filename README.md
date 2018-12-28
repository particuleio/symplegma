# Symplegma

[![Build Status](https://travis-ci.org/clusterfrak-dynamics/symplegma.svg?branch=master)](https://travis-ci.org/clusterfrak-dynamics/symplegma)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)

<p>
<img src="https://raw.githubusercontent.com/cncf/artwork/master/kubernetes/certified-kubernetes/versionless/color/certified-kubernetes-color.png" alt="Certified Kubernetes" title="Certified Kubernetes" width=150/>
</p>

Symplegma (from greek *σύμπλεγμα*) is a simple set of [Ansible](https://www.ansible.com/) playbooks to deploy [Kubernetes](https://kubernetes.io/) with [Kubeadm](https://kubernetes.io/docs/setup/independent/high-availability/). It is heavily inspired by [Kubespray](https://github.com/kubernetes-incubator/kubespray) and [OpenStack Ansible](https://docs.openstack.org/openstack-ansible/latest/).

The main goal is to be minimalist with sensible defaults.

## Deploys a Kubernetes cluster

- Deploys vanilla Kubernetes with Kubeadm.
- Supports [Container Linux OS](https://coreos.com/os/docs/latest/) and [Flatcar Linux](https://www.flatcar-linux.org/)
- Does not rely on Docker
- Uses CRI compatible runtime (containerd by default)
- Does not depend on cloud provider
- Does not depend on primary master

## Documentation

Documentation can be found [here](https://clusterfrak-dynamics.github.io/symplegma/)

## Roadmap

- [X] Provide Terraform infrastructure files for AWS
- [ ] Provide Terraform infrastructure files for OpenStack
- [ ] Support OpenStack Cloud provider
- [X] Support AWS Cloud provider
- [ ] Support [cri-o](http://cri-o.io/) as runtime
- [ ] Support [frakti](https://github.com/kubernetes/frakti) as runtime
- [ ] Support [cilium](https://github.com/cilium/cilium) as network plugin
- [ ] Support [canal](https://github.com/projectcalico/canal) as network plugin

## Contributing

Each role is hosted in a separate repository :

- [symplegma-os_bootstrap](https://github.com/clusterfrak-dynamics/symplegma-os_bootstrap)
- [symplegma-containerd](https://github.com/clusterfrak-dynamics/symplegma-containerd)
- [symplegma-cni](https://github.com/clusterfrak-dynamics/symplegma-cni)
- [symplegma-kubernetes_hosts](https://github.com/clusterfrak-dynamics/symplegma-kubernetes_hosts)
- [symplegma-kubeadm](https://github.com/clusterfrak-dynamics/symplegma-kubeadm)
- [symplegma-calico](https://github.com/clusterfrak-dynamics/symplegma-calico)
