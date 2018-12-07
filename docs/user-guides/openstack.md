# Deploying on OpenStack

Symplegma supports OpenStack as a cloud provider.

## Architecture

`contrib/OpenStack/` contains terraform file to deploy the following architecture. This is strongly opinionated and deploys the following architecture:

![OpenStack reference architecture](../images/OpenStack-infra-transparent.png)

For now, each cluster should have its own OpenStack project. Modules used are from the [Kubepsray project](https://github.com/kubernetes-incubator/kubepsray) and are included inside the symplegma module, this is subject to change in the future as PR are welcomed to make the possibilities evolved and split modules.

## Requirements

* [Terraform](https://www.terraform.io/intro/getting-started/install.html)
* [Terragrunt](https://github.com/gruntwork-io/terragrunt#install-terragrunt)
* [Ansible](https://docs.ansible.com/ansible/2.7/installation_guide/intro_installation.html)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

Git clone Symplegma main repository:

```bash
git clone https://github.com/clusterfrak-dynamics/symplegma.git
```

Fetch the roles with `ansible-galaxy`:

```bash
ansible-galaxy install -r requirements.yml
```

## Terraform and Terragrunt

Terragrunt is used to enable multiple cluster and environments.

### Terragrunt modules

Symplegma is packaged in a [Terragrunt module](https://github.com/gruntwork-io/terragrunt) available [here](https://github.com/clusterfrak-dynamics/symplegma/tree/master/contrib/openstack/terraform).

### Terragrunt variables

Cluster specific variables:

```
{!contrib/openstack/terraform/env/sample/symplegma/terraform.tfvars!}
```

## Creating the infrastructure

To init a new OpenStack cluster, simply run `./scripts/init-openstack.sh $CLUSTER_NAME`

It will generate `inventory/openstack/$CLUSTER_NAME` with the following directory structure:

```bash
sample
├── openstack.py -> ../../../contrib/openstack/inventory/openstack.py
├── extra_vars.yml
├── group_vars
│   └── all
│       └── all.yml
├── host_vars
├── symplegma-ansible.sh -> ../../../contrib/openstack/scripts/symplegma-ansible.sh
└── tf_module_symplegma
    └── terraform.tfvars
```

### Customizing the infrastructure

Terraform variable files come with sensible default.

If you wish to change remote state configuration you can edit `$CLUSTER_NAME/terraform.tfvars`

If you wish to customize the infrastructure you can edit `$CLUSTER_NAME/tf_module_symplegma/terraform.tfvars`

One of the most important variable is `cluster_name` that allows you tu use OpenStack dynamic inventory with multiple cluster. We recommend this variables to be coherent throughout your files and equals to `$CLUSTER_NAME` defined earlier.

There is also a set of sensible default tags that you can customize such as `Environment` for example or add your own.

To avoid bloating the configuration files and unnecessary hard coded values, Terraform provider credentials are derived from your OpenStack SDK config. Make sure you are using the correct OpenStack credentials by setting your `OS_CLOUD` environment variable. [[more infos]](https://docs.openstack.org/python-openstackclient/rocky/cli/man/openstack.html)

### Initializing the infrastructure

Once everything is configured to your needs, just run:

```bash
terragrunt apply-all --terragrunt-source-update
```

Couples minute later you should see your instances spawning in your Horizon dashboard.

## Deploying Kubernetes with symplegma playbooks

### OpenStack Dynamic inventory

OpenStack dynamic inventory allows you to target a specific set of instances depending on the `$CLUSTER_NAME` you set earlier. You can configure the behavior of dynamic inventory by setting the following `ENV`:

* `export SYMPLEGMA_CLUSTER=$CLUSTER_NAME` : Target only instances belonging to this cluster.

To test the behavior of the dynamic inventory just run:

```bash
./inventory/openstack/${CLUSTER_NAME}/openstack.py --list
```

It should only return a specific subset of your instances.

!!! info
    These variables can be exported automatically when using the deployment script, but they can still be set manually for testing / manual deployment purposes.

### Customizing Kubernetes deployment

In the cluster folder, it is possible to edit Ansible variables:

* `group_vars/all/all.yml`: contains default Ansible variables.

```bash
{!inventory/sample/group_vars/all/all.yml!}
```

!!! info
    `ansible_ssh_bastion_host`, `kubernetes_api_server_address` and `kubernetes_api_server_port` can be automatically populated when using the deployment script but they can still be set manually for testing / manual deployment purposes.

* `extra_vars`: contains OpenStack cloud provider specific variables that you can override.

```bash
{!contrib/openstack/extra_vars.yml!}
```

!!! info
    If you need to override control plane or kubelet specific parameters do it in `extra_vars.yml` as it overrides all other variables previously defined as per [Ansible variables precedence documentantion](https://docs.ansible.com/ansible/2.7/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable)

### Running the playbooks with deployment script

A simple (really, it cannot be simpler) deployment script can call Ansible and compute the necessary Terraform output for you:

```bash
{!contrib/openstack/scripts/symplegma-ansible.sh!}
```

From the root of the repository just run your cluster deployment script:

```bash
./inventory/openstack/${CLUSTER_NAME}/symplegma-ansible.sh
```

### Testing cluster access

When the deployment is over, `admin.conf` should be exported in `kubeconfig/$CLUSTER_NAME/admin.conf`. You should be able to call the Kubernetes API with `kubectl`:

```bash
export KUBECONFIG=$(pwd)/kubeconfig/${CLUSTER_NAME}/admin.conf

kubectl get nodes

NAME                                       STATUS   ROLES    AGE     VERSION
ip-10-0-1-140.eu-west-1.compute.internal   Ready    <none>   2d22h   v1.13.0
ip-10-0-1-22.eu-west-1.compute.internal    Ready    master   2d22h   v1.13.0
ip-10-0-2-47.eu-west-1.compute.internal    Ready    <none>   2d22h   v1.13.0
ip-10-0-2-8.eu-west-1.compute.internal     Ready    master   2d22h   v1.13.0
ip-10-0-3-123.eu-west-1.compute.internal   Ready    master   2d22h   v1.13.0
```

EOD
