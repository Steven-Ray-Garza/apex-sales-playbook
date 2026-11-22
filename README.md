# Apex of Sales & $100M Playbook (Model-Agnostic AI Repo)

One canonical source of truth for running a 5-mode Acquisition & Revenue Operations system across **Claude, Gemini, ChatGPT, and local LLMs (Ollama / llama.cpp / vLLM)**.

## Quick Start

```bash
# 1. Initialize Git
git init
git add .
git commit -m "chore: initialize apex-sales-playbook scaffold"

# 2. Rebuild all platform adapters (Master Gem, per-mode local prompts, Ollama Modelfile)
python3 scripts/build_adapters.py

# 3. Verify deterministic calculators & script linter
python3 tools/calculators.py --self-test

# 4. Run cross-model regression evals (requires promptfoo: npm i -g promptfoo)
npx promptfoo eval -c evals/promptfooconfig.yaml
```

## Directory Map

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` - Native entrypoints for coding/CLI agents.
- `core/` - Canonical router, intake protocol, 4-Gate diagnostic triage, and legal/accounting/vocal guardrails.
- `skills/` - Five portable `SKILL.md` modules (CFA/Offers, VSSL/Scripts, Recruiting/Bootcamp, Floor Ops, Transcript Audit).
- `tools/calculators.py` & `tools/mcp_server.py` - Deterministic financial math and spoken-script linter (CLI + MCP server).
- `schemas/` - JSON Schemas for 6-Line CRM Call Notes and BANT Scorecards.
- `adapters/` - Auto-compiled prompts for Gemini Gems / Custom GPTs, Ollama `Modelfile`, and lightweight single-mode prompts for 7B-32B local models.
- `evals/` - Cross-model `promptfoo` regression suite and synthetic fixtures.
- `sources/` - Gitignored local folder for private reference docs (never committed).
