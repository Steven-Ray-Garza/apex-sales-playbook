---
name: sfa-offer-architect
description: Design ideal customer avatars (80/20 Cohort Audit + cold-start fallback), Value Equation offers, Van Westendorp pricing curves, high-converting front-end promotional wrappers (Premium, Free, Discount), Non-Linear Offer Matrices, retention-stacking diagnostics, and Self-Funded Acquisition (SFA) unit economics. Use when the user asks about CAC, Gross Profit, LTGP, Payback Period (PPD), 30-Day Cash (30D Cash), Van Westendorp pricing, Value Equation, avatar surveys, pricing wrappers, or offer stacking. Do NOT use for VSL/call scripts (use vsl-script-engineer), hiring/bootcamps (use sales-recruiting-bootcamp), floor ops (use sales-floor-director), transcript audits (use transcript-audit-mode), or live interactive roleplay (use roleplay-sparring-partner).
---

# Mode 1: Offer, Avatar, and Self-Funded Acquisition (SFA) Architect

## 1. 80/20 Cohort Avatar Audit and Cold-Start Fallback

- **Existing Customers (80/20 Cohort Audit):** Deploy a 4-part customer survey covering **Demographics**, **Baseline & Current Metrics**, **Target Outcomes**, and **Buying Journey** (trigger event, exact educational assets and case studies consumed, asset count pre-purchase, sales cycle duration). Isolate the top `20%` highest-spending, longest-retaining clients (replacing the bottom `80%` with top-`20%` buyers can drive `5x` profit expansion). Extract `3-5` shared qualifiers, shut down channels delivering low-LTV buyers, rewrite ads and landing pages to call out qualifiers directly, and route every new prospect through the top-`20%` education sequence (minimum `>= 2` long-form value assets; equip reps with `2-3` curated flagship pieces).
- **Zero-Customer Cold Start:** Without existing buyers, begin in a vertical where the founder already holds domain familiarity (prior work, family, or direct network), narrow to the sharpest sub-segment they can deliver the biggest win for, serve initial clients, and execute the 80/20 Cohort Audit once live revenue exists.
- **Buyer-Scale Pricing Leverage:** Identical execution creates dramatically larger dollar value (and allowable fees) for larger accounts (for example, lifting conversion from `5%` to `7%` adds `$40k/mo` to a `$100k/mo` firm versus `$4M/mo` to a `$10M/mo` firm).

## 2. Value Equation, Van Westendorp Pricing, and Retention-Stacking Diagnostics

- **The Value Equation:** Maximize `(Dream Outcome x Perceived Likelihood of Achievement) / (Time Delay x Effort & Sacrifice)`. Separate **Effort** (unpleasant actions the client must *start*) from **Sacrifice** (enjoyable habits or conveniences the client must *stop*). One of the fastest ways to command a premium price in a crowded market is to **cut the Time Delay in half**.
- **Van Westendorp 4-Question Pricing Analysis:** Survey prospects on four price thresholds - (1) *Too Expensive* (will not consider), (2) *Too Cheap* (credibility fails), (3) *Expensive Edge* (requires scrutiny, still worth buying), and (4) *Bargain* (clear steal) - tagged with buyer attributes (revenue band, industry) to slice curves by segment and catch multi-avatar bimodal splits. Run `tools/calculators.py` (`calc_van_westendorp`) to output exact `PMC`, `PME`, `OPP`, `IDP`, and Acceptable Price Range.
- **Overwhelmed-Founder Margin Diagnostic (Underpricing Trap):** When a founder hits `~$1M` and runs out of personal capacity, inspect gross margin first. Thin margins signal the founder is pricing from personal comfort rather than buyer willingness-to-pay; repair offer pricing and terms before adding headcount. **Flagship-First Tiering:** Launch the high-touch, high-margin private service first to establish market authority and cash flow, then engineer scalable down-market tiers later.
- **Retention Stacking vs. Churn-Driven Growth:** Never confuse top-line revenue built by churning and re-acquiring `100 -> 200 -> 300` new clients annually (compressing net margin under rising acquisition cost) with stacking `100` retained buyers each year (`100 -> 200 -> 300` active clients). Repair product stickiness before pouring ad spend into a leaky bucket.

## 3. Front-End Promotional Wrappers (`Generate Flow -> Monetize Flow -> Increase Friction`)

- **5 Ps Structural Alignment & Time-Before-Buy Rule:** Align all **5 Ps** (Price, Prospect, Process, Promotion, Product) consistently to either a Free or Premium acquisition architecture rather than mixing incompatible parts. As price and complexity rise, buyers require greater total engagement time - either compressed (live workshops/seminars) or distributed across multiple calls.
- **Premium Wrapper (Standalone):** Deploy when messaging, proof, guarantees, and sales execution are dialed in and the operator prioritizes simple unit economics, high buyer intent, and minimal operational drag. If premium lead acquisition costs `5-10x` more than free leads, ticket prices must sit at least `5-10x` higher.
- **Free Wrapper (Zero-Price Arbitrage):** Deploy when entering new verticals, building initial case studies, or cutting cost-per-lead by `5x+` (behavioral economics shows dramatically higher response crossing from `$0.01` to `$0` while keeping close rates and ticket size intact when properly worked). Always include a transparent **Reason Why** the offer is free. If a Free front end underperforms, run the **3-Cause Diagnostic**: (1) low desire for the giveaway, (2) low believability (missing credible reason), or (3) audience/targeting mismatch. Dial lead quality using **5 Friction Levers**: (1) explicit qualification callouts in ad copy/creative, (2) longer applications with higher-commitment fields (open-ended text, phone, revenue), (3) multi-step opt-in flows, (4) required content consumption before CTA unlock, and (5) longer ad/video runtimes.
- **Discount Wrapper (`>= 50%` Off Splintered Component):** Avoid weak `5-25%` discounts that erode margin without shifting buyer behavior. Use bold discounts (`>= 50%` off a splintered entry component, never continuously discounting the core offer) in well-understood or regulated markets to crush no-shows (`85-90%+` show rate), collect a payment method on file (with explicit written fee disclosure per Guardrail #6) for frictionless upsells, and run two-step closes using **Two-Step Pre-Qualified Intake (`5-Minute` Specialist Handoff)** (front-desk/admin handles intake, diagnostics, and financing pre-approval; the high-cost specialist conducts a `5-minute` greeting and books the dedicated plan presentation). Test creative across all **4 Discount Display Formats**: Percentage Off, Absolute Dollar Amount Off, Relative Everyday Equivalent (savings framed negatively or cost framed positively), and Direct Discounted Price.

## 4. Self-Funded Acquisition (SFA) and Non-Linear Offer Matrix Math

Use `tools/calculators.py` (`calc_sfa_metrics`, `calc_offer_matrix`, `calc_van_westendorp`) whenever tool calling is enabled.

- Calculate every core metric explicitly (evaluating **CAC per channel** - outbound, content, paid media - to allocate budget toward the lowest-CAC channel):
  - `CAC = All Marketing + Sales Spend / New Customers Acquired`
  - `GP = Price - Direct Fulfillment Cost` and `Gross Margin = GP / Price`
  - `LTGP (Transactional) = Avg GP x Avg Lifetime Transactions`
  - `LTGP (Recurring) = Monthly GP / Monthly Churn %` (keep the starting cohort denominator fixed; new signups never alter cohort churn)
  - `Payback Period (PPD)` = months until cumulative `GP >= CAC`
  - `30D Cash` = Gross Profit collected during the first `30 days` (aligned to a 30-day interest-free billing cycle)
- Classify unit economics into exact **SFA Payback Tiers**:
  - **SFA Tier 1 (`30D GP < CAC`):** Growth requires outside capital, credit lines, or cash reserves to bridge payback.
  - **SFA Tier 2 (`30D GP >= CAC`):** Self-liquidates inside a 30-day cycle; monthly ad spend is bounded by working-capital/credit limit.
  - **SFA Tier 3 (`30D GP > 2x CAC`):** Self-compounding scale threshold where each cohort funds twice the next month's acquisition (`2^n - 1` geometric expansion over `12` cycles; trigger Guardrail #6 Fulfillment and Net-Margin Brake as volume compounds).
- Map multi-product monetization onto a **Non-Linear Offer Matrix** (accounting for buyers who skip linear stair steps) to compute blended `30D LTV` / `30D Cash` net of real sales and lead-working labor costs.
