# Windows PowerShell 5.1 Operating Manual (`apex-sales-playbook` v3.1)

An end-to-end, beginner-friendly operating manual for running, editing, testing, and syncing your **6-mode `apex-sales-playbook` (v3.1)** repository from **Windows PowerShell 5.1** (`C:\Users\srgar\apex-sales-playbook`) with zero paid API keys required.

---

## 1. PowerShell 5.1 Survival Basics

PowerShell is a text-based remote control for Windows File Explorer. Instead of clicking folders and buttons, you type short commands and press **Enter**.

### Start Every Session the Same Way

1. Press the **Windows Key**, type `Windows PowerShell`, and press **Enter**.
2. Check the left side of the prompt: `PS C:\Users\srgar>` shows the folder you are currently standing in.
3. Move into your repository folder first:
   ```powershell
   Set-Location "$HOME\apex-sales-playbook"
   ```
   Confirm your prompt now reads `PS C:\Users\srgar\apex-sales-playbook>`. If you do not see `\apex-sales-playbook>` in the prompt, commands referencing `tools\`, `scripts\`, or `adapters\` will fail with a path error.

### The 5 Golden Rules of Windows PowerShell 5.1

1. **Always type `python`, never `python3`:** Most online guides assume macOS/Linux (`python3`). On Windows, use `python`.
2. **Never chain commands with `&&`:** PowerShell 5.1 rejects `&&`. Put each command on its own line.
3. **Use keyboard lifelines:**
   - `Up Arrow` / `Down Arrow`: Recall previous commands without retyping.
   - `Tab`: Auto-complete folder and file names (type `ad` then press `Tab` -> `.\adapters\`).
   - `Ctrl + C`: Emergency brake that stops any running or stuck command immediately.
   - `Ctrl + V` (or right-click): Paste copied commands into the terminal.
4. **Clear clutter anytime:** Type `cls` and press **Enter**.
5. **Avoid inline JSON quote bugs:** PowerShell 5.1 strips raw double quotes passed to external programs. All calculator blocks in Section 3 use clean PowerShell here-strings (`@' ... '@ | python -`) so Windows never mangles your quotes (and if you use CLI `--json`, use the `ConvertTo-Json -Depth 5 -Compress` + `-replace '"', '\"'` pattern).

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

## 2. Repository Map (v3.1): What to Edit vs. Never Touch

This repo uses a **single source of truth** design so Claude, Gemini, ChatGPT, and local models never drift out of sync.

| Path | Purpose | Rule |
| :--- | :--- | :--- |
| `core\router.md` & `core\guardrails.md` | Role, Pre-Flight Intake, 4-Gate Diagnostic Triage, Mode 5/6 Fast-Tracks, and all **7 Hard Guardrails** (source fidelity, founder proof gate, accounting/comp, vocal hygiene & zero-bloat audit, compliance, labor/TCPA/FTC/fulfillment circuit breakers, AI constraint & strategic judgment gate) | **EDIT HERE** for global rules |
| `skills\*\SKILL.md` | **Six modular playbooks:** `cfa-offer-architect`, `vssl-script-engineer`, `sales-recruiting-bootcamp`, `sales-floor-director`, `transcript-audit-mode` (5A-5D), and `roleplay-sparring-partner` (Mode 6) | **EDIT HERE** for mode-specific logic |
| `adapters\*` | Auto-compiled prompts (`master-gem-prompt.md`, 6 standalone single-mode prompts with YAML frontmatter preserved for 1-click Gemini Skill pasting, Ollama `Modelfile`) | **NEVER HAND-EDIT** - rebuilt by `scripts\build_adapters.py` |
| `tools\calculators.py` & `tools\mcp_server.py` | Deterministic math engine (`cfa`, `value-grid`, `van-westendorp`, `ote`), spoken-script linter (`lint-script`), and 5-tool MCP server | **RUN** via PowerShell or connect via MCP |
| `schemas\*.json` | JSON Schemas (Draft 2020-12) for 6-Line CRM Call Notes and BANT Scorecards | **REFERENCE** for structured CRM automation |
| `evals\*` | 9-test cross-model `promptfoo` suite and synthetic transcript fixture | **TEST** manually now or via `promptfoo` later |
| `.github\workflows\ci.yml` | Automated GitHub Actions tests, drift checks, schema validation, and leak guard | **AUTOMATIC** on every GitHub push |
| `sources\` & `transcripts\` | Local-only folders for private reference PDFs, verbatim word tracks, or real call transcripts | **NEVER COMMIT** - blocked by `.gitignore` and CI |

---

## 3. Day-to-Day Operational Workflows

Confirm your prompt shows `PS C:\Users\srgar\apex-sales-playbook>` before running any block below.

### Workflow A: Deterministic Financial & Pricing Math (Modes 1 & 3)

Verify the entire math engine (CFA, Value Grid, Van Westendorp, OTE/TAC, and Script Linter) anytime with:

```powershell
python tools\calculators.py --self-test
```

Expected output: `ALL SELF-TESTS PASSED`

#### 1. Full-Loaded CAC, GP, LTGP, PPD, 30D Cash & CFA Level

Edit the numbers inside `calc_cfa_metrics(...)` to match your business, then paste into PowerShell:

```powershell
@'
import json, sys
sys.path.insert(0, "tools")
from calculators import calc_cfa_metrics

result = calc_cfa_metrics(
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
        {"name": "Outreach", "ad_spend": 0, "media_creative_payroll": 3000, "software_cost": 200, "sales_salaries_commissions": 800, "new_customers": 8},
        {"name": "Paid Ads", "ad_spend": 20000, "media_creative_payroll": 4000, "software_cost": 1000, "sales_salaries_commissions": 10000, "new_customers": 10},
    ],
)
print(json.dumps(result, indent=2))
'@ | python -
```

*(For a transactional business, change `revenue_model="transactional"`, remove `monthly_churn_rate`, and pass `avg_lifetime_transactions=4`.)*

#### 2. Non-Linear Value Grid Blended 30D LTV

Computes gross and net 30D LTV per entering prospect after deducting real sales and lead-working labor costs:

```powershell
@'
import json, sys
sys.path.insert(0, "tools")
from calculators import calc_value_grid

result = calc_value_grid(
    entering_prospects=10,
    offers=[
        {"name": "Front-End Trial", "buyers": 8, "gp_30d_per_buyer": 75},
        {"name": "Core Upsell", "buyers": 3, "gp_30d_per_buyer": 1500},
    ],
    sales_and_lead_working_labor_cost=600,
)
print(json.dumps(result, indent=2))
'@ | python -
```

#### 3. Van Westendorp 4-Question Pricing Analysis (With Multi-Avatar Split Alert)

Computes exact `PMC` (marginal cheapness), `OPP` (optimal price point), `IDP` (indifference price point), `PME` (marginal expensiveness), Acceptable Price Range, Automated vs. High-Friction sales bands, and flags `>= 1.75x` double-Gaussian divergence across avatar segments:

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
print(json.dumps(result, indent=2))
'@ | python -
```

*(You can also run the same calculator directly via CLI: `python tools\calculators.py van-westendorp --json $payload` using the PowerShell JSON-escaped `$payload` pattern.)*

#### 4. 50/50 OTE Comp Plan, Backloaded Accelerators & 1-Year TAC Cap

Computes base/variable split, flat payout per close, backloaded monthly accelerator tiers, and the `<= 33.3%` (`3:1` minimum) 1-year Talent Acquisition Cost cap:

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
print(json.dumps(result, indent=2))
'@ | python -
```

*(For a pure self-gen outbound hunter, set `sales_motion="self_gen"` and pass `allowable_cac_per_deal=1200`.)*

> **Clipboard Tip:** Change the final line of any block above from `'@ | python -` to `'@ | python - | Set-Clipboard` to copy the exact JSON output directly into your Gemini, Claude, or ChatGPT chat.

---

### Workflow B: Lint Any Spoken Sales Script (Mode 2B Hygiene Gate)

Before deploying a phone script, verify Big Four recorded-line compliance, small-yes confirmation, `?` upward pitch inflection, `<= 340` pitch words (`<= 2 minutes` at `150-170 WPM`), required pause tags (`[short pause - 1-2 sec]`, `[medium pause - 3-4 sec]`, `[long pause - 8+ sec silence until prospect speaks]`), and zero `"totally understand, but"` anti-patterns.

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
   *(To measure the `<= 340` word limit strictly on the Pitch section, save just the Pitch to `transcripts\draft_pitch.txt` and run `python tools\calculators.py lint-script --file transcripts\draft_script.txt --pitch-file transcripts\draft_pitch.txt`.)*
4. Confirm `"passed": true`. If `"passed": false`, fix every item listed under `"failures"` and re-run.

---

### Workflow C: Call Intelligence, Transcript Audits, Flywheel & Handoffs (Mode 5A-5D)

All four Mode 5 workflows skip Pre-Flight Intake automatically when pasted into your **Apex of Sales & $100M Playbook (v3.1)** Gemini Gem, Claude Project, or CLI agent:

1. **Mode 5A - Pre-Call Kill-Mode Battle Card:** Paste raw BANT intake answers or setter notes before a live call to get a 30-second briefing (VSSL status, quantified gap hypotheses, 2 Pain-Cycle probes, predicted #1 objection + matched analogy, and morning-of proof arrow).
2. **Mode 5B - Post-Call Transcript Audit (Test Right Now):**
   ```powershell
   Get-Content evals\fixtures\sample_transcript.txt -Raw | Set-Clipboard
   ```
   Paste (`Ctrl + V`) into your v3.1 Gem and press **Enter** to generate **6-Line CRM Call Notes** + **BANT & Script Scorecard** + **One Behavior Focus (`"If this, then that"`)** + a **3-turn verbatim roleplay drill**.
   - *Real Calls:* Always store raw transcripts strictly inside `transcripts\` (never in tracked folders):
     ```powershell
     notepad transcripts\call_notes_raw.txt
     Get-Content transcripts\call_notes_raw.txt -Raw | Set-Clipboard
     ```
3. **Mode 5C - Weekly Marketing <-> Sales Flywheel:** Every Friday or Monday morning, paste the week's Mode 5B audit summaries to generate your 1-page Acquisition Brief (top 3 recurring floor objections formatted as Living VSSL splices, media-buyer BANT/lead-quality drift alert, verbatim buyer copy gold, and Friday huddle target).
4. **Mode 5D - 72-Hour Sales-to-Fulfillment Inoculation Handoff:** Paste a closed-deal transcript or 6-Line Call Notes to generate a 30-second delivery specialist kickoff brief, a transparent Day-0 welcome message, and the exact first quick-win referral trigger watchpoint.

---

### Workflow D: Live Interactive Roleplay & Interruption Sparring (Mode 6)

Mode 6 skips intake immediately and runs turn-by-turn live drills inside your v3.1 Gem (or standalone `roleplay-sparring-partner` skill) across three tiers:

- **Tier 1 - NPC Prospect (Script Memorization):** Cooperative prospect for locking in `Intro -> Disco -> Pitch -> Close` line-by-line with instant `[COACH FIX]` alerts if you miss a checkpoint.
- **Tier 2 - Pressure Prospect (Live Call Dogfight):** Guarded buyer throwing vague Disco answers and `2-4` stacked smoke screens/objections after the price ask. Type `COACH` or `STOP` anytime for an Eyes-and-Ears debrief.
- **Tier 3 - Technical Interviewer (30-40x Interruption Drill):** Simulates the hiring Sales Manager interrupting every 1-2 turns to test agility and rate of learning.

**Example Kickoff Prompt:**
> `Run Mode 6 Tier 2 Pressure Prospect. I sell a $5,000 B2B lead-gen system. Start at the top of the Close right after I ask for the $5,000.`

---

### Workflow E: Edit Playbook Rules & Sync Every AI Platform (Zero Drift)

Whenever you refine any rule, threshold, or workflow, follow this exact 4-step loop:

1. **Edit the canonical file** under `core\` or `skills\` (never inside `adapters\`):
   ```powershell
   notepad core\guardrails.md
   ```
   Save (`Ctrl + S`) and close Notepad.
2. **Rebuild and lint all 6-mode platform adapters (writes clean LF endings & preserves YAML frontmatter):**
   ```powershell
   python scripts\build_adapters.py
   ```
   Confirm you see `ALL ADAPTERS BUILT & LINTED CLEANLY.`
3. **Copy the compiled prompt straight to your clipboard (always use `-Raw` to preserve exact line breaks):**
   - **Standalone Master Gem / Claude Project / Custom GPT:**
     ```powershell
     Get-Content adapters\master-gem-prompt.md -Raw | Set-Clipboard
     ```
   - **All 6 Standalone Gem Skills (YAML frontmatter `name` / `description` is now included automatically):**
     ```powershell
     Get-Content adapters\system-prompts-by-mode\cfa-offer-architect.md -Raw | Set-Clipboard
     Get-Content adapters\system-prompts-by-mode\vssl-script-engineer.md -Raw | Set-Clipboard
     Get-Content adapters\system-prompts-by-mode\sales-recruiting-bootcamp.md -Raw | Set-Clipboard
     Get-Content adapters\system-prompts-by-mode\sales-floor-director.md -Raw | Set-Clipboard
     Get-Content adapters\system-prompts-by-mode\transcript-audit-mode.md -Raw | Set-Clipboard
     Get-Content adapters\system-prompts-by-mode\roleplay-sparring-partner.md -Raw | Set-Clipboard
     ```
4. **Paste** (`Ctrl + V`) into your Gemini Gem **Instructions** box (or Gemini Skill Management body), click **Save**, and open a **fresh chat** so the updated instructions take effect.

---

### Workflow F: Managing & Verifying Your Private Local `sources\` Vault

Keep purchased books, verbatim third-party transcripts, and your local `apex-sales-word-track-playbook.md` strictly inside `sources\` (never committed to GitHub). Prefer `.pdf` (one copy per source) inside `sources\` for local CLI agents, and keep your native Google Docs attached privately in Gemini Gem Knowledge.

Verify 100% `.gitignore` shielding anytime with:

```powershell
Set-Location "$HOME\apex-sales-playbook"
Get-ChildItem sources
git ls-files sources/
git status --ignored -s sources/
```

- **`Get-ChildItem sources`:** Lists the private files sitting locally on your hard drive.
- **`git ls-files sources/`:** Must print **ONLY** `sources/.gitkeep` (proving zero private files will upload to GitHub).
- **`git status --ignored -s sources/`:** Prints `!!` in front of every private file in `sources\` (`!!` means Git is actively ignoring it and will never upload it).

---

## 4. Git & GitHub Daily Save-and-Ship SOP

Think of Git as a video-game save system: **edit -> test -> check status -> stage (`add`) -> save checkpoint (`commit`) -> upload backup (`push`)**.

### Standard Save & Push Routine

Run these lines one at a time inside `C:\Users\srgar\apex-sales-playbook`:

```powershell
python tools\calculators.py --self-test
python scripts\build_adapters.py
git status
```

Inspect `git status` to verify only intended files appear (never `.pdf`, `.gdoc`, `.docx`, `.env`, `sources\*`, or `transcripts\*`). Then commit and push:

```powershell
git add .
git commit -m "chore: update playbook and rebuild adapters"
git push
```

### Verify Your Automated GitHub CI Gate

1. Open `https://github.com/Steven-Ray-Garza/apex-sales-playbook` and click the **Actions** tab.
2. Wait ~20-30 seconds for **Apex Sales Playbook CI** (`Build, Test, Schema & Leak Guard`) to show a green checkmark.
3. Every push automatically validates:
   - Calculator self-tests (CFA, Value Grid, Van Westendorp, OTE/TAC, Script Linter) and `mcp_server.py` syntax
   - Zero drift between `core/` + `skills/` and `adapters/`
   - JSON Schema (Draft 2020-12) and 9-test `evals/promptfooconfig.yaml` validity
   - Copyright, PII, and secret leak protection (blocks forbidden extensions, `sources/` or `transcripts/` files, publisher copyright notices, non-distribution markers, API keys, SSNs, and unredacted phone numbers)

### Beginner Undo & Safety Commands

- **Check which version is compiled locally:**
  ```powershell
  Select-String -Path "adapters\master-gem-prompt.md" -Pattern "Playbook \(v"
  ```
- **Confirm a specific file was committed and pushed:**
  ```powershell
  git log -n 3 --oneline -- POWERSHELL_SOP.md
  git status
  ```
- **Inspect unsaved edits before committing:**
  ```powershell
  git diff
  ```
- **Restore one accidentally broken file back to your last saved commit:**
  ```powershell
  git checkout -- core\guardrails.md
  ```
- **View your last 5 saved checkpoints:**
  ```powershell
  git log --oneline -n 5
  ```

### Recommended Privacy Lock

Keep your GitHub repository **Private** for internal business operations:

1. Open `https://github.com/Steven-Ray-Garza/apex-sales-playbook/settings`.
2. Scroll to **Danger Zone** at the bottom.
3. Click **Change visibility** -> **Change to private** -> confirm.

---

## 5. Connecting AI Tools (CLI Agents, MCP & Optional Local Models)

### A. CLI Agents (Codex, Claude Code, Gemini CLI)

Always enter your repository folder **before** starting your CLI agent so it discovers `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md` automatically:

```powershell
Set-Location "$HOME\apex-sales-playbook"
```

To conserve tokens, instruct the agent to load only the single skill file needed (for example: *"Read only `skills/vssl-script-engineer/SKILL.md` and write a 4-step BAMFAM follow-up text cadence"*).

### B. Deterministic MCP Server (`tools\mcp_server.py`)

`mcp` is already installed on your machine. Do **not** launch `python tools\mcp_server.py` directly in PowerShell - register it inside your AI client's MCP config file (such as Claude Desktop's `%APPDATA%\Claude\claude_desktop_config.json` or Cursor's `.cursor\mcp.json`) so the client starts it automatically:

```json
{
  "mcpServers": {
    "apex-sales-playbook": {
      "command": "python",
      "args": ["C:\\Users\\srgar\\apex-sales-playbook\\tools\\mcp_server.py"]
    }
  }
}
```

This gives your AI client **5 deterministic tools**: `cfa_unit_economics`, `value_grid_ltv`, `van_westendorp_pricing`, `ote_and_tac_calculator`, and `script_hygiene_linter`.

### C. Optional Future Upgrades (Skip Until Needed)

- **Offline Local LLMs (Ollama):** If you install Ollama later, build your lean local router with:
  ```powershell
  ollama pull qwen2.5:14b-instruct
  ollama create apex-sales-router -f adapters\ollama\Modelfile
  ollama run apex-sales-router
  ```
- **Automated Cross-Model Evals (`promptfoo`):** Leave skipped until you attach either Ollama or cloud API keys (`npx promptfoo eval -c evals/promptfooconfig.yaml` runs all 9 regression tests).

---

## 6. Troubleshooting Cheat Sheet

| Error Message | Cause | Exact Fix |
| :--- | :--- | :--- |
| `The term 'python3' is not recognized` | Used macOS/Linux command on Windows | Use `python` instead of `python3` |
| `The token '&&' is not a valid statement separator` | PowerShell 5.1 does not support `&&` | Run each command on its own line |
| `Cannot find path` / `No such file` | You are in `C:\Users\srgar` instead of the repo | Run `Set-Location "$HOME\apex-sales-playbook"` |
| `Missing expression after unary operator '!'` | Accidentally typed `!! filename` example output as a command | Ignore - `!!` is `git status --ignored` output, not a command |
| `json.decoder.JSONDecodeError` on CLI `--json` | Passed raw `'{"a":1}'` in PowerShell 5.1 | Use the `@' ... '@ \| python -` here-string blocks in Section 3A |
| `warning: LF will be replaced by CRLF` | Normal Windows line-ending normalization | Ignore - completely harmless |
| `ERROR: adapters/ is out of sync` (GitHub Actions) | Edited `core/` or `skills/` without rebuilding | Run `python scripts\build_adapters.py`, then `git add .`, `git commit`, `git push` |
| `LEAK GUARD FAILED` (GitHub Actions) | Staged a forbidden file, copyright notice, secret, or phone number | Move private files to `sources\` or `transcripts\`, run `git rm --cached <file>`, commit, and push |
| `remote origin already exists` | Ran `git remote add origin` twice | Use `git remote set-url origin https://github.com/Steven-Ray-Garza/apex-sales-playbook.git` |
| Terminal appears frozen | Waiting on input or background process | Press `Ctrl + C` twice to return to your prompt |

---

## 7. 7-Day Verification Drill

Run this 3-minute drill once today to verify every v3.1 component end-to-end:

1. `Set-Location "$HOME\apex-sales-playbook"`
2. `python tools\calculators.py --self-test` (verify `ALL SELF-TESTS PASSED`)
3. `git ls-files sources/` (verify output is ONLY `sources/.gitkeep`)
4. Run the `calc_van_westendorp` block in Section 3A (confirm `multi_avatar_alert` fires cleanly).
5. Run `Get-Content evals\fixtures\sample_transcript.txt -Raw | Set-Clipboard`, paste into your **Apex of Sales & $100M Playbook (v3.1)** Gemini Gem, and verify it skips intake and outputs 6-Line CRM Call Notes + BANT grading + a 3-turn roleplay drill.

**7-Day Leading Indicator:** Track **100% single-source sync compliance** over the next `7 days` - every edit to a rule or script starts in `core\` or `skills\`, passes `python scripts\build_adapters.py`, syncs via `Get-Content ... -Raw | Set-Clipboard`, and lands with a green checkmark in GitHub Actions.
