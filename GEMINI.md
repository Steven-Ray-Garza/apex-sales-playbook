# GEMINI.md

Read `AGENTS.md` first and follow its Progressive Loading Protocol.

- Load `core/router.md` and `core/guardrails.md` as your base operating system.
- Activate only the matching `skills/*/SKILL.md` module(s) per the 4-Gate Diagnostic Triage (or jump straight to `skills/transcript-audit-mode/SKILL.md` when a transcript is pasted).
- Prefer running `tools/calculators.py` (or `tools/mcp_server.py`) for all CAC, GP, LTGP, PPD, Value Grid, OTE, TAC, and script-lint checks.
- To sync changes into a standalone Gemini Gem, run `python scripts/build_adapters.py` and copy `adapters/master-gem-prompt.md`.
