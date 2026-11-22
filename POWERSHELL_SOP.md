# Windows PowerShell 5.1 Operating Manual (`apex-sales-playbook` v4.0)

An end-to-end, beginner-friendly operating manual for running, editing, testing, and syncing your **6-mode `apex-sales-playbook` (v4.0 Clean-Room)** repository from **Windows PowerShell 5.1** (`$HOME\apex-sales-playbook`) with zero paid API keys required.

---

## 1. PowerShell 5.1 Survival Basics

PowerShell is a text-based remote control for Windows File Explorer. Instead of clicking folders and buttons, you type short commands and press **Enter**.

### Start Every Session the Same Way

1. Press the **Windows Key**, type `Windows PowerShell`, and press **Enter**.
2. Check the left side of the prompt: `PS C:\Users\<YOUR_USER>>` shows the folder you are currently standing in.
3. Move into your repository folder first:
   ```powershell
   Set-Location "$HOME\apex-sales-playbook"
   ```
   Confirm your prompt now ends with `\apex-sales-playbook>`. If you do not see `\apex-sales-playbook>` in the prompt, commands referencing `tools\`, `scripts\`, or `adapters\` will fail with a path error.

### The 5 Golden Rules of Windows PowerShell 5.1

1. **Always type `python`, never `python3`:** Most online guides assume macOS/Linux (`python3`). On Windows, use `python`.
2. **Never chain commands with `&&`:** PowerShell 5.1 rejects `&&`. Put each command on its own line.
3. **Use keyboard lifelines:**
   - `Up Arrow` / `Down Arrow`: Recall previous commands without retyping.
   - `Tab`: Auto-complete folder and file names (type `ad` then press `Tab` -> `.\adapters\`).
   - `Ctrl + C`: Emergency brake that stops any running or stuck command immediately.
   - `Ctrl + V` (or right-click): Paste copied commands into the terminal.
4. **Clear clutter anytime:** Type `cls` and press **Enter**.
5. **Avoid inline JSON quote bugs:** PowerShell 5.1 strips raw double quotes passed to external programs. All calculator blocks in Section 3 use clean PowerShell here-strings (`@' ... '@ | python -`) so Windows never mangles your quotes.

### The Only 10 PowerShell Commands You Need

| Command | Plain-English Meaning | Example |
| :--- | :--- | :--- |
| `Set-Location` (or `cd`) | Move into a folder | `cd "$HOME\apex-sales-playbook"` |
| `Get-ChildItem` (or `ls`) | List files in the current folder | `Get-ChildItem skills` |
| `Get-Content` | Display a file's text on screen | `Get-Content README.md` |
| `Set-Clipboard` | Copy output to Windows clipboard | `Get-Content README.md -Raw \| Set-Clipboard` |
| `notepad <file>` | Open a file in Notepad to edit | `notepad core\router.md` |
| `New-Item -ItemType Directory` | Create a folder | `New-Item -ItemType Directory -Force transcripts` |
| `cls` | Clear the terminal window | `cls` |
| `git status` | Show which files changed since last save | `git status` |
| `git diff` | Inspect your exact line-by-line edits | `git diff` |
| `Ctrl + C` | Cancel a running command | *(Keyboard shortcut)* |

---

## 2. Repository Map (v4.0 Clean-Room): What to Edit vs. Never Touch

This repo uses a **single source of truth** design so Claude, Gemini, ChatGPT, and local models never drift out of sync.

| Path | Purpose | Rule |
| :--- | :--- | :--- |
| `core\router.md` & `core\guardrails.md` | Role, Pre-Flight Intake, 4-Gate Diagnostic Triage, Mode 5/6 Fast-Tracks, and all **7 Hard Operational Guardrails** | **EDIT HERE** for global rules |
| `skills\*\SKILL.md` | **Six modular playbooks:** `sfa-offer-architect`, `vsl-script-engineer`, `sales-recruiting-bootcamp`, `sales-floor-director`, `transcript-audit-mode` (5A-5D), and `roleplay-sparring-partner` (Mode 6) | **EDIT HERE** for mode-specific logic |
| `adapters\*` | Auto-compiled prompts (`master-gem-prompt.md`, 6 standalone single-mode prompts with YAML frontmatter preserved for 1-click Gemini Skill pasting, Ollama `Modelfile`) | **NEVER HAND-EDIT** - rebuilt by `scripts\build_adapters.py` |
| `tools\calculators.py` & `tools\mcp_server.py` | Hardened deterministic math engine (`sfa`, `offer-matrix`, `van-westendorp`, `ote` + legacy aliases `cfa`/`value-grid`), spoken-script linter (`lint-script`), and 5-tool MCP server | **RUN** via PowerShell or connect via MCP |
| `schemas\*.json` | JSON Schemas (Draft 2020-12) for 6-Line CRM Call Notes and BANT Scorecards | **REFERENCE** for structured CRM automation |
| `evals\*` | 9-test cross-model `promptfoo` suite and synthetic transcript fixture | **TEST** manually now or via `promptfoo` later |
| `.github\workflows\ci.yml` | Automated GitHub Actions tests, drift checks, schema validation, and Clean-Room IP/PII/Secret Leak Guard | **AUTOMATIC** on every GitHub push |
| `LICENSE`, `NOTICE.md`, `SECURITY.md` | Governance, clean-room IP independence statement, and security/compliance policy | **MAINTAIN** for audit readiness |
| `sources\` & `transcripts\` | Local-only folders for private reference PDFs, personal study notes, or real call transcripts | **NEVER COMMIT** - blocked by `.gitignore` and CI |

---

## 3. Day-to-Day Operational Workflows

Confirm your prompt ends with `\apex-sales-playbook>` before running any block below.

### Workflow A: Deterministic Financial & Pricing Math (Modes 1 & 3)

Verify the entire math engine (SFA, Offer Matrix, Van Westendorp, OTE/TAC, Script Linter, plus strict RFC-8259 JSON and negative-input bounds checks) anytime with:

```powershell
python tools\calculators.py --self-test
```

Expected output: `ALL SELF-TESTS PASSED`

#### 1. Full-Loaded CAC, GP, LTGP, PPD, 30D Cash & SFA Payback Tier

```powershell
@'
import json, sys
sys.path.insert(0, "tools")
from calculators import calc_sfa_metrics

result = calc_sfa_metrics(
    price=3000,
    direct_fulfillment_cost=600,
    ad_spend=20000,
    media_creative_payroll=4000,
    software_cost=1000,
    sales_salaries_commissions=10000,
    new_customers=10,
    revenue_model="recurring",
    monthly_churn_rate=0.05,
    gp_30d=7500,
    channels=[
        {"name": "Outbound", "ad_spend": 0, "media_creative_payroll": 3000, "software_cost": 200, "sales_salaries_commissions": 800, "new_customers": 8},
        {"name": "Paid Media", "ad_spend": 20000, "media_creative_payroll": 4000, "software_cost": 1000, "sales_salaries_commissions": 10000, "new_customers": 10},
    ],
)
print(json.dumps(result, indent=2, allow_nan=False))
'@ | python -
```

*(For a transactional business, change `revenue_model="transactional"`, remove `monthly_churn_rate`, and pass `avg_lifetime_transactions=4`.)*

#### 2. Non-Linear Offer Matrix Blended 30D LTV

```powershell
@'
import json, sys
sys.path.insert(0, "tools")
from calculators import calc_offer_matrix

result = calc_offer_matrix(
    entering_prospects=10,
    offers=[
        {"name": "Entry Trial", "buyers": 8, "gp_30d_per_buyer": 75},
        {"name": "Core Upsell", "buyers": 3, "gp_30d_per_buyer": 1500},
    ],
    sales_and_lead_working_labor_cost=600,
)
print(json.dumps(result, indent=2, allow_nan=False))
'@ | python -
```

#### 3. Van Westendorp 4-Question Pricing Analysis (With Multi-Avatar Split Alert)

```powershell
@'
import json, sys
sys.path.insert(0, "tools")
from calculators import calc_van_westendorp

result = calc_van_westendorp(
    segment_field="segment",
    responses=[
        {"segment": "smb", "too_cheap": 500, "bargain": 1000, "expensive": 2000, "too_expensive": 3000},
        {"segment": "smb", "too_cheap": 600, "bargain": 1200, "expensive": 2200, "too_expensive": 3500},
        {"segment": "enterprise", "too_cheap": 3000, "bargain": 6000, "expensive": 12000, "too_expensive": 18000},
        {"segment": "enterprise", "too_cheap": 4000, "bargain": 8000, "expensive": 15000, "too_expensive": 22000},
    ],
)
print(json.dumps(result, indent=2, allow_nan=False))
'@ | python -
```

#### 4. 50/50 OTE Comp Plan, Backloaded Accelerators & 1-Year TAC Cap

```powershell
@'
import json, sys
sys.path.insert(0, "tools")
from calculators import calc_ote_and_tac

result = calc_ote_and_tac(
    sales_motion="inbound",
    ote_annual=100000,
    expected_weekly_closes=12,
    working_weeks_per_year=50,
    annual_rep_gp=250000,
    activation_rate=0.5,
)
print(json.dumps(result, indent=2, allow_nan=False))
'@ | python -
```

> **Clipboard Tip:** Change the final line of any block above from `'@ | python -` to `'@ | python - | Set-Clipboard` to copy strict JSON directly into Gemini, Claude, or ChatGPT.

---

### Workflow B: Lint Any Spoken Sales Script (Mode 2B Hygiene Gate)

1. Create your private, gitignored `transcripts` folder (one-time setup):
   ```powershell
   New-Item -ItemType Directory -Force transcripts | Out-Null
   ```
2. Open a draft script in Notepad, paste your script, press `Ctrl + S`, and close Notepad:
   ```powershell
   notepad transcripts\draft_script.txt
   ```
3. Run the deterministic linter:
   ```powershell
   python tools\calculators.py lint-script --file transcripts\draft_script.txt
   ```
4. Confirm `"passed": true`. If `"passed": false`, fix every item listed under `"failures"` and re-run.

---

### Workflow C: Call Intelligence, Transcript Audits, Flywheel & Handoffs (Mode 5A-5D)

All four Mode 5 workflows skip Pre-Flight Intake automatically when pasted into your **Apex Revenue Operations Playbook (v4.0)** Gemini Gem, Claude Project, or CLI agent:

1. **Mode 5A - Pre-Call Kill-Mode Battle Card:** Paste raw BANT intake answers or setter notes before a live call for a 30-second briefing.
2. **Mode 5B - Post-Call Transcript Audit (Test Right Now):**
   ```powershell
   Get-Content evals\fixtures\sample_transcript.txt -Raw | Set-Clipboard
   ```
   Paste (`Ctrl + V`) into your v4.0 Gem and press **Enter** to generate **6-Line CRM Call Notes** + **BANT & Script Scorecard** + **One Behavior Focus (`"If this, then that"`)** + a **3-turn roleplay drill**.
3. **Mode 5C - Weekly Marketing <-> Sales Flywheel:** Paste the week's Mode 5B audit summaries to generate your Monday Acquisition Brief (top 3 floor objections formatted as Living VSL splices, BANT drift alert, verbatim buyer copy, Friday huddle target).
4. **Mode 5D - 72-Hour Sales-to-Fulfillment Inoculation Handoff:** Paste a closed-deal transcript or 6-Line Call Notes for a delivery kickoff brief, Day-0 welcome message, and referral trigger watchpoint.

---

### Workflow D: Live Interactive Roleplay & Interruption Sparring (Mode 6)

Mode 6 skips intake immediately across three tiers (**Tier 1 Cooperative Practice Buyer**, **Tier 2 Pressure Buyer**, **Tier 3 High-Frequency Interruption Interviewer**).

**Example Kickoff Prompt:**
> `Run Mode 6 Tier 2 Pressure Buyer. I sell a $5,000 B2B lead-gen system. Start at the top of the Close right after I ask for the $5,000.`

---

### Workflow E: Edit Playbook Rules & Sync Every AI Platform (Zero Drift)

1. Edit the canonical file under `core\` or `skills\` (never inside `adapters\`):
   ```powershell
   notepad core\guardrails.md
   ```
2. Rebuild and lint all 6-mode platform adapters:
   ```powershell
   python scripts\build_adapters.py
   ```
   Confirm you see `ALL ADAPTERS BUILT & LINTED CLEANLY.`
3. Copy the compiled prompt to your clipboard (always use `-Raw`):
   - **Standalone Master Gem / Claude Project / Custom GPT:**
     ```powershell
     Get-Content adapters\master-gem-prompt.md -Raw | Set-Clipboard
     ```
   - **All 6 Standalone Gem Skills (YAML frontmatter included automatically):**
     ```powershell
     Get-Content adapters\system-prompts-by-mode\sfa-offer-architect.md -Raw | Set-Clipboard
     Get-Content adapters\system-prompts-by-mode\vsl-script-engineer.md -Raw | Set-Clipboard
     Get-Content adapters\system-prompts-by-mode\sales-recruiting-bootcamp.md -Raw | Set-Clipboard
     Get-Content adapters\system-prompts-by-mode\sales-floor-director.md -Raw | Set-Clipboard
     Get-Content adapters\system-prompts-by-mode\transcript-audit-mode.md -Raw | Set-Clipboard
     Get-Content adapters\system-prompts-by-mode\roleplay-sparring-partner.md -Raw | Set-Clipboard
     ```
4. Paste (`Ctrl + V`) into your Gem **Instructions** box (or Skill Management body), save, and start a **fresh chat**.

---

### Workflow F: Managing & Verifying Your Private Local `sources\` Vault

Verify 100% `.gitignore` shielding anytime with:

```powershell
Set-Location "$HOME\apex-sales-playbook"
Get-ChildItem sources
git ls-files sources/
git status --ignored -s sources/
```

- `git ls-files sources/` must print **ONLY** `sources/.gitkeep`.
- `git status --ignored -s sources/` prints `!!` in front of every ignored local file.

---

## 4. Git & GitHub Daily Save-and-Ship SOP

```powershell
python tools\calculators.py --self-test
python scripts\build_adapters.py
git status
git add -A
git commit -m "chore: update playbook and rebuild adapters"
git push
```

Confirm the green checkmark under your repository's **Actions** tab (`Build, Test, Schema & Clean-Room IP/PII Guard`).

---

## 5. Connecting AI Tools (CLI Agents, MCP & Optional Local Models)

### A. CLI Agents (Codex, Claude Code, Gemini CLI)

```powershell
Set-Location "$HOME\apex-sales-playbook"
```

### B. Deterministic MCP Server (`tools\mcp_server.py`)

Register in your AI client's MCP config file (replacing `<YOUR_USER>` with your Windows username):

```json
{
  "mcpServers": {
    "apex-sales-playbook": {
      "command": "python",
      "args": ["C:\\Users\\<YOUR_USER>\\apex-sales-playbook\\tools\\mcp_server.py"]
    }
  }
}
```

Exposes **5 deterministic tools**: `sfa_unit_economics`, `offer_matrix_ltv`, `van_westendorp_pricing`, `ote_and_tac_calculator`, and `script_hygiene_linter`.

### C. Optional Future Upgrades (Skip Until Needed)

- **Offline Local LLMs (Ollama):**
  ```powershell
  ollama pull qwen2.5:14b-instruct
  ollama create apex-sales-router -f adapters\ollama\Modelfile
  ollama run apex-sales-router
  ```
- **Automated Cross-Model Evals (`promptfoo`):** `npx promptfoo eval -c evals/promptfooconfig.yaml`

---

## 6. Troubleshooting Cheat Sheet

| Error Message | Cause | Exact Fix |
| :--- | :--- | :--- |
| `The term 'python3' is not recognized` | Used macOS/Linux command on Windows | Use `python` instead of `python3` |
| `The token '&&' is not a valid statement separator` | PowerShell 5.1 does not support `&&` | Run each command on its own line |
| `Cannot find path` / `No such file` | Standing outside repo root | Run `Set-Location "$HOME\apex-sales-playbook"` |
| `Missing expression after unary operator '!'` | Typed `!!` example output as a command | Ignore - `!!` is `git status --ignored` output |
| `ERROR: adapters/ is out of sync` (GitHub Actions) | Edited `core/` or `skills/` without rebuilding | Run `python scripts\build_adapters.py`, commit, and push |
| `CLEAN-ROOM LEAK GUARD FAILED` (GitHub Actions) | Staged forbidden file, third-party mark, hardcoded path, secret, or phone number | Move private files to `sources\` or `transcripts\`, scrub the flagged line, commit, and push |
| Terminal appears frozen | Waiting on input or background process | Press `Ctrl + C` twice |

---

## 7. 7-Day Verification Drill

1. `Set-Location "$HOME\apex-sales-playbook"`
2. `python tools\calculators.py --self-test` (confirm `ALL SELF-TESTS PASSED`)
3. `git ls-files sources/` (confirm output is **ONLY** `sources/.gitkeep`)
4. Run `calc_van_westendorp` in Section 3A (confirm `multi_avatar_alert` fires cleanly).
5. Run `Get-Content evals\fixtures\sample_transcript.txt -Raw | Set-Clipboard`, paste into your **Apex Revenue Operations Playbook (v4.0)** Gemini Gem, and verify instant 6-Line CRM Call Notes + BANT grading + 3-turn roleplay drill.

**7-Day Leading Indicator:** Maintain **100% Clean-Room CI pass rate** (`0` IP/PII alerts, `0` adapter drift, `100%` strict-JSON calculator tests) on every push over the next `7 days`.
