# Security Policy

Reeper treats external repositories as untrusted and intentionally blocks source-code execution during analysis.

## Reporting

Please report vulnerabilities privately through GitHub Security Advisories after the repository is published. Do not include real credentials or sensitive repository contents in public issues.

## Security-sensitive areas

- source repository cloning and static inspection
- lifecycle script and hook detection
- secret-name handling
- approval gates before implementation or destructive operations
- plugin permissions and bundled scripts
