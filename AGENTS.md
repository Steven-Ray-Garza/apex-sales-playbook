# AGENTS.md - Apex Revenue Operations Playbook (v4.0 Universal Agent Entrypoint)

This repository implements a clean-room, model-agnostic Acquisition & Revenue Operations system designed to run reliably across **Claude, Gemini, ChatGPT, and local LLMs (Ollama / llama.cpp / vLLM)**.

## Progressive Loading Protocol (Mandatory)

To prevent attention decay across both frontier and local models:

1. **Always load first:**
   - `core/router.md` (Role, Intake Protocol, 4-Gate Diagnostic Triage, Output Standards)
   - `core/guardrails.md` (Source fidelity, founder proof gate, accounting integrity, vocal hygiene, compliance, legal/telecom/fulfillment circuit breakers, AI ROI judgment gate)
2. **Load ONLY the active skill(s) required for the user's request:**
   - Offer design, 80/20 cohort avatar audit, promotional wrappers, Non-Linear Offer Matrix, Van Westendorp pricing, or Self-Funded Acquisition (SFA) math -> `skills/sfa-offer-architect/SKILL.md`
   - Multi-Stage Pre-Call VSL architecture, BANT forms, spoken call scripts, analogies, AAA objection loops, BAMFAM, referrals -> `skills/vsl-script-engineer/SKILL.md`
   - Recruiting funnels, `3 Ps + 1`, manager scorecards, `50/50 OTE`, 14-day bootcamp, ramp gates, internal promotion pipelines -> `skills/sales-recruiting-bootcamp/SKILL.md`
   - Manager schedules, Mon-Sat huddles, Hunt vs. Kill Mode, pipeline audits, 1-on-1s, call-tape diagnostics -> `skills/sales-floor-director/SKILL.md`
   - Pre-call battle card, raw call transcript audit, weekly flywheel brief, or closed-deal fulfillment handoff -> `skills/transcript-audit-mode/SKILL.md` (skip intake immediately)
   - Live interactive roleplay, cooperative memorization drill, pressure objection sparring, or high-frequency interruption interview -> `skills/roleplay-sparring-partner/SKILL.md` (skip intake immediately)
3. **Prefer deterministic tools over mental math:**
   - Run `tools/calculators.py` (or its MCP server `tools/mcp_server.py`) for CAC, GP, LTGP, PPD, 30D Cash, Non-Linear Offer Matrix, Van Westendorp pricing, OTE accelerators, TAC caps, and spoken pitch word-count/tag linting.
4. **Enforce JSON schemas for CRM automation:**
   - Validate Mode 5 structured outputs against `schemas/call_notes_6line.schema.json` and `schemas/bant_scorecard.schema.json`.

## Hard Repo & Privacy Rules

- Never commit third-party copyrighted materials, client recordings, hardcoded local usernames, or raw PII transcripts into Git. Keep private local files exclusively inside `sources/` or `transcripts/` (gitignored).
- Never fabricate chapters, policies, or metrics absent from verified inputs.
- Always run `python scripts/build_adapters.py` after editing `core/` or `skills/` so `adapters/` stay synchronized with zero drift.
