#!/usr/bin/env python3
"""Deterministic financial math and spoken-script linter for Apex Sales Playbook.

Zero external dependencies (Python 3.10+ stdlib only) so any agent, CLI, MCP server,
or local LLM runner can execute exact unit economics without hallucinated math.

Usage examples:
  python3 tools/calculators.py --self-test
  python3 tools/calculators.py cfa --json '{"price":3000,"direct_fulfillment_cost":600,"ad_spend":20000,"media_creative_payroll":4000,"software_cost":1000,"sales_salaries_commissions":10000,"new_customers":10,"revenue_model":"recurring","monthly_churn_rate":0.05,"gp_30d":7500}'
  python3 tools/calculators.py value-grid --json '{"entering_prospects":10,"offers":[{"name":"Trial + Core","buyers":8,"gp_30d_per_buyer":75}],"sales_and_lead_working_labor_cost":600}'
  python3 tools/calculators.py ote --json '{"sales_motion":"inbound","ote_annual":100000,"expected_weekly_closes":12,"annual_rep_gp":250000,"activation_rate":0.5}'
  python3 tools/calculators.py lint-script --file path/to/script.txt
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def calc_cfa_metrics(
    *,
    price: float,
    direct_fulfillment_cost: float,
    ad_spend: float,
    media_creative_payroll: float = 0.0,
    software_cost: float = 0.0,
    sales_salaries_commissions: float = 0.0,
    new_customers: int,
    revenue_model: str = "recurring",
    monthly_churn_rate: float | None = None,
    avg_lifetime_transactions: float | None = None,
    gp_30d: float | None = None,
    channels: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Calculate Full-Loaded CAC, GP, Gross Margin, LTGP, PPD, 30D Cash, and CFA Level."""
    if new_customers <= 0:
        raise ValueError("new_customers must be > 0")
    if price <= 0:
        raise ValueError("price must be > 0")

    total_acq_spend = (
        ad_spend + media_creative_payroll + software_cost + sales_salaries_commissions
    )
    cac = total_acq_spend / new_customers
    gp = price - direct_fulfillment_cost
    gross_margin = gp / price

    model = revenue_model.strip().lower()
    if model == "recurring":
        if monthly_churn_rate is None or not (0 < monthly_churn_rate <= 1):
            raise ValueError("monthly_churn_rate must be in (0, 1] for recurring models")
        ltgp = gp / monthly_churn_rate
        effective_30d_gp = gp if gp_30d is None else gp_30d
        payback_months = cac / gp if gp > 0 else float("inf")
    elif model == "transactional":
        if avg_lifetime_transactions is None or avg_lifetime_transactions <= 0:
            raise ValueError("avg_lifetime_transactions must be > 0 for transactional models")
        ltgp = gp * avg_lifetime_transactions
        effective_30d_gp = gp if gp_30d is None else gp_30d
        payback_months = 1.0 if effective_30d_gp >= cac else (
            cac / effective_30d_gp if effective_30d_gp > 0 else float("inf")
        )
    else:
        raise ValueError("revenue_model must be 'recurring' or 'transactional'")

    ltgp_to_cac = ltgp / cac if cac > 0 else float("inf")
    gp_30d_to_cac = effective_30d_gp / cac if cac > 0 else float("inf")

    if effective_30d_gp > 2.0 * cac:
        cfa_level = 3
        cfa_label = "CFA Level 3 (30D GP > 2x CAC: Self-Compounding Growth)"
        fulfillment_brake_alert = (
            "TRIGGER GUARDRAIL #6: Operations/fulfillment is now the growth constraint. "
            "Model fixed overhead step-functions, delivery headcount, refund reserves, and net EBITDA before scaling spend."
        )
    elif effective_30d_gp >= cac:
        cfa_level = 2
        cfa_label = "CFA Level 2 (30D GP >= CAC: Credit-Card Self-Liquidating)"
        fulfillment_brake_alert = None
    else:
        cfa_level = 1
        cfa_label = "CFA Level 1 (30D GP < CAC: Requires Outside Capital/Float)"
        fulfillment_brake_alert = None

    channel_breakdown = []
    if channels:
        for ch in channels:
            ch_cust = int(ch["new_customers"])
            ch_spend = (
                float(ch.get("ad_spend", 0.0))
                + float(ch.get("media_creative_payroll", 0.0))
                + float(ch.get("software_cost", 0.0))
                + float(ch.get("sales_salaries_commissions", 0.0))
            )
            ch_cac = ch_spend / ch_cust if ch_cust > 0 else float("inf")
            channel_breakdown.append({
                "channel": ch["name"],
                "total_spend": round(ch_spend, 2),
                "new_customers": ch_cust,
                "cac": round(ch_cac, 2),
            })
        channel_breakdown.sort(key=lambda x: x["cac"])

    level3_compounding_12mo = [
        {"month": m, "new_customers": 2 ** (m - 1), "total_customers": (2 ** m) - 1}
        for m in range(1, 13)
    ]

    return {
        "inputs": {
            "price": price,
            "direct_fulfillment_cost": direct_fulfillment_cost,
            "total_acquisition_spend": round(total_acq_spend, 2),
            "new_customers": new_customers,
            "revenue_model": model,
        },
        "metrics": {
            "full_loaded_cac": round(cac, 2),
            "gross_profit_per_unit": round(gp, 2),
            "gross_margin_pct": round(gross_margin * 100, 2),
            "ltgp": round(ltgp, 2),
            "ltgp_to_cac_ratio": round(ltgp_to_cac, 2),
            "payback_period_months": round(payback_months, 2),
            "cash_30d_gp": round(effective_30d_gp, 2),
            "cash_30d_to_cac_ratio": round(gp_30d_to_cac, 2),
        },
        "cfa_level": cfa_level,
        "cfa_label": cfa_label,
        "fulfillment_brake_alert": fulfillment_brake_alert,
        "channel_cac_ranked": channel_breakdown,
        "level3_compounding_reference": level3_compounding_12mo if cfa_level == 3 else None,
    }


def calc_value_grid(
    *,
    entering_prospects: int,
    offers: list[dict[str, Any]],
    sales_and_lead_working_labor_cost: float = 0.0,
) -> dict[str, Any]:
    """Compute non-linear Value Grid blended 30D GP/LTV net of sales & lead-working labor."""
    if entering_prospects <= 0:
        raise ValueError("entering_prospects must be > 0")

    offer_rows = []
    gross_30d_gp = 0.0
    for offer in offers:
        buyers = float(offer["buyers"])
        gp_per_buyer = float(offer["gp_30d_per_buyer"])
        subtotal = buyers * gp_per_buyer
        gross_30d_gp += subtotal
        offer_rows.append({
            "offer": offer["name"],
            "buyers": buyers,
            "take_rate_pct": round((buyers / entering_prospects) * 100, 2),
            "gp_30d_per_buyer": round(gp_per_buyer, 2),
            "subtotal_30d_gp": round(subtotal, 2),
        })

    net_30d_gp = gross_30d_gp - sales_and_lead_working_labor_cost
    gross_per_prospect = gross_30d_gp / entering_prospects
    net_per_prospect = net_30d_gp / entering_prospects

    return {
        "entering_prospects": entering_prospects,
        "offers": offer_rows,
        "gross_30d_gp_total": round(gross_30d_gp, 2),
        "sales_and_lead_working_labor_cost": round(sales_and_lead_working_labor_cost, 2),
        "net_30d_gp_total": round(net_30d_gp, 2),
        "gross_30d_ltv_per_prospect": round(gross_per_prospect, 2),
        "net_30d_ltv_per_prospect": round(net_per_prospect, 2),
        "max_allowable_cost_per_prospect_breakeven": round(max(0.0, net_per_prospect), 2),
        "max_allowable_cost_per_prospect_cfa_level3": round(max(0.0, net_per_prospect / 2.0), 2),
    }


def calc_ote_and_tac(
    *,
    sales_motion: str = "inbound",
    ote_annual: float,
    expected_weekly_closes: float,
    working_weeks_per_year: int = 50,
    annual_rep_gp: float,
    activation_rate: float = 0.5,
    allowable_cac_per_deal: float | None = None,
) -> dict[str, Any]:
    """Compute 50/50 OTE split, flat payout, backloaded accelerators, and 1-year TAC cap (<= 33.3%)."""
    if expected_weekly_closes <= 0 or working_weeks_per_year <= 0:
        raise ValueError("expected_weekly_closes and working_weeks_per_year must be > 0")
    if not (0 < activation_rate <= 1):
        raise ValueError("activation_rate must be in (0, 1]")

    expected_1yr_gp_per_hire = annual_rep_gp * activation_rate
    max_1yr_tac = expected_1yr_gp_per_hire / 3.0

    motion = sales_motion.strip().lower()
    if motion == "inbound":
        base_annual = ote_annual * 0.5
        variable_annual = ote_annual * 0.5
        weekly_variable = variable_annual / working_weeks_per_year
        flat_per_close = weekly_variable / expected_weekly_closes
        monthly_target_closes = round((expected_weekly_closes * working_weeks_per_year) / 12.0)

        t1 = max(1, round(monthly_target_closes * 0.60))
        t2 = max(t1 + 1, round(monthly_target_closes * 0.80))
        t3 = max(t2 + 1, monthly_target_closes)
        t4 = max(t3 + 1, round(monthly_target_closes * 1.20))

        accelerators = [
            {"tier": f"1-{t1} closes", "payout_per_close": round(flat_per_close * 0.90, 2)},
            {"tier": f"{t1 + 1}-{t2} closes", "payout_per_close": round(flat_per_close * 1.14, 2)},
            {"tier": f"{t2 + 1}-{t3} closes", "payout_per_close": round(flat_per_close * 1.26, 2)},
            {"tier": f"{t3 + 1}-{t4} closes", "payout_per_close": round(flat_per_close * 1.50, 2)},
            {"tier": f"{t4 + 1}+ closes", "payout_per_close": round(flat_per_close * 1.80, 2)},
        ]
        comp_block = {
            "structure": "50% Base / 50% Variable (Inbound)",
            "ote_annual": round(ote_annual, 2),
            "base_annual": round(base_annual, 2),
            "variable_annual": round(variable_annual, 2),
            "weekly_variable_target": round(weekly_variable, 2),
            "expected_weekly_closes": expected_weekly_closes,
            "flat_payout_per_close": round(flat_per_close, 2),
            "monthly_target_closes": monthly_target_closes,
            "backloaded_monthly_accelerators": accelerators,
        }
    elif motion == "self_gen":
        if allowable_cac_per_deal is None or allowable_cac_per_deal <= 0:
            raise ValueError("allowable_cac_per_deal must be > 0 for self_gen motion")
        comp_block = {
            "structure": "Uncapped Allowable-CAC Backed (Pure Self-Gen Hunter)",
            "max_commission_per_close_from_cac": round(allowable_cac_per_deal, 2),
            "note": "Pay strictly on closes / upfront cash collected; never on uncollected contract value.",
        }
    else:
        raise ValueError("sales_motion must be 'inbound' or 'self_gen'")

    return {
        "compensation": comp_block,
        "tac_economics": {
            "annual_rep_gp_activated": round(annual_rep_gp, 2),
            "activation_rate": activation_rate,
            "expected_1yr_gp_per_hire": round(expected_1yr_gp_per_hire, 2),
            "max_1yr_tac_cap_33_3_pct": round(max_1yr_tac, 2),
            "minimum_ltgp_to_tac_ratio": "3:1",
            "referral_payout_trigger": "Day 90 post-activation",
        },
        "labor_compliance_reminder": (
            "Verify W-2 vs. 1099 classification, FLSA/state overtime, meal breaks, and inside-vs-outside "
            "sales exemption rules before finalizing schedules or comp agreements."
        ),
    }


def audit_script_metrics(script_text: str, pitch_text: str | None = None) -> dict[str, Any]:
    """Deterministically lint a spoken sales script against vocal, pause, and pitch-length rules."""
    target_pitch = pitch_text if pitch_text is not None else script_text
    spoken_pitch = re.sub(r"\[[^\]]+\]", " ", target_pitch)
    pitch_words = len(re.findall(r"\b[\w'-]+\b", spoken_pitch))
    est_seconds_at_160wpm = round((pitch_words / 160.0) * 60.0, 1)

    checks = {
        "has_recorded_line_disclosure": bool(re.search(r"recorded\s+line", script_text, re.I)),
        "has_small_yes_check": bool(re.search(r"sound\s+good\?|fair\s+enough\?|make\s+sense\?", script_text, re.I)),
        "has_upward_inflection_question_marks": "?" in script_text,
        "has_short_pause_tag": bool(re.search(r"\[short\s+pause\s*-\s*1-2\s*sec\]", script_text, re.I)),
        "has_medium_pause_tag": bool(re.search(r"\[medium\s+pause\s*-\s*3-4\s*sec\]", script_text, re.I)),
        "has_long_8sec_silence_tag": bool(
            re.search(r"\[long\s+pause\s*-\s*8\+\s*sec\s+silence[^\]]*\]", script_text, re.I)
        ),
        "pitch_within_2_min_limit": pitch_words <= 340,
        "no_acknowledge_but_antipattern": not bool(
            re.search(r"(totally\s+(hear|get|understand)[^.!?\n]{0,40}\bbut\b)", script_text, re.I)
        ),
    }

    failures = [k for k, v in checks.items() if not v]
    return {
        "pitch_word_count": pitch_words,
        "max_pitch_words_at_170wpm": 340,
        "estimated_pitch_seconds_at_160wpm": est_seconds_at_160wpm,
        "checks": checks,
        "passed": len(failures) == 0,
        "failures": failures,
    }


def _self_test() -> None:
    cfa = calc_cfa_metrics(
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
    assert cfa["metrics"]["full_loaded_cac"] == 3500.0
    assert cfa["metrics"]["gross_profit_per_unit"] == 2400.0
    assert cfa["metrics"]["ltgp"] == 48000.0
    assert cfa["cfa_level"] == 3
    assert cfa["level3_compounding_reference"][-1]["total_customers"] == 4095

    vg = calc_value_grid(
        entering_prospects=10,
        offers=[{"name": "Trial + Core", "buyers": 8, "gp_30d_per_buyer": 75}],
        sales_and_lead_working_labor_cost=600,
    )
    assert vg["gross_30d_gp_total"] == 600.0
    assert vg["net_30d_ltv_per_prospect"] == 0.0

    comp = calc_ote_and_tac(
        sales_motion="inbound",
        ote_annual=100000,
        expected_weekly_closes=12,
        working_weeks_per_year=50,
        annual_rep_gp=250000,
        activation_rate=0.5,
    )
    assert comp["compensation"]["flat_payout_per_close"] == 83.33
    assert round(comp["tac_economics"]["max_1yr_tac_cap_33_3_pct"], 2) == 41666.67

    sample_script = (
        "Hi, this is Alex from Acme on a recorded line calling about your application. Sound good? "
        "[short pause - 1-2 sec] Based on your numbers, here is how we fix it. [medium pause - 3-4 sec] "
        "Investment is $5,000. Ready to get started? [long pause - 8+ sec silence until prospect speaks] "
        "Totally understand, and our top clients asked that exact question?"
    )
    lint = audit_script_metrics(sample_script, pitch_text="Based on your numbers, here is how we fix it.")
    assert lint["passed"], f"Script lint failed: {lint}"
    print("ALL SELF-TESTS PASSED")


def main() -> None:
    parser = argparse.ArgumentParser(description="Apex Sales Playbook deterministic calculators")
    parser.add_argument("--self-test", action="store_true", help="Run built-in verification assertions")
    sub = parser.add_subparsers(dest="cmd")

    for name in ["cfa", "value-grid", "ote"]:
        p = sub.add_parser(name)
        p.add_argument("--json", required=True, help="JSON payload of function keyword arguments")

    p_lint = sub.add_parser("lint-script")
    p_lint.add_argument("--file", required=True, help="Path to script text file")
    p_lint.add_argument("--pitch-file", help="Optional path to isolated pitch text file")

    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return

    if args.cmd == "cfa":
        print(json.dumps(calc_cfa_metrics(**json.loads(args.json)), indent=2))
    elif args.cmd == "value-grid":
        print(json.dumps(calc_value_grid(**json.loads(args.json)), indent=2))
    elif args.cmd == "ote":
        print(json.dumps(calc_ote_and_tac(**json.loads(args.json)), indent=2))
    elif args.cmd == "lint-script":
        script_txt = Path(args.file).read_text(encoding="utf-8")
        pitch_txt = Path(args.pitch_file).read_text(encoding="utf-8") if args.pitch_file else None
        print(json.dumps(audit_script_metrics(script_txt, pitch_txt), indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
