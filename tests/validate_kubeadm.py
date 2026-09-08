"""Validate rendered configs with the pinned kubeadm binary; never contact a cluster."""

import argparse
import hashlib
import platform
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from .test_configuration import render, variables

# A Linux userspace for local macOS validation. CI executes kubeadm natively.
VALIDATION_IMAGE = (
    "debian:trixie-slim@sha256:d7e12182ce18b85b93007c1dedf31f2d29e01ccf3182cc4017c709b6259bc132"
)


def validate_version(version):
    if not re.fullmatch(r"v1\.\d+\.\d+", version):
        raise ValueError("Expected a stable Kubernetes version such as v1.36.4")
    arch = {"x86_64": "amd64", "aarch64": "arm64", "arm64": "arm64"}[platform.machine()]
    url = f"https://dl.k8s.io/release/{version}/bin/linux/{arch}/kubeadm"
    with tempfile.TemporaryDirectory(prefix="symplegma-kubeadm-") as temp:
        directory = Path(temp)
        binary = directory / "kubeadm"
        with urllib.request.urlopen(url, timeout=60) as response:
            binary.write_bytes(response.read())
        with urllib.request.urlopen(f"{url}.sha256", timeout=60) as response:
            checksum = response.read().decode().strip()
        if hashlib.sha256(binary.read_bytes()).hexdigest() != checksum:
            raise ValueError("Kubeadm checksum mismatch")
        binary.chmod(0o755)
        for inventory in ("ubuntu", "flatcar"):
            for role in ("master", "node"):
                config = directory / f"{inventory}-{role}.yaml"
                config.write_text(
                    render(
                        f"symplegma-kubeadm/{role}",
                        "kubeadm-config.yaml.j2",
                        inventory=inventory,
                        kubernetes_version=version,
                        kubeadm_version=version,
                    )
                )
                if platform.system() == "Linux":
                    command = [str(binary), "config", "validate", "--config", str(config)]
                else:
                    command = [
                        "docker",
                        "run",
                        "--rm",
                        "--network=none",
                        "--mount",
                        f"type=bind,source={directory},target=/validation,readonly",
                        VALIDATION_IMAGE,
                        "/validation/kubeadm",
                        "config",
                        "validate",
                        "--config",
                        f"/validation/{config.name}",
                    ]
                subprocess.run(command, check=True)
                print(f"{version}: {config.name} validated", flush=True)


def main():
    _, defaults = variables("symplegma-kubeadm/master")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("versions", nargs="*", help="Stable Kubernetes versions to validate")
    args = parser.parse_args()
    for version in args.versions or [defaults["kubernetes_version"]]:
        validate_version(version)


if __name__ == "__main__":
    main()
