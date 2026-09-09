"""Reject stale node readiness and retry transient control-plane outages."""

import json
import unittest
from pathlib import Path

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

ROOT = Path(__file__).resolve().parents[1]


class UpgradeReadinessTests(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()
        self.tasks = self.loader.load_from_file(
            str(ROOT / "tasks/upgrade-node.yml"), trusted_as_template=True
        )

    def test_node_requires_target_version_and_ready(self):
        task = self.tasks[-3]
        for rc, version, ready, allowed in (
            (1, "v1.34.11", "True", False),
            (0, "v1.33.13", "True", False),
            (0, "v1.34.11", "False", False),
            (0, "v1.34.11", "Unknown", False),
            (0, "v1.34.11", None, False),
            (0, "v1.34.11", "True", True),
        ):
            status = {
                "nodeInfo": {"kubeletVersion": version},
                "conditions": [] if ready is None else [{"type": "Ready", "status": ready}],
            }
            templar = Templar(
                loader=self.loader,
                variables={
                    "kubernetes_version": "v1.34.11",
                    "upgrade_node_status": {
                        "rc": rc,
                        "stdout": "" if rc else json.dumps({"status": status}),
                    },
                },
            )
            with self.subTest(rc=rc, version=version, ready=ready):
                self.assertEqual(templar.evaluate_conditional(task["until"]), allowed)

    def test_final_api_operations_are_bounded_and_retry_failures(self):
        for task in self.tasks[-3:]:
            self.assertEqual(task["retries"], 30)
            self.assertEqual(task["delay"], 5)
            self.assertIn("--request-timeout=10s", task["ansible.builtin.command"]["argv"])
            self.assertEqual(task["delegate_to"], "{{ groups['master'] | first }}")
        for task in self.tasks[-2:]:
            for rc in (0, 1):
                templar = Templar(loader=self.loader, variables={task["register"]: {"rc": rc}})
                self.assertEqual(templar.evaluate_conditional(task["until"]), rc == 0)
        self.assertIn("--raw=/readyz", self.tasks[-2]["ansible.builtin.command"]["argv"])
        self.assertNotIn("when", self.tasks[-3])
        self.assertNotIn("when", self.tasks[-2])
        self.assertEqual(self.tasks[-4]["ansible.builtin.meta"], "flush_handlers")


if __name__ == "__main__":
    unittest.main()
