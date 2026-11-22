---
name: transcript-audit-mode
description: Convert any raw setter or closer call transcript into standardized 6-line CRM Call Notes (readable in 30 seconds) plus a BANT and Intro-Disco-Pitch-Close scorecard with one targeted behavior focus and a 3-turn verbatim roleplay drill. Trigger immediately whenever the user pastes a call transcript or recording log without asking intake questions.
---

# Mode 5: Transcript Audit Mode (6-Line Call Notes + BANT Coach)

Trigger automatically whenever the user pastes a raw setter or closer call transcript. Output both deliverables in exact order (or emit JSON conforming to `schemas/call_notes_6line.schema.json` and `schemas/bant_scorecard.schema.json` when structured output is requested):

## 1. 6-Line CRM Call Notes (Readable in 30 Seconds)

- **Line 1 - Avatar and Context:** Prospect role, business/situation, lead source, and VSSL consumption status.
- **Line 2 - Quantified Gap:** Exact Current State vs. Desired State numbers.
- **Line 3 - Core Pain and Stakes:** Primary obstacle plus attached dollar figure, timeline, or affected person.
- **Line 4 - BANT and Deal Breakers:** Budget, Authority (all decision makers?), Need, Timing, plus logistics or value deal breakers.
- **Line 5 - Predicted Objections and Proof Arrows:** Anticipated smoke screens/objections plus matched case studies/testimonials for the next call.
- **Line 6 - Next Step and Tone Intel:** Exact BAMFAM/handoff slot, prospect style (needs challenge vs. back-foot), and required follow-up.

## 2. BANT and Script Scorecard + Targeted Roleplay Drill

- Grade **Budget, Authority, Need, Timing** (`Pass / Partial / Missing`) with quoted transcript evidence, and audit `Intro -> Disco -> Pitch -> Close` execution (Big Four compliance, small-yes, Pain Cycle depth, pitch `<= 2 min`, `8+ sec` post-ask silence, question-only looping, AAA bridge).
- Prescribe **One Behavior Focus** (`"If this, then that"`) targeting the single highest-leverage gap.
- Deliver a verbatim **3-turn Manager-to-Rep Roleplay Drill** (with `?` and pause tags) so the rep can immediately rehearse the exact missing moment.
