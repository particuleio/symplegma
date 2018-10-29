#! /bin/sh

INVENTORY_DIR=$(dirname "${0}")

export SYMPLEGMA_CLUSTER="$( cd "${INVENTORY_DIR}" && terragrunt output-all cluster_name 2>/dev/null )"
export SYMPLEGMA_AWS_REGION="$( cd "${INVENTORY_DIR}" && terragrunt output-all aws_region 2>/dev/null )"

ansible-playbook -i "${INVENTORY_DIR}"/aws.py symplegma-init.yml -b -v -e @"${INVENTORY_DIR}"/extra_vars.yml -e ansible_ssh_bastion_host="$( cd "${INVENTORY_DIR}" && terragrunt output-all -module=bastion public_ip 2>/dev/null )" -e kubernetes_api_server_address="$( cd "${INVENTORY_DIR}" && terragrunt output-all kubernetes_api_lb_dns_name 2>/dev/null )"
