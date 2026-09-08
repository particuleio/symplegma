#!/usr/bin/env python3
"""Install exact published role revisions without overwriting local changes."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def run(*args, check=True):
    return subprocess.run(args, cwd=ROOT, check=check)


def main():
    os.environ.setdefault("ANSIBLE_HOME", str(ROOT / ".ansible"))
    requirements = yaml.safe_load((ROOT / "requirements.yml").read_text())
    missing = [role for role in requirements if not (ROOT / "roles" / role["name"]).exists()]
    if missing:
        with tempfile.TemporaryDirectory(prefix="symplegma-roles-") as temp:
            manifest = Path(temp) / "requirements.yml"
            manifest.write_text(yaml.safe_dump(missing))
            run(
                str(Path(sys.executable).with_name("ansible-galaxy")),
                "role",
                "install",
                "-r",
                str(manifest),
                "-p",
                "roles",
            )
    for role in requirements:
        name = role["name"]
        role_dir = ROOT / "roles" / name
        expected = role["version"]
        if (role_dir / ".git").exists():
            expected = subprocess.check_output(
                ["git", "-C", str(role_dir), "rev-parse", f"{expected}^{{commit}}"], text=True
            ).strip()
            version = subprocess.check_output(
                ["git", "-C", str(role_dir), "rev-parse", "HEAD"], text=True
            ).strip()
        else:
            metadata = role_dir / "meta" / ".galaxy_install_info"
            version = yaml.safe_load(metadata.read_text())["version"]
        if version != expected:
            sys.exit(
                f"{name}: expected {role['version']}, found {version}; preserve local edits before reinstalling."
            )
        print(f"{name}: verified {role['version']}", flush=True)


if __name__ == "__main__":
    main()
