"""Keep destructive drain behavior opt-in while preserving eviction safeguards."""

import unittest
from pathlib import Path

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

ROOT = Path(__file__).resolve().parents[1]


class UpgradeDrainTests(unittest.TestCase):
    def test_skip_drain_requires_explicit_opt_in(self):
        loader = DataLoader()
        tasks = loader.load_from_file(
            str(ROOT / "tasks/upgrade-node.yml"), trusted_as_template=True
        )
        for value, should_drain in (
            (None, True),
            (False, True),
            ("false", True),
            (True, False),
            ("true", False),
        ):
            variables = {} if value is None else {"upgrade_skip_drain": value}
            with self.subTest(value=value):
                templar = Templar(loader=loader, variables=variables)
                for task in (tasks[0], tasks[-1]):
                    self.assertEqual(templar.evaluate_conditional(task["when"]), should_drain)
        for task in tasks[1:-1]:
            self.assertNotIn("upgrade_skip_drain", str(task))
        self.assertEqual(tasks[-3]["name"], "Wait for the upgraded node to become ready")
        self.assertEqual(
            tasks[-2]["name"], "Wait for the API to be ready after the kubelet restart"
        )
        self.assertEqual(tasks[-1]["name"], "Uncordon the successfully upgraded node")

    def test_emptydir_deletion_requires_explicit_opt_in(self):
        loader = DataLoader()
        tasks = loader.load_from_file(
            str(ROOT / "tasks/upgrade-node.yml"), trusted_as_template=True
        )
        drain = tasks[0]["ansible.builtin.command"]["argv"]
        for value, expected in (
            (None, "false"),
            (False, "false"),
            ("false", "false"),
            (True, "true"),
            ("true", "true"),
        ):
            variables = {"ansible_facts": {"hostname": "blackwell"}}
            if value is not None:
                variables["upgrade_drain_delete_emptydir_data"] = value
            with self.subTest(value=value):
                argv = Templar(loader=loader, variables=variables).template(drain)
                self.assertIn(f"--delete-emptydir-data={expected}", argv)
                self.assertIn("--ignore-daemonsets", argv)
                self.assertIn("--timeout=10m", argv)
                self.assertFalse(
                    any(arg.split("=")[0] in ("--force", "--disable-eviction") for arg in argv)
                )


if __name__ == "__main__":
    unittest.main()
