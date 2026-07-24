# Changelog

## Unreleased

- Added `make export` (`scripts/export_marketplace_skill.py`), which builds the flattened
  single-skill distribution at `dist/claude-skills/skills/reeper/` from the plugin source
- Added the authored router `marketplace/SKILL.md` and `marketplace/manifest.yaml`
- Added `tests/test_marketplace_export.py`, which fails on any emitted file that escapes the
  skill root or references a path the build does not produce

## 0.1.0 — 2026-07-24

- Initial Claude Code marketplace and plugin structure
- Added `/reeper:import`, `/reeper:resume`, and `/reeper:skillify`
- Added source, target, conflict, and verification subagents
- Added durable session artifacts and contract approval gate
- Added safe clone, fingerprint, session, validation, and skill scaffolding scripts
- Added standard-library tests and local validation workflow
