# AGENTS.md - Apex of Sales & $100M Playbook (Universal Agent Entrypoint)

This repository implements a model-agnostic Acquisition & Revenue Operations system designed to run reliably across **Claude, Gemini, ChatGPT, and local LLMs (Ollama / llama.cpp / vLLM)**.

## Progressive Loading Protocol (Mandatory)

To prevent attention decay ("lost-in-the-middle") across both frontier and local models:

1. **Always load first:**
   - `core/router.md` (Role, Intake Protocol, 4-Gate Diagnostic Triage, Output Standards)
   - `core/guardrails.md` (Source fidelity, accounting integrity, vocal hygiene, legal/telecom/fulfillment circuit breakers)
2. **Load ONLY the active skill(s) required for the user's request:**
   - Offer, avatar, wrapper, Value Grid, or CFA math -> `skills/cfa-offer-architect/SKILL.md`
   - VSSL Sandwich, BANT forms, spoken call scripts, analogies, AAA loops, BAMFAM, referrals -> `skills/vssl-script-engineer/SKILL.md`
   - Hiring funnels, `3 Ps + 1`, manager scorecards, `50/50 OTE`, 14-day bootcamp, ramp gates, farm promotions -> `skills/sales-recruiting-bootcamp/SKILL.md`
   - Manager schedules, Mon-Sat huddles, Hunt vs. Kill Mode, pipeline audits, 1-on-1s, call-tape diagnostics -> `skills/sales-floor-director/SKILL.md`
   - Raw call transcript pasted -> `skills/transcript-audit-mode/SKILL.md` (skip intake immediately)
3. **Prefer deterministic tools over mental math:**
   - Run `tools/calculators.py` (or its MCP server `tools/mcp_server.py`) for CAC, GP, LTGP, PPD, 30D Cash, Value Grid, OTE accelerators, TAC caps, and spoken pitch word-count/tag linting.
4. **Enforce JSON schemas for CRM automation:**
   - Validate Mode 5 structured outputs against `schemas/call_notes_6line.schema.json` and `schemas/bant_scorecard.schema.json`.

## Hard Repo & Privacy Rules

- Never commit copyrighted reference files, client recordings, or raw PII transcripts into Git. Keep all private reference files inside `sources/` (gitignored).
- Never fabricate chapters or rules outside verified files.
- Always run `python scripts/build_adapters.py` after editing `core/` or `skills/` so `adapters/` stay synchronized with zero drift.
