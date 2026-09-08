# mise owns tool versions; uv owns Python and Python dependencies.
set shell := ["mise", "exec", "--", "bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# Install the locked environment, roles, and local Git hooks.
setup: sync roles hooks

sync:
    uv sync --locked --all-groups

# Install exact published upstream role revisions.
roles:
    uv run --locked python scripts/install-roles.py

hooks:
    uv run --locked pre-commit install

# Run the same pre-commit checks as CI.
lint:
    uv run --locked pre-commit run --all-files --show-diff-on-failure

# Render Kubernetes, runtime, and network configurations.
test:
    uv run --locked python -m unittest discover -s tests -v

# Check configuration with the actual released kubeadm binary.
[positional-arguments]
validate-kubeadm *versions:
    uv run --locked python -m tests.validate_kubeadm "$@"

# Read-only SSH/API checks; does not drain nodes or upgrade components.
[positional-arguments]
upgrade-check inventory version:
    uv run --locked ansible-playbook -b -i "inventory/$1/hosts" symplegma-upgrade.yml --tags always -e "kubernetes_version=$2" -e "kubeadm_version=$2"

# Check all playbooks against both Linux inventories.
syntax:
    #!/usr/bin/env bash
    set -euo pipefail
    for inventory in ubuntu flatcar; do
      for playbook in symplegma-init.yml symplegma-upgrade.yml symplegma-reset.yml; do
        mise exec -- uv run --locked ansible-playbook -i "inventory/$inventory/hosts" "$playbook" --syntax-check
      done
    done

docs:
    uv run --locked --group docs mkdocs build --strict

check: lint test syntax docs
