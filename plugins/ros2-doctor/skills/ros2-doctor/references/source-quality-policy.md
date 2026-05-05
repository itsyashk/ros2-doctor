# Source Quality Policy

Use official documentation first.

## Priority Order

1. Official ROS 2 documentation, package docs, and REP documents.
2. colcon and ament documentation.
3. Maintainer-backed GitHub issues or release notes.
4. Robotics StackExchange, Stack Overflow, ROS Discourse, Reddit, and blogs as pattern evidence only.

## Community Source Rules

- Use community sources to identify recurring signatures, not to copy fixes.
- Rewrite every pattern in original wording.
- Preserve URLs in `SOURCES.md` or a playbook `Sources used` section.
- Prefer official docs when advice conflicts.
- Say when a fix is pattern-based and uncertain.
- Avoid Quora and unattributed snippets.

## Verification Standard

Every diagnosis should connect at least one observed symptom to one inspected
file, command output, log line, or source-backed ROS 2 rule. If that evidence is
missing, classify the result as a hypothesis and give the next command needed to
confirm it.
