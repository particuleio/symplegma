#! /bin/sh

mkdir -p inventory/openstack/"${1}"
cp -arn inventory/sample/* inventory/openstack/"${1}"/.
cp -arn contrib/openstack/terraform/env/terraform.tfvars inventory/openstack/.
cp -arn contrib/openstack/terraform/env/sample/symplegma/. inventory/openstack/"${1}"/tf_module_symplegma
cp -arn contrib/openstack/extra_vars.yml inventory/openstack/"${1}"/.
ln -sf ../../../contrib/openstack/scripts/symplegma-ansible.sh inventory/openstack/"${1}"/.
ln -sf ../../../contrib/openstack/inventory/openstack.py inventory/openstack/"${1}"/.
