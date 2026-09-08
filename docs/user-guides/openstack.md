# OpenStack

The former OpenStack provisioning modules and deployment wrapper are no longer
present in this repository. Provision current Ubuntu or Flatcar instances with
your existing OpenStack tooling, create a Linux inventory, and follow the
[bare-metal deployment guide](bare-metal.md).

Use private node addresses that are reachable by every cluster member, and make
the Kubernetes API endpoint reachable by the Ansible controller. Configure a load
balancer address with `kubernetes_api_server_address` for HA control planes.
The removed Terraform modules and Windows worker workflow are not supported by
the refreshed playbooks.
