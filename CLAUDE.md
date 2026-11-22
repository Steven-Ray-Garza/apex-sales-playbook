# CLAUDE.md

Read `AGENTS.md` first and follow its Progressive Loading Protocol.

- Load `core/router.md` and `core/guardrails.md` as your base operating system.
- Activate only the matching `skills/*/SKILL.md` module(s) per the 4-Gate Diagnostic Triage (or jump straight to `skills/transcript-audit-mode/SKILL.md` when a transcript is pasted).
- Prefer calling `tools/calculators.py` (via Bash or `tools/mcp_server.py`) for all financial calculations and script linting instead of doing arithmetic by hand.
- After modifying any file under `core/` or `skills/`, run `python scripts/build_adapters.py` to rebuild platform adapters and verify token/ASCII compliance.
