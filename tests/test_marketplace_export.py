from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "scripts" / "export_marketplace_skill.py"

WORKFLOWS = ["import", "resume", "skillify"]


class MarketplaceExportTest(unittest.TestCase):
    """The single-skill build must never reintroduce the plugin-root climb.

    `${CLAUDE_SKILL_DIR}/../../references/...` resolves correctly inside a plugin
    and escapes into `~/.claude/` from a marketplace install, so a regression here
    ships a skill whose guides and scripts silently fail to load.
    """

    @classmethod
    def setUpClass(cls):
        cls._temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls._temp.name) / "reeper"
        result = subprocess.run(
            ["python3", str(EXPORT), "--output", str(cls.output), "--quiet"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stdout + result.stderr

    @classmethod
    def tearDownClass(cls):
        cls._temp.cleanup()

    def test_no_file_escapes_the_skill_directory(self):
        offenders = [
            path.relative_to(self.output).as_posix()
            for path in sorted(self.output.rglob("*"))
            if path.is_file() and "../.." in path.read_text(encoding="utf-8", errors="ignore")
        ]
        self.assertEqual(offenders, [], f"files still escape the skill root: {offenders}")

    def test_every_referenced_skill_path_exists(self):
        missing = []
        for path in sorted(self.output.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            for target in _skill_dir_references(text):
                if not (self.output / target).exists():
                    missing.append(f"{path.relative_to(self.output).as_posix()} -> {target}")
        self.assertEqual(missing, [], f"dangling ${{CLAUDE_SKILL_DIR}} references: {missing}")

    def test_router_and_workflows_are_present(self):
        self.assertTrue((self.output / "SKILL.md").is_file())
        self.assertTrue((self.output / "manifest.yaml").is_file())
        for name in WORKFLOWS:
            workflow = self.output / "workflows" / f"{name}.md"
            self.assertTrue(workflow.is_file(), f"missing workflow: {name}")
            body = workflow.read_text(encoding="utf-8")
            self.assertNotIn("---\nname:", body[:8], "frontmatter should be stripped")
            self.assertLess(len(body.splitlines()), 500)

    def test_manifest_version_is_rendered(self):
        manifest = (self.output / "manifest.yaml").read_text(encoding="utf-8")
        self.assertNotIn("{{VERSION}}", manifest)
        self.assertIn('version: "', manifest)

    def test_helper_scripts_are_shipped_and_runnable(self):
        scripts = self.output / "scripts"
        for name in [
            "new_session.py",
            "repo_fingerprint.py",
            "validate_session.py",
            "scaffold_skill.py",
            "safe_clone.sh",
        ]:
            self.assertTrue((scripts / name).is_file(), f"missing script: {name}")
        result = subprocess.run(
            ["python3", str(scripts / "validate_session.py"), "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_categories_do_not_gate_the_skill(self):
        manifest = (self.output / "manifest.yaml").read_text(encoding="utf-8")
        self.assertNotIn("lgj-exclusive", manifest)


def _skill_dir_references(text: str) -> list[str]:
    references = []
    for chunk in text.split("${CLAUDE_SKILL_DIR}/")[1:]:
        target = chunk.split("`")[0].split('"')[0].split(" ")[0].split("\n")[0]
        target = target.rstrip(".,)")
        if target:
            references.append(target)
    return references


if __name__ == "__main__":
    unittest.main()
