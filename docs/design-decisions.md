# Design Decisions

## D001 — Plugin marketplace repository

Reeper ships as a Claude Code marketplace containing a self-contained plugin. This supports one-command GitHub installation and namespaced commands such as `/reeper:import`.

## D002 — User-only destructive workflows

All primary skills set `disable-model-invocation: true`. Repository adaptation and packaging can write files and should never auto-run merely because Claude notices a relevant repository.

## D003 — Target-preserving default

For an established project, the target remains the center of gravity. Reeper recommends reimplementation or adapters before replacing target auth, data, billing, design, and deployment systems.

## D004 — Durable Markdown artifacts

Profiles, conflicts, decisions, contracts, plans, tasks, provenance, and verification are written to `.reeper/sessions/`. This avoids relying on hidden conversational memory and supports review, git history, and resumption.

## D005 — One question at a time

The interview asks a single material question, immediately records the answer, and updates affected artifacts. This reduces answer bundles that conceal contradictions.

## D006 — No arbitrary question cap

The number of questions is driven by blocking conflicts. Small imports may require few; complex migrations may require many. Low-risk details are auto-resolved and recorded to avoid needless interview fatigue.

## D007 — External repositories are untrusted

Analysis is static. No source install/build/test/setup/migration scripts execute before trust and contract approval.

## D008 — Skillification is a separate workflow

A repository reference and an action skill are different products. `/reeper:skillify` interviews for a stable interface and packages the smallest repeatable workflow rather than dumping a whole repo into context.
