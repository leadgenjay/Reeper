# Reeper Architecture

## Components

### Orchestrator skills

- `import`: end-to-end repository adaptation
- `resume`: artifact-driven continuation
- `skillify`: repository-to-skill/plugin packaging

### Read-only analysts

- source analyst
- target analyst
- conflict analyst
- verification auditor

### Deterministic helpers

- session creation
- repository fingerprinting
- safe source cloning
- session validation
- Agent Skill scaffolding

### Durable artifacts

Session files act as the communication layer between phases and across Claude Code contexts. They make decisions auditable and resumable.

## Why the interview is inside the main skill

The interview needs conversation history and direct user interaction, so the main `/reeper:import` skill runs inline. High-volume source/target analysis is delegated to subagents to preserve the main context.

## Why implementation is not a separate automatic agent

The target project may already have its own development methodology, agents, and permissions. Reeper supplies the approved contract and task plan, then integrates with the target's existing tooling rather than imposing an implementation agent that bypasses it.

## Why Repomix is optional

Repomix is the preferred remote ingestion path for large repositories, but Reeper must remain usable with Git and Python alone. The safe clone and fingerprint scripts provide a conservative fallback.
