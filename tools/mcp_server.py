#!/usr/bin/env python3
"""Optional MCP (Model Context Protocol) server exposing deterministic playbook calculators.

Requires: pip install mcp
Run:      python tools/mcp_server.py
Works with Claude Desktop, Claude Code, Gemini CLI, Cursor, and local MCP clients.
"""

from __future__ import annotations

from typing import Any
from mcp.server.fastmcp import FastMCP
from calculators import (
    audit_script_metrics,
    calc_cfa_metrics,
    calc_ote_and_tac,
    calc_value_grid,
    calc_van_westendorp,
)

mcp = FastMCP("apex-sales-playbook")


@mcp.tool()
def cfa_unit_economics(
    price: float,
    direct_fulfillment_cost: float,
    ad_spend: float,
    new_customers: int,
    media_creative_payroll: float = 0.0,
    software_cost: float = 0.0,
    sales_salaries_commissions: float = 0.0,
    revenue_model: str = "recurring",
    monthly_churn_rate: float | None = None,
    avg_lifetime_transactions: float | None = None,
    gp_30d: float | None = None,
    channels: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compute Full-Loaded CAC (blended & per channel), GP, Gross Margin, LTGP, PPD, 30D Cash, and CFA Level."""
    return calc_cfa_metrics(
        price=price,
        direct_fulfillment_cost=direct_fulfillment_cost,
        ad_spend=ad_spend,
        media_creative_payroll=media_creative_payroll,
        software_cost=software_cost,
        sales_salaries_commissions=sales_salaries_commissions,
        new_customers=new_customers,
        revenue_model=revenue_model,
        monthly_churn_rate=monthly_churn_rate,
        avg_lifetime_transactions=avg_lifetime_transactions,
        gp_30d=gp_30d,
        channels=channels,
    )


@mcp.tool()
def value_grid_ltv(
    entering_prospects: int,
    offers: list[dict[str, Any]],
    sales_and_lead_working_labor_cost: float = 0.0,
) -> dict[str, Any]:
    """Calculate non-linear Value Grid blended 30D LTV net of sales and lead-working labor."""
    return calc_value_grid(
        entering_prospects=entering_prospects,
        offers=offers,
        sales_and_lead_working_labor_cost=sales_and_lead_working_labor_cost,
    )


@mcp.tool()
def van_westendorp_pricing(
    responses: list[dict[str, Any]],
    segment_field: str | None = None,
) -> dict[str, Any]:
    """Compute Van Westendorp PMC, PME, OPP, IDP, Acceptable Price Range, and multi-avatar split alerts."""
    return calc_van_westendorp(responses=responses, segment_field=segment_field)


@mcp.tool()
def ote_and_tac_calculator(
    ote_annual: float,
    expected_weekly_closes: float,
    annual_rep_gp: float,
    sales_motion: str = "inbound",
    working_weeks_per_year: int = 50,
    activation_rate: float = 0.5,
    allowable_cac_per_deal: float | None = None,
) -> dict[str, Any]:
    """Calculate 50/50 OTE splits, backloaded monthly accelerators, and 1-year <= 33.3% TAC cap."""
    return calc_ote_and_tac(
        sales_motion=sales_motion,
        ote_annual=ote_annual,
        expected_weekly_closes=expected_weekly_closes,
        working_weeks_per_year=working_weeks_per_year,
        annual_rep_gp=annual_rep_gp,
        activation_rate=activation_rate,
        allowable_cac_per_deal=allowable_cac_per_deal,
    )


@mcp.tool()
def script_hygiene_linter(script_text: str, pitch_text: str | None = None) -> dict[str, Any]:
    """Verify pitch duration (<= 340 words / <= 2 min), Big Four opening, ? inflection, and 8+ sec silence tag."""
    return audit_script_metrics(script_text=script_text, pitch_text=pitch_text)


if __name__ == "__main__":
    mcp.run()
