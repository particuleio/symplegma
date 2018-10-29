#! /bin/sh

mkdir -p inventory/aws/"${1}"
cp -arn inventory/sample/* inventory/aws/"${1}"/.
cp -arn contrib/aws/terraform/env/terraform.tfvars inventory/aws/.
cp -arn contrib/aws/terraform/env/sample/symplegma/. inventory/aws/"${1}"/tf_module_symplegma
cp -arn contrib/aws/extra_vars.yml inventory/aws/"${1}"/.
ln -sf contrib/aws/scripts/symplegma-ansible.sh inventory/aws/"${1}"/.
ln -sf ../../../contrib/aws/inventory/aws.py inventory/aws/"${1}"/.
