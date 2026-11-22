# Apex Revenue Operations Playbook (v4.0 - Clean-Room Model-Agnostic AI Repo)

One canonical, clean-room source of truth for running a **6-mode Acquisition & Revenue Operations system** across **Claude, Gemini, ChatGPT, and local LLMs (Ollama / llama.cpp / vLLM)** with deterministic Python unit-economics calculators and an MCP server.

## Architecture (Single Source of Truth)

| Directory / File | Role |
| :--- | :--- |
| `core/router.md` & `core/guardrails.md` | Shared role, Pre-Flight Intake, 4-Gate Triage, Mode 5/6 Fast-Tracks, and 7 Hard Operational Guardrails |
| `skills/*/SKILL.md` | 6 portable execution modules: `sfa-offer-architect`, `vsl-script-engineer`, `sales-recruiting-bootcamp`, `sales-floor-director`, `transcript-audit-mode`, `roleplay-sparring-partner` |
| `adapters/` | Auto-compiled prompts (`master-gem-prompt.md`, 6 standalone single-mode prompts with YAML frontmatter, Ollama `Modelfile`) built via `scripts/build_adapters.py` |
| `tools/calculators.py` & `tools/mcp_server.py` | Zero-dependency deterministic math (`sfa`, `offer-matrix`, `van-westendorp`, `ote` + legacy aliases), spoken-script linter (`lint-script`), and 5-tool MCP server |
| `schemas/` | Strict JSON Schemas (Draft 2020-12) for 6-Line CRM Call Notes and BANT Scorecards |
| `evals/` | 9-test cross-model `promptfoo` regression suite and synthetic call transcript fixture |
| `POWERSHELL_SOP.md` | End-to-end Windows PowerShell 5.1 operating manual |
| `.github/workflows/ci.yml` | Automated self-tests, adapter zero-drift check, schema validation, and Clean-Room IP/PII/Secret Leak Guard |

## Quick Start

```bash
python tools/calculators.py --self-test
python scripts/build_adapters.py
```

For full Windows PowerShell 5.1 instructions, see `POWERSHELL_SOP.md`.
