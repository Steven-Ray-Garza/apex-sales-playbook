#!/usr/bin/env python3
"""Compile canonical core/ + skills/ into platform-specific adapters with lint checks.

Outputs:
  - adapters/master-gem-prompt.md         (Gemini Gems, Claude Projects, Custom GPTs)
  - adapters/system-prompts-by-mode/*.md  (Lightweight single-mode prompts for 7B-32B local LLMs)
  - adapters/ollama/Modelfile             (Ready-to-run Ollama Modelfile using core router + guardrails)

Also validates:
  - No corrupted/stripped math thresholds (blank spaces before 'minutes', 'calls', empty '()')
  - Pure ASCII punctuation in operators (no stray Unicode math arrows/inequalities)
  - Approximate token budgets per compiled adapter
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
SKILLS_DIR = REPO_ROOT / "skills"
ADAPTERS_DIR = REPO_ROOT / "adapters"

SKILL_ORDER = [
    "cfa-offer-architect",
    "vssl-script-engineer",
    "sales-recruiting-bootcamp",
    "sales-floor-director",
    "transcript-audit-mode",
]


def strip_frontmatter(md_text: str) -> str:
    return re.sub(r"^---\n.*?\n---\n+", "", md_text, flags=re.S).strip()


def approx_tokens(text: str) -> int:
    return max(1, round(len(text) / 4))


def lint_markdown(name: str, text: str) -> list[str]:
    issues: list[str] = []
    if re.search(r"\(\s*\)", text):
        issues.append(f"{name}: contains empty parentheses '()'")
    if re.search(r"  +(minutes|calls|of 1-year|long-form)", text):
        issues.append(f"{name}: suspicious double-space suggesting stripped threshold")
    for bad_char, label in [("\u2264", "<="), ("\u2265", ">="), ("\u2192", "->"), ("\u2014", "em-dash")]:
        if bad_char in text:
            issues.append(f"{name}: contains non-ASCII '{bad_char}' (replace with '{label}')")
    return issues


def build() -> int:
    router = (CORE_DIR / "router.md").read_text(encoding="utf-8").strip()
    guardrails = (CORE_DIR / "guardrails.md").read_text(encoding="utf-8").strip()

    all_issues: list[str] = []
    all_issues.extend(lint_markdown("core/router.md", router))
    all_issues.extend(lint_markdown("core/guardrails.md", guardrails))

    master_sections = [router, guardrails]
    by_mode_dir = ADAPTERS_DIR / "system-prompts-by-mode"
    by_mode_dir.mkdir(parents=True, exist_ok=True)

    for skill_name in SKILL_ORDER:
        skill_path = SKILLS_DIR / skill_name / "SKILL.md"
        raw = skill_path.read_text(encoding="utf-8")
        body = strip_frontmatter(raw)
        all_issues.extend(lint_markdown(f"skills/{skill_name}/SKILL.md", body))
        master_sections.append(body)

        single_mode = f"{router}\n\n{guardrails}\n\n---\n\n{body}\n"
        out_path = by_mode_dir / f"{skill_name}.md"
        out_path.write_text(single_mode, encoding="utf-8")
        print(f"Built {out_path.relative_to(REPO_ROOT)} (~{approx_tokens(single_mode)} tokens)")

    master_text = "\n\n---\n\n".join(master_sections) + "\n"
    master_out = ADAPTERS_DIR / "master-gem-prompt.md"
    master_out.write_text(master_text, encoding="utf-8")
    print(f"Built {master_out.relative_to(REPO_ROOT)} (~{approx_tokens(master_text)} tokens)")

    ollama_dir = ADAPTERS_DIR / "ollama"
    ollama_dir.mkdir(parents=True, exist_ok=True)
    ollama_system = f"{router}\n\n{guardrails}".replace('"""', '\\"\\"\\"')
    modelfile = (
        "# Build locally: ollama create apex-sales-router -f adapters/ollama/Modelfile\n"
        "# Swap base model as desired (e.g., qwen2.5:14b-instruct, llama3.3:70b, mistral-small)\n"
        "FROM qwen2.5:14b-instruct\n\n"
        "PARAMETER temperature 0.2\n"
        "PARAMETER num_ctx 16384\n"
        "PARAMETER repeat_penalty 1.05\n\n"
        'SYSTEM """\n'
        f"{ollama_system}\n"
        '"""\n'
    )
    modelfile_out = ollama_dir / "Modelfile"
    modelfile_out.write_text(modelfile, encoding="utf-8")
    print(f"Built {modelfile_out.relative_to(REPO_ROOT)} (~{approx_tokens(ollama_system)} system tokens)")

    if all_issues:
        print("\nLINT WARNINGS:")
        for issue in all_issues:
            print(f"  - {issue}")
        return 1

    print("\nALL ADAPTERS BUILT & LINTED CLEANLY.")
    return 0


if __name__ == "__main__":
    sys.exit(build())
