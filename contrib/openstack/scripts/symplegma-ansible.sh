#! /bin/sh

INVENTORY_DIR=$(dirname "${0}")

export SYMPLEGMA_CLUSTER="$( cd "${INVENTORY_DIR}" && terragrunt output-all cluster_name 2>/dev/null )"

ansible-playbook -i "${INVENTORY_DIR}"/hosts.ini symplegma-init.yml -b -v \
  -e @"${INVENTORY_DIR}"/extra_vars.yml \
  -e ansible_ssh_bastion_host="$( cd "${INVENTORY_DIR}" && terragrunt output-all bastion_fips 2>/dev/null )" \
  "$@"
