# Reeper

**Reeper safely adapts external GitHub repositories to your existing project instead of blindly copying their architecture.**

It analyzes the source and target independently, builds an evidence-backed conflict matrix, interviews you one material decision at a time, writes an Integration Contract, waits for explicit approval, implements in isolation, and verifies the result against the contract.

## Why Reeper

Coding agents are good at copying code and bad at noticing when the copied assumptions quietly replace your authentication, database, billing, deployment, design system, or operational conventions. Reeper turns repository adaptation into a durable reconciliation process.

Core principles:

- **Target-preserving by default** — existing project systems remain authoritative unless you approve replacement.
- **Evidence before questions** — Reeper inspects both repos first and asks only what code cannot answer.
- **One conflict at a time** — every material decision is recommended, answered, and recorded.
- **Contract before code** — implementation is blocked until you approve the Integration Contract.
- **Untrusted source model** — source scripts, installs, hooks, submodules, and binaries are not executed during analysis.
- **Resumable artifacts** — sessions survive context loss and can be resumed later.
- **Provenance-aware** — copied, adapted, replaced, rejected, and reimplemented components are tracked.

## Commands

### `/reeper:import`

Import or adapt a repository into the current project.

```text
/reeper:import https://github.com/example/source-repo
Bring its analytics dashboard into this app, but preserve our Supabase auth,
Stripe billing, shadcn components, and Vercel deployment.
```

Supported integration modes:

- transplant selected features
- reimplement behavior against target-native systems
- fork the source as the new base
- vendor an isolated library/package
- reference source patterns without copying code

### `/reeper:resume`

Resume the most recent incomplete Reeper session without repeating completed analysis or interview decisions.

```text
/reeper:resume
```

### `/reeper:skillify`

Turn a repository or stable workflow into a callable Agent Skill or Claude Code plugin.

```text
/reeper:skillify .
Create a user-invoked command that audits and repairs our lead import pipeline.
```

## Install from GitHub

After this repository is published at `leadgenjay/Reeper`:

```text
/plugin marketplace add leadgenjay/Reeper
/plugin install reeper@reeper
```

Then invoke:

```text
/reeper:import <repo-url> [goal]
```

## Install as a single Agent Skill

Reeper also ships as one flattened Agent Skill for people who install skills rather than plugins:

```bash
curl -sL 'https://leadgenjay.com/api/skills/install.sh?items=reeper' | bash
```

That form is a build artifact, not a second source of truth. Regenerate it with:

```bash
make export     # -> dist/claude-skills/skills/reeper/
```

The plugin lays its skills out as `plugins/reeper/skills/<name>/SKILL.md` and reaches the shared
guides with `${CLAUDE_SKILL_DIR}/../../references/...`. That climb is correct inside a plugin and
wrong for a skill install, where every file lands in one directory, so `scripts/export_marketplace_skill.py`
rewrites the paths, strips the per-skill frontmatter into `workflows/*.md`, and renders the router
`SKILL.md` plus `manifest.yaml` from `marketplace/`. `tests/test_marketplace_export.py` fails the
build if any emitted file escapes the skill root or points at a path that does not exist.

The plugin form remains the richer install: namespaced commands and automatically registered subagents.

## Test locally

From Claude Code:

```text
/plugin marketplace add /absolute/path/to/Reeper
/plugin install reeper@reeper
/plugin validate /absolute/path/to/Reeper
```

Or with the CLI:

```bash
claude plugin validate .
```

## What Reeper creates in the target

Each adaptation gets a durable session:

```text
.reeper/sessions/<session>/
├── manifest.json
├── intake.md
├── source-profile.md
├── target-profile.md
├── source-fingerprint.json
├── target-fingerprint.json
├── conflict-matrix.md
├── decisions.md
├── integration-contract.md
├── plan.md
├── tasks.md
├── provenance.json
└── verification.md
```

Local source checkouts and worktrees are ignored under `.reeper/cache/` and `.reeper/worktrees/`.

## Workflow

```text
Source repo ─┐
             ├─ independent evidence-first profiles
Target repo ─┘
                    ↓
             conflict matrix
                    ↓
          one-question interview
                    ↓
          Integration Contract
                    ↓ explicit approval
          isolated implementation
                    ↓
        contract-based verification
                    ↓
       optional skill/plugin packaging
```

## Safety model

During analysis Reeper may read and statically inspect files, manifests, git metadata, and packed repository output. It must not run external repository install, build, setup, migration, seed, hook, application, container, or arbitrary scripts before trust approval.

The bundled `safe_clone.sh` disables hooks, skips submodules, and skips Git LFS smudge. It still treats the cloned files as untrusted.

## Requirements

- Claude Code with plugin support
- Git
- Python 3.10+
- Optional: Node/npm for Repomix (`npx repomix@latest`)

The core helper scripts use only the Python standard library.

## Inspiration

Reeper combines ideas from:

- **Repomix:** remote repository packing, incremental codebase exploration, security-aware ingestion, and generated reference skills
- **GitHub Spec Kit:** durable phase artifacts, clarification, planning, task generation, and cross-artifact validation
- **Superpowers:** one-question-at-a-time design discovery and a hard implementation gate
- **Anthropic Agent Skills and Claude Code plugins:** progressive disclosure, invocable skills, supporting scripts/references, subagents, and marketplace distribution

Reeper is an independent project and does not include code copied from those projects.

## Status

`v0.1.0` is an initial functional plugin scaffold with the complete workflow, deterministic session/fingerprint/scaffolding helpers, validation, and tests. It should be exercised against real repositories before a stable release.

## License

MIT
