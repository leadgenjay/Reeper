---
description: Safely adapt an external repository into this project. Routes to the Reeper import, resume, or skillify workflow.
argument-hint: <repo-url|owner/repo|path> [goal] | resume [session] | skillify <path> [command]
---

# Reeper

Route `$ARGUMENTS` to the correct Reeper workflow, then follow that workflow exactly.

## 1. Pick the workflow

Read the first token of `$ARGUMENTS`:

| First token | Workflow | Remaining arguments |
|---|---|---|
| `resume` | `resume` | optional session slug or path |
| `skillify` | `skillify` | `<repo-path\|repo-url> [desired command]` |
| anything else (a URL, `owner/repo`, or a local path) | `import` | the whole of `$ARGUMENTS`: source first, goal after |
| empty | see below | |

If `$ARGUMENTS` is empty, first check whether `.reeper/sessions/` in the current project holds a session whose `manifest.json` is incomplete. If one exists, use `resume`. Otherwise ask the user for the source repository and nothing else.

Before starting `import`, check `.reeper/sessions/` for an incomplete session on the same source. If there is one, use `resume` instead so completed analysis and interview answers are not repeated.

## 2. Locate the installed workflow

Reeper installs either as a plugin or as a single skill. Resolve whichever is present, preferring the plugin because it also registers the read-only subagents:

```bash
WORKFLOW=import   # or: resume | skillify
for root in "$HOME"/.claude/plugins/cache/reeper/reeper/*/ "$HOME"/.claude/skills/reeper/; do
  [ -d "$root" ] || continue
  for candidate in "$root/skills/$WORKFLOW/SKILL.md" "$root/workflows/$WORKFLOW.md"; do
    if [ -f "$candidate" ]; then
      echo "REEPER_ROOT=${root%/}"
      echo "REEPER_WORKFLOW=$candidate"
      break 2
    fi
  done
done
```

Read the file at `REEPER_WORKFLOW` and follow it. Inside that file, every `${CLAUDE_SKILL_DIR}` is the plugin form's `<root>/skills/<workflow>/` or the skill form's `REEPER_ROOT`; in both cases the referenced `references/` and `scripts/` directories live directly under `REEPER_ROOT`, so resolve them there.

If the loop prints nothing, Reeper is not installed. Tell the user and offer both installs, then stop:

```text
/plugin marketplace add leadgenjay/Reeper
/plugin install reeper@reeper
```

```bash
curl -sL 'https://leadgenjay.com/api/skills/install.sh?items=reeper' | bash
```

## 3. Gates that apply no matter which workflow runs

These come from the workflow files themselves. Restated here so they are in context before any analysis begins:

1. Do not run source install, build, setup, migration, hook, or executable scripts during analysis.
2. Do not copy secrets, `.env` values, tokens, private keys, generated credentials, or local machine state.
3. Do not modify application code until the user explicitly approves the written Integration Contract.
4. Do not overwrite target architecture by default. The target's existing systems stay authoritative unless a recorded decision says otherwise.
5. Pin the source to an exact commit SHA and record its license before implementation.
6. Implement on an isolated branch or worktree when the target is a Git repository.
7. Ask exactly one material question per message during the interview.

Do not summarize the workflow and improvise. Read it and execute it.
