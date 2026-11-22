---
name: cfa-offer-architect
description: Design ideal customer avatars (VAM + zero-customer cold start), Value Equation offers, Van Westendorp pricing curves, high-converting front-end promotional wrappers (Premium, Free, Discount), non-linear Value Grids, retention-stacking diagnostics, and Customer Financed Acquisition (CFA) unit economics. Use when the user asks about CAC, Gross Profit, LTGP, Payback Period (PPD), 30-Day Cash (30D Cash), Van Westendorp pricing, Value Equation, VAM surveys, pricing wrappers, or offer stacking. Do NOT use for VSSL/call scripts (use vssl-script-engineer), hiring/bootcamps (use sales-recruiting-bootcamp), floor ops (use sales-floor-director), transcript audits (use transcript-audit-mode), or live interactive roleplay (use roleplay-sparring-partner).
---

# Mode 1: Offer, Avatar, and CFA Unit-Economics Architect

## 1. Value Acceleration Method (VAM) Avatar Audit and Cold-Start Fallback

- **Existing Customers (VAM):** Build a 4-part customer survey covering **Demographics**, **Business/Life Stats (Before and Current)**, **Aspirations**, and **Buying Process** (trigger event, exact content/testimonials consumed, count of assets consumed pre-purchase, time-to-buy). Isolate the top `20%` highest-spending, longest-retaining clients (replacing the bottom `80%` with top-`20%` buyers drives `5x` growth). Extract `3-5` common qualifiers, cut channels feeding low-value buyers, rewrite ads/pages to call out qualifiers explicitly, and force all new leads through the top-`20%` buying path (minimum `>= 2` long-form value pieces; arm reps with `2-3` hand-selected "all-time greatest hits" assets).
- **Zero-Customer Cold Start:** If no customers exist yet, start in an industry where the founder holds insider knowledge (past jobs, family, network), select the narrowest target they can help most, serve them first, and run VAM once live buyers exist.
- **Who-They-Are Pricing Power:** Identical work produces exponentially more dollar value (and fees) for larger buyers (e.g., lifting conversion from `5%` to `7%` creates `$40k/mo` for a `$100k/mo` business vs. `$4M/mo` for a `$10M/mo` business).

## 2. Value Equation, Van Westendorp Pricing, and Retention-Stacking Diagnostics

- **The Value Equation:** Maximize `(Dream Outcome x Perceived Likelihood of Achievement) / (Time Delay x Effort & Sacrifice)`. Separate **Effort** (things the buyer must *start* doing that they dislike) from **Sacrifice** (good things they must *stop* doing). To disrupt an established market at a premium price, **halve the Time Delay** to the outcome.
- **Van Westendorp 4-Question Pricing Analysis:** Survey prospects on 4 price points - (1) *Too Expensive* (would not consider), (2) *Too Cheap* (not believable), (3) *Expensive Edge* (must think hard, still buy), and (4) *Bargain* (great deal) - paired with customer stats (revenue tier, vertical) to slice curves by avatar and detect multi-avatar double-Gaussian splits. Run `tools/calculators.py` (`calc_van_westendorp`) to compute exact `PMC`, `PME`, `OPP`, `IDP`, and Acceptable Price Range.
- **Overwhelmed-Founder Margin Diagnostic ("Selling Out of Your Own Wallet"):** When a founder hits `~$1M` and runs out of time, audit gross margin first. Thin margins mean the founder is undercharging for skills that feel easy to them; fix the offer and pricing before hiring. **Start Unscalable, Anchor High, Step Down (Tesla Roadster -> Model S):** Build the absurdly valuable, high-margin private service first to anchor authority and collect cash flow, then build scalable down-market tiers.
- **Retention Stacking (`Company A vs. Company B`):** Never confuse top-line growth from churning and re-selling `100 -> 200 -> 300` new buyers each year (Company B, compressing net margin) with stacking `100` retained buyers per year (`100 -> 200 -> 300` active buyers, Company A). Fix product stickiness before pouring distribution fuel onto a leaky bucket.

## 3. Front-End Promotional Wrappers (`Generate Flow -> Monetize Flow -> Increase Friction`)

- **5 Ps Alignment and Time-Spent Rules:** Align all **5 Ps** (Price, Prospect, Process, Promotion, Product) to either a Free or Premium structure rather than mixing and matching. As price and complexity rise, prospects require more total time before buying - either compressed (workshops/seminars) or spread across multiple calls.
- **Premium Wrapper (Standalone):** Use when avatar copy, guarantees/bonuses, and sales conviction are proven and the operator wants simplest math, highest lead quality, and lowest operational drag. If premium lead costs are `5-10x` higher than free leads, prices must be at least `5-10x` higher.
- **Free Wrapper (Penny Gap Arbitrage):** Use when entering new markets, collecting testimonials, or lowering lead costs by `5x+` (`9x` more response across the `$0.01 -> $0` penny gap at equal close rates and average ticket size). Always pair with a believable **Reason Why**. If a Free offer fails to convert, run the **3-Cause Diagnostic**: (1) prospects do not want the giveaway, (2) they do not believe it (missing credible Reason Why), or (3) wrong audience/targeting. Tune quality with the **5 Friction Levers**: (1) explicit qualifications in copy/creative, (2) application length and heavier question types (open-ended text and cell/income fields over multiple choice), (3) multi-step funnel sequence, (4) forced content consumption before CTA, and (5) longer ad/video length.
- **Discount Wrapper (`>= 50%` Off Splintered Component):** Never run marginal `5-25%` discounts that erode margin without driving action. Use massive discounts (`>= 50%` off a splintered component, not the core offer continuously) for well-understood services or regulated markets to eliminate no-shows (`85-90%+` show rate), capture a card on file (with explicit written fee disclosure) for seamless upsells, and execute two-step closes including the **Proprietary 5-Minute Appointment Method** (front-desk admin handles intake, diagnostics, and financing pre-approval; specialist conducts a `5-minute` intro and books the core treatment/plan close). Generate ad variants across all **4 Discount Display Formats**: Percentage Off, Absolute Amount Off, Relative Equivalent Off (negative savings and positive cost), and Simply Discounted Price.

## 4. Customer Financed Acquisition (CFA) and Value Grid Math

Use `tools/calculators.py` (`calc_cfa_metrics`, `calc_value_grid`, `calc_van_westendorp`) whenever tool calling is enabled.

- Compute all core metrics explicitly (evaluating **CAC per channel** - outreach, content, paid ads - to double down on the lowest-cost source):
  - `CAC = All Marketing + Sales Spend / New Customers Acquired`
  - `GP = Price - Fulfillment Cost` and `Gross Margin = GP / Price`
  - `LTGP (Transactional) = Avg GP x Avg Lifetime Transactions`
  - `LTGP (Recurring) = Monthly GP / Monthly Churn %` (hold initial cohort denominator fixed; new signups never change churn denominator)
  - `Payback Period (PPD)` = time until cumulative `GP > CAC`
  - `30D Cash` = Gross Profit collected in the first `30 days` (aligned with a 30-day interest-free credit card cycle)
- Classify the model into its exact CFA Level:
  - **CFA Level 1 (`30D GP < CAC`):** Requires outside capital, loans, or savings to float growth.
  - **CFA Level 2 (`30D GP = CAC`):** Self-liquidates within a 30-day credit card cycle; ad budget capped by credit limit.
  - **CFA Level 3 (`30D GP > 2x CAC`):** Minimum real-life scaling standard; self-compounding growth where 1 paid customer scales into `4,095` total customers over `12 months` (trigger Fulfillment and Net-Margin Brake as volume compounds).
- Map multi-offer monetization onto a non-linear **Value Grid** to calculate blended `30D LTV` / `30D Cash` after deducting real sales and lead-working labor costs.
