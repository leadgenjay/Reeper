from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins" / "reeper" / "scripts"
FIXTURE = ROOT / "tests" / "fixtures" / "minimal-target"


class ReeperScriptsTest(unittest.TestCase):
    def test_fingerprint_detects_stack_without_reading_secret_values(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "fingerprint.json"
            subprocess.run(
                ["python3", str(SCRIPTS / "repo_fingerprint.py"), str(FIXTURE), "--json-out", str(out)],
                check=True,
            )
            data = json.loads(out.read_text())
            self.assertEqual(data["package_manager"], "pnpm")
            self.assertIn("Next.js", data["frameworks"])
            self.assertIn("Supabase", data["frameworks"])
            self.assertIn("Stripe", data["frameworks"])
            self.assertIn("postinstall", data["lifecycle_scripts"])
            self.assertIn("SUPABASE_URL", data["environment_variable_names"])
            self.assertNotIn("SUPABASE_URL=", json.dumps(data))
            self.assertIn(".env.example", data["sensitive_filename_candidates"])

    def test_new_session_creates_required_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run(
                [
                    "python3", str(SCRIPTS / "new_session.py"),
                    "--source", "example/source", "--target", temp,
                    "--goal", "Import dashboard", "--slug", "test-session",
                ],
                check=True, capture_output=True, text=True,
            )
            session = Path(result.stdout.strip())
            self.assertTrue((session / "manifest.json").exists())
            self.assertTrue((session / "integration-contract.md").exists())
            manifest = json.loads((session / "manifest.json").read_text())
            self.assertEqual(manifest["session"], "test-session")
            self.assertEqual(manifest["phases"]["implementation"], "blocked")

    def test_scaffold_skill(self):
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(
                [
                    "python3", str(SCRIPTS / "scaffold_skill.py"),
                    "--output", temp, "--name", "My Workflow",
                    "--description", "Runs my workflow when requested.", "--user-only",
                ],
                check=True,
            )
            skill = Path(temp) / "my-workflow"
            body = (skill / "SKILL.md").read_text()
            self.assertIn("name: my-workflow", body)
            self.assertIn("disable-model-invocation: true", body)
            self.assertTrue((skill / "evals" / "prompts.json").exists())

    def test_plugin_structure_and_manual_invocation_guards(self):
        root = ROOT
        marketplace = json.loads((root / ".claude-plugin" / "marketplace.json").read_text())
        plugin = json.loads((root / "plugins" / "reeper" / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(marketplace["name"], "reeper")
        self.assertEqual(plugin["name"], "reeper")
        for skill in ["import", "resume", "skillify"]:
            body = (root / "plugins" / "reeper" / "skills" / skill / "SKILL.md").read_text()
            self.assertIn("disable-model-invocation: true", body)
            self.assertLess(len(body.splitlines()), 500)

    def test_validate_incomplete_session(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run(
                [
                    "python3", str(SCRIPTS / "new_session.py"),
                    "--source", "example/source", "--target", temp, "--slug", "test-session",
                ],
                check=True, capture_output=True, text=True,
            )
            session = result.stdout.strip()
            validation = subprocess.run(
                ["python3", str(SCRIPTS / "validate_session.py"), session, "--allow-incomplete"],
                capture_output=True, text=True,
            )
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)


if __name__ == "__main__":
    unittest.main()
