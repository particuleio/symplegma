"""Render real role templates with Ansible's current templating engine."""

import json
import tomllib
import unittest
from pathlib import Path

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

ROOT = Path(__file__).resolve().parents[1]
ROLES = ROOT / "roles"


def variables(role, arch="x86_64", inventory="ubuntu", **overrides):
    loader = DataLoader()
    defaults_dir = ROLES / role / "defaults"
    defaults = next(defaults_dir.glob("main.y*ml"))
    data = loader.load_from_file(str(defaults), trusted_as_template=True)
    data.update(
        loader.load_from_file(
            str(ROOT / "inventory" / inventory / "group_vars/all/all.yml"), trusted_as_template=True
        )
    )
    facts = {
        "architecture": arch,
        "hostname": "master-1",
        "fqdn": "master-1.example.test",
        "default_ipv4": {"address": "192.0.2.10"},
        "env": {},
    }
    data.update(
        {
            "ansible_facts": facts,
            "inventory_hostname": "master-1",
            "groups": {"master": ["master-1", "master-2"], "node": ["worker-1"]},
            "hostvars": {
                "master-1": {"ansible_facts": facts},
                "master-2": {"ansible_facts": {**facts, "default_ipv4": {"address": "192.0.2.11"}}},
            },
            "kubeadm_token": {"stdout": "abcdef.0123456789abcdef"},
            "kubeadm_ca_hash": {"stdout": "a" * 64},
            "kubernetes_control_plane_local": {"rc": 0},
        }
    )
    data.update(overrides)
    return loader, data


def render(role, template, **kwargs):
    loader, data = variables(role, **kwargs)
    templar = Templar(loader=loader, variables=data)
    source = (ROLES / role / "templates" / template).read_text()
    result = templar.template(trust_as_template(source))
    if "{{" in result or "{%" in result:
        raise AssertionError(f"Unresolved template in {role}/{template}")
    return result


class ConfigurationTests(unittest.TestCase):
    def test_kubeadm_api_and_etcd_members_for_both_inventories(self):
        for inventory in ("ubuntu", "flatcar"):
            with self.subTest(inventory=inventory):
                docs = list(
                    yaml.safe_load_all(
                        render(
                            "symplegma-kubeadm/master",
                            "kubeadm-config.yaml.j2",
                            inventory=inventory,
                        )
                    )
                )
                cluster, init, kubelet, proxy = docs
                self.assertEqual(cluster["apiVersion"], "kubeadm.k8s.io/v1beta4")
                self.assertEqual(init["apiVersion"], "kubeadm.k8s.io/v1beta4")
                self.assertEqual(cluster["kubernetesVersion"], "v1.37.0")
                args = {a["name"]: a["value"] for a in cluster["etcd"]["local"]["extraArgs"]}
                self.assertEqual(
                    args["initial-cluster"],
                    "master-1=https://192.0.2.10:2380,master-2=https://192.0.2.11:2380",
                )
                self.assertEqual(kubelet["cgroupDriver"], "systemd")
                self.assertEqual(proxy["kind"], "KubeProxyConfiguration")

    def test_kubeadm_preserves_duplicate_arguments_and_types(self):
        docs = list(
            yaml.safe_load_all(
                render(
                    "symplegma-kubeadm/master",
                    "kubeadm-config.yaml.j2",
                    kubeadm_api_server_extra_args=[
                        {"name": "tls-sni-cert-key", "value": "cert-a,key-a"},
                        {"name": "tls-sni-cert-key", "value": "cert-b,key-b"},
                    ],
                    kubeadm_kubelet_extra_args={"v": 2},
                    kubeadm_kubelet_component_config={"failSwapOn": False},
                )
            )
        )
        self.assertEqual(len(docs[0]["apiServer"]["extraArgs"]), 2)
        self.assertEqual(
            docs[1]["nodeRegistration"]["kubeletExtraArgs"], [{"name": "v", "value": "2"}]
        )
        self.assertIs(docs[2]["failSwapOn"], False)

    def test_legacy_yaml_strings_are_migrated(self):
        cluster = next(
            yaml.safe_load_all(
                render(
                    "symplegma-kubeadm/master",
                    "kubeadm-config.yaml.j2",
                    kubeadm_api_server_extra_args='audit-log-maxage: "30"\n',
                )
            )
        )
        self.assertEqual(
            cluster["apiServer"]["extraArgs"], [{"name": "audit-log-maxage", "value": "30"}]
        )

    def test_join_uses_ca_verification_for_both_runtimes(self):
        for socket in ("unix:///run/containerd/containerd.sock", "unix:///run/crio/crio.sock"):
            join = next(
                yaml.safe_load_all(
                    render(
                        "symplegma-kubeadm/node",
                        "kubeadm-config.yaml.j2",
                        cri_socket=socket,
                    )
                )
            )
            self.assertEqual(join["apiVersion"], "kubeadm.k8s.io/v1beta4")
            discovery = join["discovery"]["bootstrapToken"]
            self.assertEqual(discovery["caCertHashes"], ["sha256:" + "a" * 64])
            self.assertNotIn("unsafeSkipCAVerification", discovery)
            self.assertEqual(join["nodeRegistration"]["criSocket"], socket)

    def test_containerd_configuration(self):
        for arch in ("x86_64", "aarch64"):
            config = tomllib.loads(
                render(
                    "symplegma-containerd",
                    "config.toml.j2",
                    arch=arch,
                    containerd_socket="/run/test-containerd.sock",
                )
            )
            self.assertEqual(config["version"], 4)
            self.assertEqual(
                config["plugins"]["io.containerd.server.v1.grpc"]["address"],
                "/run/test-containerd.sock",
            )
            runtime = config["plugins"]["io.containerd.cri.v1.runtime"]["containerd"]["runtimes"][
                "runc"
            ]
            self.assertEqual(runtime["runtime_type"], "io.containerd.runc.v2")
            self.assertEqual(runtime["options"]["BinaryName"], "/usr/local/bin/runc")
            self.assertIs(runtime["options"]["SystemdCgroup"], True)
            self.assertEqual(
                config["plugins"]["io.containerd.cri.v1.images"]["pinned_images"]["sandbox"],
                "registry.k8s.io/pause:3.10.2",
            )

    def test_crio_runtime_selection_and_cgroups(self):
        for use_crun, expected in (
            (True, "crun"),
            (False, "runc"),
            ("true", "crun"),
            ("false", "runc"),
        ):
            config = tomllib.loads(
                render("symplegma-crio", "10-crun.conf.j2", crio_use_crun=use_crun)
            )
            self.assertEqual(config["crio"]["runtime"]["default_runtime"], expected)
        cgroups = tomllib.loads(render("symplegma-crio", "02-cgroup-manager.conf.j2"))
        self.assertEqual(cgroups["crio"]["runtime"]["cgroup_manager"], "systemd")

    def test_flannel_uses_supported_resources_and_cni_installer(self):
        for backend in ("host-gw", "vxlan"):
            docs = list(
                yaml.safe_load_all(
                    render(
                        "symplegma-flannel",
                        "kube-flannel.yaml.j2",
                        flannel_backend=backend,
                    )
                )
            )
            self.assertNotIn("PodSecurityPolicy", [d["kind"] for d in docs])
            config = next(d for d in docs if d["kind"] == "ConfigMap")
            self.assertEqual(
                json.loads(config["data"]["net-conf.json"])["Backend"]["Type"], backend
            )
            json.loads(config["data"]["cni-conf.json"])
            ds = next(d for d in docs if d["kind"] == "DaemonSet")
            spec = ds["spec"]["template"]["spec"]
            self.assertEqual(spec["initContainers"][1]["command"], ["/opt/bin/install-conf"])
            self.assertTrue(
                all(
                    c["image"].startswith("ghcr.io/flannel-io/")
                    for c in spec["initContainers"] + spec["containers"]
                )
            )

    def test_crictl_follows_the_target_kubernetes_minor(self):
        for minor in range(32, 38):
            loader, data = variables(
                "symplegma-kubernetes_hosts", kubernetes_version=f"v1.{minor}.8"
            )
            templar = Templar(loader=loader, variables=data)
            self.assertEqual(templar.template(data["crictl_version"]), f"v1.{minor}.0")

    def test_download_architectures(self):
        cases = {
            "symplegma-containerd": ["containerd_release_url", "runc_release_url"],
            "symplegma-crio": ["crio_release_url", "crun_release_url", "runc_release_url"],
            "symplegma-cni": ["cni_plugins_release_url"],
            "symplegma-kubernetes_hosts": ["kubernetes_binaries_url", "crictl_release_url"],
            "symplegma-os_bootstrap": ["etcd_release_url", "jq_release_url"],
        }
        for arch, expected in (("x86_64", "amd64"), ("aarch64", "arm64")):
            for role, names in cases.items():
                loader, data = variables(role, arch=arch)
                templar = Templar(loader=loader, variables=data)
                for name in names:
                    with self.subTest(arch=arch, role=role, variable=name):
                        url = templar.template(data[name])
                        self.assertIn(expected, url)
                        self.assertNotIn("{{", url)

    def test_crio_registry_security_settings_are_not_swapped(self):
        config = tomllib.loads(
            render(
                "symplegma-crio",
                "registries.conf.j2",
                registries_insecure=["insecure.example.test"],
                registries_block=["blocked.example.test"],
            )
        )
        registries = {entry["location"]: entry for entry in config["registry"]}
        self.assertIs(registries["insecure.example.test"]["insecure"], True)
        self.assertIs(registries["insecure.example.test"]["blocked"], False)
        self.assertIs(registries["blocked.example.test"]["blocked"], True)
        self.assertIs(registries["blocked.example.test"]["insecure"], False)

    def test_upgrade_preflight_rejects_skipped_minors_and_downgrades(self):
        loader = DataLoader()
        plays = loader.load_from_file(str(ROOT / "symplegma-upgrade.yml"), trusted_as_template=True)
        task = next(t for t in plays[0]["tasks"] if "single-minor" in t["name"])
        conditions = task["ansible.builtin.assert"]["that"]
        for source, target, allowed in (
            ("1.32.2", "1.32.13", True),
            ("1.32.13", "1.33.13", True),
            ("1.33.13", "1.34.11", True),
            ("1.34.11", "1.35.8", True),
            ("1.35.8", "1.36.4", True),
            ("1.32.2", "1.36.4", False),
            ("1.36.4", "1.37.0", True),
            ("1.37.0", "1.37.0", True),
            ("1.24.1", "1.37.0", False),
            ("1.35.8", "1.37.0", False),
            ("1.37.0", "1.36.4", False),
        ):
            templar = Templar(
                loader=loader,
                variables={
                    "current_version": source,
                    "target_version": target,
                    "kubernetes_version": f"v{target}",
                    "kubeadm_version": f"v{target}",
                },
            )
            with self.subTest(source=source, target=target):
                self.assertEqual(all(templar.evaluate_conditional(c) for c in conditions), allowed)

    def test_runtime_preflight_rejects_unsupported_transitions(self):
        loader = DataLoader()
        plays = loader.load_from_file(str(ROOT / "symplegma-upgrade.yml"), trusted_as_template=True)
        task = next(t for t in plays[0]["tasks"] if "supported containerd" in t["name"])
        for source, target, allowed in (
            ("1.6.38", "2.3.5", False),
            ("1.6.38", "1.7.29", False),  # This role requires the v4 configuration schema.
            ("1.7.29", "2.3.5", True),
            ("1.7.29", "2.2.0", False),
            ("2.0.3", "2.3.5", True),
            ("2.0.6", "2.3.5", True),
            ("2.0.6", "2.4.0", False),
            ("2.2.6", "2.3.5", True),
            ("2.3.4", "2.3.5", True),
            ("2.3.5", "2.3.5", True),
            ("2.3.5", "2.3.4", False),
        ):
            templar = Templar(
                loader=loader,
                variables={
                    **task["vars"],
                    "installed_containerd": {
                        "stdout": f"containerd github.com/containerd/containerd v{source} abc123\n"
                    },
                    "containerd_version": target,
                },
            )
            with self.subTest(source=source, target=target):
                self.assertEqual(
                    all(
                        templar.evaluate_conditional(c)
                        for c in task["ansible.builtin.assert"]["that"]
                    ),
                    allowed,
                )

    def test_upgrade_does_not_require_manual_confirmation_variables(self):
        source = (ROOT / "symplegma-upgrade.yml").read_text()
        self.assertNotIn("upgrade_backup_confirmed", source)
        self.assertNotIn("upgrade_maintenance_confirmed", source)

    def test_auxiliary_templates_render_without_undefined_variables(self):
        for role in (
            "symplegma-containerd",
            "symplegma-crio",
            "symplegma-kubernetes_hosts",
            "symplegma-kubeadm/node",
            "symplegma-os_bootstrap",
        ):
            for template in (ROLES / role / "templates").glob("*.j2"):
                with self.subTest(role=role, template=template.name):
                    output = render(role, template.name)
                    if ".json." in template.name:
                        json.loads(output)
                    if ".yaml." in template.name:
                        list(yaml.safe_load_all(output))

    def test_windows_roles_are_retired(self):
        requirements = yaml.safe_load((ROOT / "requirements.yml").read_text())
        self.assertFalse(any("win_" in r["name"] for r in requirements))
        for filename in ("symplegma-init.yml", "symplegma-upgrade.yml"):
            self.assertNotIn("win_node", (ROOT / filename).read_text())


if __name__ == "__main__":
    unittest.main()
