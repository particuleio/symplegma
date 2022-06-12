# Deploying on bare metal

Symplegma supports deploying on bare metal. It is actually the main use case.

`symplegma-os_bootstrap` supports bootstrapping python on Flatcar Linux but
should also work with any OS manageable by Ansible as it installs binaries from
sources and does not depends on distribution package manager. If you are using
another distribution, just make sure `python3-dev python3-pip` or `python-dev
python-pip` are installed and that the following kernel modules can be loaded.

```yaml
{!roles/symplegma-os_bootstrap/defaults/main.yml!}
```

You can contribute to the bootstrap role
[here](https://github.com/clusterfrak-dynamics/symplegma-os_bootstrap)

## Requirements

* [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

Git clone Symplegma main repository:

```console
git clone https://github.com/clusterfrak-dynamics/symplegma.git
```

Fetch the roles with `ansible-galaxy`:

```console
ansible-galaxy install -r requirements.yml
```

## Preparing inventory

Simply copy the sample inventory to another folder with the desired cluster
name:

```console
cp -ar inventory/ubuntu inventory/$CLUSTER_NAME
```

Create an inventory in a [compatible
format](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html),
for example in `inventory/$CLUSTER_NAME/hosts` file:

```ini
k8s-master-1.clusterfrak-dynamics.io
k8s-worker-1.clusterfrak-dynamics.io
k8s-worker-2.clusterfrak-dynamics.io
k8s-worker-3.clusterfrak-dynamics.io
k8s-worker-4.clusterfrak-dynamics.io

[master]
k8s-master-1.clusterfrak-dynamics.io

[node]
k8s-worker-1.clusterfrak-dynamics.io
k8s-worker-2.clusterfrak-dynamics.io
k8s-worker-3.clusterfrak-dynamics.io
k8s-worker-4.clusterfrak-dynamics.io
```

Your directory structure should be the following:

```console
tree -I 'roles|contrib|docs|scripts|sample'
.
├── README.md
└── symplegma
    ├── CODEOWNERS
    ├── LICENSE
    ├── README.md
    ├── ansible.cfg
    ├── inventory
    │   └── $CLUSTER_NAME
    │       ├── group_vars
    │       │   └── all
    │       │       └── all.yml
    │       ├── host_vars
    │       └── hosts
    ├── kubeconfig
    │   └── $CLUSTER_NAME
    │       └── admin.conf
    ├── mkdocs.yml
    ├── requirements.yml
    ├── symplegma-init.yml
    ├── symplegma-reset.yml
    └── symplegma-upgrade.yml
```

## Configuring the cluster

Cluster configuration is done in
`inventory/$CLUSTER_NAME/group_vars/all/all.yml`:

```yaml
{!inventory/ubuntu/group_vars/all/all.yml!}
```

Some lines have been modified compared to the original file assumes you are
running behind a bastion host. Here we connect directly to the host through SSH.
`kubeadm` version and `kubernetes` version can also be customized here, please
note by default `kubernetes_version` is equal to `kubeadm_version` but not the
opposite :

```yaml
{!roles/symplegma-kubeadm/master/defaults/main.yaml!}
```

This allow to create custom deployments and custom upgrade logic (updating
Kubelet before control plane for example).

## Running the playbooks

Playbooks can be run from the `symplegma` directory of the repository:

```console
sudo ansible-playbook -i inventory/$CLUSTER_NAME/hosts -b symplegma-init.yml -v
```

The following tags are also availabled to run specific roles:

* `bootstrap`: bootstrap OS for ansible.
* `containerd`: install Kubernetes default container runtime.
* `cni`: install container network interface plugins.
* `kubernetes_hosts`: install Kubernetes binaries and Kubeadm.
* `kubeadm-master`: bootstrap Kubeadm master nodes
* `kuebadm-nodes`: bootstrap Kubeadm worker nodes

### Upgrading the cluster

There is another playbook `symplegma-upgrade.yml` which does the same thing as
`symplegma-init.yml` but with a serial set to 1. It means that nodes will be
upgraded one by one.

To update Kubernetes to another version, just change `kubeadm_version` and
`kubernetes_version` in `symplegma/inventory/$CLUSTER_NAME/group_vars/all/all.yml`
and re-run the playbooks for `kubernetes_host` and `kubeadm-master`.

```console
ansible-playbook -i inventory/$CLUSTER_NAME/hosts -b symplegma-upgrade.yml -v --tags kubernetes_hosts
ansible-playbook -i inventory/$CLUSTER_NAME/hosts -b symplegma-upgrade.yml -v --tags kubeadm-master
```

## Accessing the cluster

When the playbbok are done, a `kubeconfig` file is generated in
`symplegma/kubeconfig/$CLUSTER_NAME/admin.conf`. This file contains the TLS
certificates to access the cluster as an administrator.

By default, `kubectl` looks into `~/.kube/config`. To use the generated
`kubeconfig` file from the `symplegma` directory:

```console
export KUBECONFIG=$(pwd)/kubeconfig/$CLUSTER_NAME/admin.conf
```

Check that you can access the cluster:

```console
kubectl get nodes
NAME               STATUS   ROLES    AGE   VERSION
k8s-master-1   Ready    master   25h   v1.15.0
k8s-worker-1   Ready    <none>   25h   v1.15.0
k8s-worker-2   Ready    <none>   25h   v1.15.0
k8s-worker-3   Ready    <none>   25h   v1.15.0
k8s-worker-4   Ready    <none>   25h   v1.15.0
```

```console
kubectl get pods --all-namespaces
NAMESPACE             NAME                                             READY   STATUS    RESTARTS   AGE
kube-system           calico-kube-controllers-6fb584dd97-wfj5r         1/1     Running   1          7d20h
kube-system           calico-node-554qz                                1/1     Running   1          7d20h
kube-system           calico-node-c28zf                                1/1     Running   1          7d20h
kube-system           calico-node-glqjd                                1/1     Running   1          7d20h
kube-system           calico-node-lm9hp                                1/1     Running   0          20h
kube-system           calico-node-qkw4j                                1/1     Running   1          7d20h
kube-system           coredns-5c98db65d4-kvsnz                         1/1     Running   2          7d20h
kube-system           coredns-5c98db65d4-s8zsb                         1/1     Running   2          7d20h
kube-system           etcd-k8s-master-1-dev                            1/1     Running   2          7d20h
kube-system           kube-apiserver-k8s-master-1-dev                  1/1     Running   2          7d20h
kube-system           kube-controller-manager-k8s-master-1-dev         1/1     Running   2          7d20h
kube-system           kube-proxy-dxllt                                 1/1     Running   1          7d20h
kube-system           kube-proxy-h97vq                                 1/1     Running   0          20h
kube-system           kube-proxy-kt9gc                                 1/1     Running   1          7d20h
kube-system           kube-proxy-ngw7p                                 1/1     Running   1          7d20h
kube-system           kube-proxy-rgh7t                                 1/1     Running   1          7d20h
kube-system           kube-scheduler-k8s-master-1-dev                  1/1     Running   2          7d20h
kube-system           nginx-proxy-k8s-worker-1-dev                     1/1     Running   1          7d20h
kube-system           nginx-proxy-k8s-worker-2-dev                     1/1     Running   1          7d20h
kube-system           nginx-proxy-k8s-worker-3-dev                     1/1     Running   1          7d20h
kube-system           nginx-proxy-k8s-worker-4-dev                     1/1     Running   1          20h
```

## Conformance end to end test

The cluster has passed Kubernetes conformance testing. These tests are run with
[`sonobuoy`](https://github.com/heptio/sonobuoy).

#### Install Sonobuoy

Install `sonobuoy`:

1. by downloading the binary -> go to https://github.com/heptio/sonobuoy/releases
2. alternatively, on a machine with Go installed:

```console
go get -u -v github.com/heptio/sonobuoy
```

#### Run sonobuoy manually

To run sonobuoy (the right `kubeconfig` must be set as sonobuoy talks to the
cluster):

```console
sonobuoy run
```

The tests might take between 60 minutes and 2h. To check the status:

```console
sonobuoy status
```

To retrieve the results once it is done:

```console
sonobuoy retrieve
```

To inspect results:

```console
sonobuoy e2e 201906261404_sonobuoy_4aff5e8e-21a8-448c-8960-c6565b92be91.tar.gz
failed tests: 0
```

Then delete cluster resources:

```console
sonobuoy delete
```

