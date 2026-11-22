#!/usr/bin/env python3
"""Deterministic financial math, Van Westendorp pricing, and spoken-script linter (v4.0).

Zero external dependencies (Python 3.10+ stdlib only) with strict RFC-8259 JSON compliance
(no Infinity/NaN outputs) and input bounds validation.

Usage examples:
  python tools/calculators.py --self-test
  python tools/calculators.py sfa --json '{"price":3000,"direct_fulfillment_cost":600,"ad_spend":20000,"new_customers":10,"revenue_model":"recurring","monthly_churn_rate":0.05}'
  python tools/calculators.py offer-matrix --json '{"entering_prospects":10,"offers":[{"name":"Trial","buyers":8,"gp_30d_per_buyer":75}],"sales_and_lead_working_labor_cost":600}'
  python tools/calculators.py van-westendorp --json '{"responses":[{"too_cheap":100,"bargain":250,"expensive":500,"too_expensive":800},{"too_cheap":150,"bargain":300,"expensive":600,"too_expensive":900}]}'
  python tools/calculators.py ote --json '{"sales_motion":"inbound","ote_annual":100000,"expected_weekly_closes":12,"annual_rep_gp":250000,"activation_rate":0.5}'
  python tools/calculators.py lint-script --file path/to/script.txt
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


def _require_non_negative(name: str, value: float) -> None:
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a finite number >= 0 (got {value})")


def _require_positive(name: str, value: float) -> None:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite number > 0 (got {value})")


def calc_sfa_metrics(
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
    """Calculate Full-Loaded CAC, GP, Gross Margin, LTGP, PPD, 30D Cash, and SFA Payback Tier."""
    _require_positive("price", price)
    _require_non_negative("direct_fulfillment_cost", direct_fulfillment_cost)
    _require_non_negative("ad_spend", ad_spend)
    _require_non_negative("media_creative_payroll", media_creative_payroll)
    _require_non_negative("software_cost", software_cost)
    _require_non_negative("sales_salaries_commissions", sales_salaries_commissions)
    if not isinstance(new_customers, int) or new_customers <= 0:
        raise ValueError("new_customers must be an integer > 0")
    if gp_30d is not None and not math.isfinite(gp_30d):
        raise ValueError("gp_30d must be finite when provided")

    total_acq_spend = (
        ad_spend + media_creative_payroll + software_cost + sales_salaries_commissions
    )
    cac = total_acq_spend / new_customers
    gp = price - direct_fulfillment_cost
    gross_margin = gp / price

    model = revenue_model.strip().lower()
    if model == "recurring":
        if monthly_churn_rate is None or not math.isfinite(monthly_churn_rate) or not (0 < monthly_churn_rate <= 1):
            raise ValueError("monthly_churn_rate must be in (0, 1] for recurring models")
        ltgp = gp / monthly_churn_rate
        effective_30d_gp = gp if gp_30d is None else gp_30d
        if cac == 0:
            payback_months: float | None = 0.0
            payback_status = "zero_cac_organic"
        elif gp > 0:
            payback_months = round(cac / gp, 2)
            payback_status = "valid"
        else:
            payback_months = None
            payback_status = "non_positive_gross_profit"
    elif model == "transactional":
        if avg_lifetime_transactions is None or not math.isfinite(avg_lifetime_transactions) or avg_lifetime_transactions <= 0:
            raise ValueError("avg_lifetime_transactions must be > 0 for transactional models")
        ltgp = gp * avg_lifetime_transactions
        effective_30d_gp = gp if gp_30d is None else gp_30d
        if cac == 0:
            payback_months = 0.0
            payback_status = "zero_cac_organic"
        elif effective_30d_gp >= cac:
            payback_months = 1.0
            payback_status = "valid"
        elif effective_30d_gp > 0:
            payback_months = round(cac / effective_30d_gp, 2)
            payback_status = "valid"
        else:
            payback_months = None
            payback_status = "non_positive_30d_gp"
    else:
        raise ValueError("revenue_model must be 'recurring' or 'transactional'")

    if cac > 0:
        ltgp_to_cac: float | None = round(ltgp / cac, 2)
        gp_30d_to_cac: float | None = round(effective_30d_gp / cac, 2)
        ratio_status = "valid"
    else:
        ltgp_to_cac = None
        gp_30d_to_cac = None
        ratio_status = "zero_cac_organic"

    if effective_30d_gp > 0 and effective_30d_gp > 2.0 * cac:
        sfa_tier = 3
        sfa_label = "SFA Tier 3 (30D GP > 2x CAC: Self-Compounding Growth)"
        fulfillment_brake_alert = (
            "TRIGGER GUARDRAIL #6: Operations/fulfillment is now the growth constraint. "
            "Model fixed overhead step-functions, delivery headcount, refund reserves, and net EBITDA before scaling spend."
        )
    elif effective_30d_gp > 0 and effective_30d_gp >= cac:
        sfa_tier = 2
        sfa_label = "SFA Tier 2 (30D GP >= CAC: 30-Day Cycle Self-Liquidating)"
        fulfillment_brake_alert = None
    else:
        sfa_tier = 1
        sfa_label = "SFA Tier 1 (30D GP < CAC or Non-Positive GP: Requires Working Capital Float)"
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
            _require_non_negative(f"channel '{ch['name']}' spend", ch_spend)
            ch_cac: float | None = round(ch_spend / ch_cust, 2) if ch_cust > 0 else None
            channel_breakdown.append({
                "channel": ch["name"],
                "total_spend": round(ch_spend, 2),
                "new_customers": ch_cust,
                "cac": ch_cac,
            })
        channel_breakdown.sort(key=lambda x: float("inf") if x["cac"] is None else x["cac"])

    tier3_compounding_12mo = [
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
            "ltgp_to_cac_ratio": ltgp_to_cac,
            "payback_period_months": payback_months,
            "payback_status": payback_status,
            "ratio_status": ratio_status,
            "cash_30d_gp": round(effective_30d_gp, 2),
            "cash_30d_to_cac_ratio": gp_30d_to_cac,
        },
        "sfa_tier": sfa_tier,
        "sfa_label": sfa_label,
        "fulfillment_brake_alert": fulfillment_brake_alert,
        "channel_cac_ranked": channel_breakdown,
        "tier3_compounding_reference": tier3_compounding_12mo if sfa_tier == 3 else None,
    }


def calc_offer_matrix(
    *,
    entering_prospects: int,
    offers: list[dict[str, Any]],
    sales_and_lead_working_labor_cost: float = 0.0,
) -> dict[str, Any]:
    """Compute Non-Linear Offer Matrix blended 30D GP/LTV net of sales & lead-working labor."""
    if not isinstance(entering_prospects, int) or entering_prospects <= 0:
        raise ValueError("entering_prospects must be an integer > 0")
    _require_non_negative("sales_and_lead_working_labor_cost", sales_and_lead_working_labor_cost)

    offer_rows = []
    gross_30d_gp = 0.0
    for offer in offers:
        buyers = float(offer["buyers"])
        gp_per_buyer = float(offer["gp_30d_per_buyer"])
        _require_non_negative(f"offer '{offer['name']}' buyers", buyers)
        if not math.isfinite(gp_per_buyer):
            raise ValueError(f"offer '{offer['name']}' gp_30d_per_buyer must be finite")
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
        "max_allowable_cost_per_prospect_sfa_tier3": round(max(0.0, net_per_prospect / 2.0), 2),
    }


def _find_curve_intersection(
    prices: list[float],
    curve_a: list[float],
    curve_b: list[float],
) -> float:
    """Linearly interpolate the price where curve_a(p) intersects curve_b(p)."""
    diffs = [a - b for a, b in zip(curve_a, curve_b)]
    for i in range(len(prices) - 1):
        d1, d2 = diffs[i], diffs[i + 1]
        if d1 == 0:
            return round(prices[i], 2)
        if (d1 < 0 < d2) or (d1 > 0 > d2):
            p1, p2 = prices[i], prices[i + 1]
            t = abs(d1) / (abs(d1) + abs(d2))
            return round(p1 + t * (p2 - p1), 2)
    min_idx = min(range(len(diffs)), key=lambda idx: abs(diffs[idx]))
    return round(prices[min_idx], 2)


def _solve_van_westendorp_cohort(responses: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute PMC, PME, OPP, IDP, and Acceptable Price Range for a single cohort."""
    valid = []
    for r in responses:
        tc = float(r["too_cheap"])
        bg = float(r["bargain"])
        ex = float(r["expensive"])
        te = float(r["too_expensive"])
        for val_name, val in [("too_cheap", tc), ("bargain", bg), ("expensive", ex), ("too_expensive", te)]:
            _require_non_negative(val_name, val)
        if tc <= bg <= ex <= te:
            valid.append((tc, bg, ex, te))

    if len(valid) < 2:
        raise ValueError(
            "Need at least 2 logically ordered non-negative responses "
            "(0 <= too_cheap <= bargain <= expensive <= too_expensive)"
        )

    n = len(valid)
    grid = sorted({p for row in valid for p in row})
    tc_curve = [sum(1 for row in valid if row[0] >= p) / n for p in grid]
    bg_curve = [sum(1 for row in valid if row[1] >= p) / n for p in grid]
    ex_curve = [sum(1 for row in valid if row[2] <= p) / n for p in grid]
    te_curve = [sum(1 for row in valid if row[3] <= p) / n for p in grid]

    pmc = _find_curve_intersection(grid, tc_curve, ex_curve)
    pme = _find_curve_intersection(grid, te_curve, bg_curve)
    opp = _find_curve_intersection(grid, tc_curve, te_curve)
    idp = _find_curve_intersection(grid, bg_curve, ex_curve)

    low_bound = min(pmc, pme)
    high_bound = max(pmc, pme)

    return {
        "valid_responses": n,
        "dropped_inconsistent_responses": len(responses) - n,
        "point_of_marginal_cheapness_pmc": pmc,
        "optimal_price_point_opp": opp,
        "indifference_price_point_idp": idp,
        "point_of_marginal_expensiveness_pme": pme,
        "acceptable_price_range": [low_bound, high_bound],
        "recommended_band_automated_checkout": [low_bound, min(high_bound, max(opp, idp))],
        "recommended_band_high_friction_sales": [max(low_bound, idp), high_bound],
    }


def calc_van_westendorp(
    *,
    responses: list[dict[str, Any]],
    segment_field: str | None = None,
) -> dict[str, Any]:
    """Run Van Westendorp 4-question pricing analysis (overall + optional avatar segmentation)."""
    if not responses:
        raise ValueError("responses list cannot be empty")

    overall = _solve_van_westendorp_cohort(responses)
    segments_out: dict[str, Any] = {}
    multi_avatar_alert = None

    if segment_field:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for r in responses:
            key = str(r.get(segment_field, "unclassified"))
            grouped.setdefault(key, []).append(r)

        opps = []
        for seg_name, rows in sorted(grouped.items()):
            if len(rows) >= 2:
                seg_res = _solve_van_westendorp_cohort(rows)
                segments_out[seg_name] = seg_res
                opps.append(seg_res["optimal_price_point_opp"])
            else:
                segments_out[seg_name] = {"skipped": f"Only {len(rows)} response(s); need >= 2."}

        if len(opps) >= 2 and min(opps) > 0 and (max(opps) / min(opps)) >= 1.75:
            multi_avatar_alert = (
                "MULTI-AVATAR SPLIT DETECTED: Optimal price points diverge by >= 1.75x across segments "
                "(bimodal distribution). Price and message each segment separately rather than averaging."
            )

    return {
        "overall": overall,
        "segments": segments_out if segment_field else None,
        "multi_avatar_alert": multi_avatar_alert,
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
    _require_positive("ote_annual", ote_annual)
    _require_positive("expected_weekly_closes", expected_weekly_closes)
    _require_positive("annual_rep_gp", annual_rep_gp)
    if not isinstance(working_weeks_per_year, int) or not (1 <= working_weeks_per_year <= 52):
        raise ValueError("working_weeks_per_year must be an integer in [1, 52]")
    if not math.isfinite(activation_rate) or not (0 < activation_rate <= 1):
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
        if allowable_cac_per_deal is None:
            raise ValueError("allowable_cac_per_deal is required for self_gen motion")
        _require_positive("allowable_cac_per_deal", allowable_cac_per_deal)
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
        "has_small_yes_check": bool(
            re.search(r"sound\s+good\?|sound\s+fair\?|fair\s+enough\?|make\s+sense\?", script_text, re.I)
        ),
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


# Backward-compatible aliases so existing scripts/workflows never break
calc_cfa_metrics = calc_sfa_metrics
calc_value_grid = calc_offer_matrix


def _assert_strict_json(obj: Any) -> None:
    """Verify output serializes cleanly under strict RFC-8259 JSON (no NaN/Infinity)."""
    json.dumps(obj, allow_nan=False)


def _assert_raises_value_error(fn: Any, **kwargs: Any) -> None:
    try:
        fn(**kwargs)
    except ValueError:
        return
    raise AssertionError(f"Expected ValueError for {fn.__name__}({kwargs})")


def _self_test() -> None:
    # 1. Core SFA Tier 3 calculation
    sfa = calc_sfa_metrics(
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
    _assert_strict_json(sfa)
    assert sfa["metrics"]["full_loaded_cac"] == 3500.0
    assert sfa["metrics"]["gross_profit_per_unit"] == 2400.0
    assert sfa["metrics"]["ltgp"] == 48000.0
    assert sfa["sfa_tier"] == 3
    assert sfa["tier3_compounding_reference"][-1]["total_customers"] == 4095

    # 2. Adversarial edge cases: zero-CAC organic & loss-leader GP <= 0 (must produce strict JSON, zero Infinity)
    organic = calc_sfa_metrics(
        price=1000, direct_fulfillment_cost=200, ad_spend=0,
        new_customers=5, revenue_model="recurring", monthly_churn_rate=0.05,
    )
    _assert_strict_json(organic)
    assert organic["metrics"]["payback_period_months"] == 0.0
    assert organic["metrics"]["ltgp_to_cac_ratio"] is None

    loss_leader = calc_sfa_metrics(
        price=100, direct_fulfillment_cost=150, ad_spend=500,
        new_customers=5, revenue_model="recurring", monthly_churn_rate=0.10,
    )
    _assert_strict_json(loss_leader)
    assert loss_leader["metrics"]["payback_period_months"] is None
    assert loss_leader["sfa_tier"] == 1

    # 3. Non-Linear Offer Matrix
    om = calc_offer_matrix(
        entering_prospects=10,
        offers=[{"name": "Entry Trial", "buyers": 8, "gp_30d_per_buyer": 75}],
        sales_and_lead_working_labor_cost=600,
    )
    _assert_strict_json(om)
    assert om["gross_30d_gp_total"] == 600.0
    assert om["net_30d_ltv_per_prospect"] == 0.0

    # 4. Van Westendorp multi-avatar split
    vw = calc_van_westendorp(
        responses=[
            {"segment": "smb", "too_cheap": 500, "bargain": 1000, "expensive": 2000, "too_expensive": 3000},
            {"segment": "smb", "too_cheap": 600, "bargain": 1200, "expensive": 2200, "too_expensive": 3500},
            {"segment": "enterprise", "too_cheap": 3000, "bargain": 6000, "expensive": 12000, "too_expensive": 18000},
            {"segment": "enterprise", "too_cheap": 4000, "bargain": 8000, "expensive": 15000, "too_expensive": 22000},
        ],
        segment_field="segment",
    )
    _assert_strict_json(vw)
    assert vw["overall"]["valid_responses"] == 4
    assert vw["multi_avatar_alert"] is not None
    assert vw["segments"]["enterprise"]["optimal_price_point_opp"] > vw["segments"]["smb"]["optimal_price_point_opp"]

    # 5. OTE & TAC
    comp = calc_ote_and_tac(
        sales_motion="inbound",
        ote_annual=100000,
        expected_weekly_closes=12,
        working_weeks_per_year=50,
        annual_rep_gp=250000,
        activation_rate=0.5,
    )
    _assert_strict_json(comp)
    assert comp["compensation"]["flat_payout_per_close"] == 83.33
    assert round(comp["tac_economics"]["max_1yr_tac_cap_33_3_pct"], 2) == 41666.67

    # 6. Bounds validation assertions (negative inputs must fail loudly)
    _assert_raises_value_error(
        calc_sfa_metrics, price=1000, direct_fulfillment_cost=-10, ad_spend=500,
        new_customers=5, revenue_model="recurring", monthly_churn_rate=0.05,
    )
    _assert_raises_value_error(
        calc_offer_matrix, entering_prospects=10,
        offers=[{"name": "Bad", "buyers": -1, "gp_30d_per_buyer": 100}],
    )
    _assert_raises_value_error(
        calc_van_westendorp, responses=[
            {"too_cheap": -10, "bargain": 50, "expensive": 100, "too_expensive": 200},
            {"too_cheap": 10, "bargain": 50, "expensive": 100, "too_expensive": 200},
        ],
    )
    _assert_raises_value_error(
        calc_ote_and_tac, sales_motion="inbound", ote_annual=-1000,
        expected_weekly_closes=5, annual_rep_gp=100000, activation_rate=0.5,
    )

    # 7. Script hygiene linter (neutral persona)
    sample_script = (
        "Hi, this is Jordan from Northstar on a recorded line calling about your request. Does that sound fair? "
        "[short pause - 1-2 sec] Based on your targets, here is the three-step plan. [medium pause - 3-4 sec] "
        "The investment is $5,000. Ready to move forward? [long pause - 8+ sec silence until prospect speaks] "
        "Totally hear you, and our best-performing clients asked that exact question?"
    )
    lint = audit_script_metrics(sample_script, pitch_text="Based on your targets, here is the three-step plan.")
    _assert_strict_json(lint)
    assert lint["passed"], f"Script lint failed: {lint}"
    print("ALL SELF-TESTS PASSED")


def main() -> None:
    parser = argparse.ArgumentParser(description="Apex Revenue Operations deterministic calculators (v4.0)")
    parser.add_argument("--self-test", action="store_true", help="Run built-in verification and edge-case assertions")
    sub = parser.add_subparsers(dest="cmd")

    for name in ["sfa", "cfa", "offer-matrix", "value-grid", "ote", "van-westendorp"]:
        p = sub.add_parser(name)
        p.add_argument("--json", required=True, help="JSON payload of function keyword arguments")

    p_lint = sub.add_parser("lint-script")
    p_lint.add_argument("--file", required=True, help="Path to script text file")
    p_lint.add_argument("--pitch-file", help="Optional path to isolated pitch text file")

    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return

    if args.cmd in ("sfa", "cfa"):
        out = calc_sfa_metrics(**json.loads(args.json))
    elif args.cmd in ("offer-matrix", "value-grid"):
        out = calc_offer_matrix(**json.loads(args.json))
    elif args.cmd == "ote":
        out = calc_ote_and_tac(**json.loads(args.json))
    elif args.cmd == "van-westendorp":
        out = calc_van_westendorp(**json.loads(args.json))
    elif args.cmd == "lint-script":
        script_txt = Path(args.file).read_text(encoding="utf-8")
        pitch_txt = Path(args.pitch_file).read_text(encoding="utf-8") if args.pitch_file else None
        out = audit_script_metrics(script_txt, pitch_txt)
    else:
        parser.print_help()
        return

    print(json.dumps(out, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
