# Contributing

## Development

Run:

```bash
make validate
```

Test the plugin locally in Claude Code:

```text
/plugin marketplace add /absolute/path/to/Reeper
/plugin install reeper@reeper
/plugin validate /absolute/path/to/Reeper
```

## Pull requests

- Keep source analysis read-only.
- Do not add permission bypasses.
- Preserve the Integration Contract approval gate.
- Add or update tests for deterministic scripts.
- Document any new session artifact or phase transition.
- Bump plugin and marketplace versions for releases.
