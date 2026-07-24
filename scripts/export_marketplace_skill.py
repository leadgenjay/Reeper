#!/usr/bin/env python3
"""Build the single-skill marketplace form of the Reeper plugin.

The plugin lays its skills out as `plugins/reeper/skills/<name>/SKILL.md` and lets
them reach the shared guides with `${CLAUDE_SKILL_DIR}/../../references/...`. That
climb is correct inside a plugin and wrong for a marketplace install, where every
file lands under a single `~/.claude/skills/<id>/` directory.

This script emits that flattened form so the two distributions cannot drift by
hand. Everything except `marketplace/SKILL.md` and `marketplace/manifest.yaml`
is mechanically derived from `plugins/reeper/`.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "reeper"
AUTHORED_ROOT = REPO_ROOT / "marketplace"
DEFAULT_OUTPUT = REPO_ROOT / "dist" / "claude-skills" / "skills" / "reeper"

WORKFLOWS = ["import", "resume", "skillify"]
VERBATIM_DIRS = ["references", "scripts", "templates", "agents"]

# The plugin-root climb becomes a skill-root reference.
PATH_REWRITE = ("${CLAUDE_SKILL_DIR}/../../", "${CLAUDE_SKILL_DIR}/")

FRONTMATTER = re.compile(r"\A---\n.*?\n---\n+", re.DOTALL)

WORKFLOW_HEADER = (
    "> Part of the `reeper` skill. `SKILL.md` holds the operating principles and the\n"
    "> non-negotiable gates that apply to this workflow.\n\n"
)


def command_rewrites() -> dict[str, str]:
    """Plugin slash commands do not exist in the single-skill form."""
    return {
        f"/reeper:{name}": f"the {name} workflow (`workflows/{name}.md`)"
        for name in WORKFLOWS
    }


def transform_workflow(text: str) -> str:
    body = FRONTMATTER.sub("", text, count=1)
    body = body.replace(*PATH_REWRITE)
    for command, replacement in command_rewrites().items():
        body = body.replace(f"`{command}`", replacement)
        body = body.replace(command, replacement)
    return WORKFLOW_HEADER + body


def plugin_version() -> str:
    manifest = json.loads(
        (PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    version = manifest.get("version")
    if not version:
        raise SystemExit("plugin.json has no version")
    return str(version)


def build(output: Path) -> list[Path]:
    if not PLUGIN_ROOT.is_dir():
        raise SystemExit(f"plugin root not found: {PLUGIN_ROOT}")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    written: list[Path] = []

    version = plugin_version()
    skill_md = (AUTHORED_ROOT / "SKILL.md").read_text(encoding="utf-8")
    (output / "SKILL.md").write_text(skill_md, encoding="utf-8")
    written.append(output / "SKILL.md")

    manifest = (AUTHORED_ROOT / "manifest.yaml").read_text(encoding="utf-8")
    manifest = manifest.replace("{{VERSION}}", version)
    (output / "manifest.yaml").write_text(manifest, encoding="utf-8")
    written.append(output / "manifest.yaml")

    workflows_dir = output / "workflows"
    workflows_dir.mkdir()
    for name in WORKFLOWS:
        source = PLUGIN_ROOT / "skills" / name / "SKILL.md"
        if not source.is_file():
            raise SystemExit(f"missing plugin skill: {source}")
        destination = workflows_dir / f"{name}.md"
        destination.write_text(
            transform_workflow(source.read_text(encoding="utf-8")), encoding="utf-8"
        )
        written.append(destination)

    for directory in VERBATIM_DIRS:
        source = PLUGIN_ROOT / directory
        if not source.is_dir():
            raise SystemExit(f"missing plugin directory: {source}")
        shutil.copytree(source, output / directory)
        written.extend(sorted(p for p in (output / directory).rglob("*") if p.is_file()))

    return written


def audit(output: Path) -> list[str]:
    """Fail loudly on the failure modes this build exists to prevent."""
    problems: list[str] = []
    for path in sorted(output.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        relative = path.relative_to(output).as_posix()
        if "../.." in text:
            problems.append(f"{relative}: escapes the skill directory with '../..'")
        if "CLAUDE_PLUGIN_ROOT" in text:
            problems.append(f"{relative}: references CLAUDE_PLUGIN_ROOT")
        if re.search(r"/Users/[a-zA-Z]|/home/[a-zA-Z]|C:\\\\Users", text):
            problems.append(f"{relative}: contains a username-bearing absolute path")
        if "{{" in text and "}}" in text and "templates/" not in relative:
            problems.append(f"{relative}: unrendered placeholder remains")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Reeper as a single marketplace skill")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    output = Path(args.output).expanduser().resolve()
    written = build(output)

    problems = audit(output)
    if problems:
        print("Export audit failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    if not args.quiet:
        print(f"{output} ({len(written)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
