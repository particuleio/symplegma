#! /bin/bash

set -x

INVENTORY_DIR=$(dirname "${0}")

export SYMPLEGMA_CLUSTER="$(cd "${INVENTORY_DIR}" && terragrunt run-all output cluster_name 2>/dev/null)"
export SYMPLEGMA_AWS_REGION="$(cd "${INVENTORY_DIR}" && terragrunt run-all output aws_region 2>/dev/null)"

ansible-playbook -i "${INVENTORY_DIR}"/aws_ec2.yml symplegma-init.yml -b -v \
  -e @"${INVENTORY_DIR}"/extra_vars.yml \
  -e ansible_ssh_bastion_host="$(cd "${INVENTORY_DIR}" && terragrunt run-all output bastion_public_ip 2>/dev/null)" \
  -e kubernetes_api_server_address="$(cd "${INVENTORY_DIR}" && terragrunt run-all output kubernetes_api_lb_dns_name 2>/dev/null)" \
  -e kubernetes_api_server_port="$(cd "${INVENTORY_DIR}" && terragrunt run-all output kubernetes_api_lb_listener_port 2>/dev/null)" \
  ${@}
