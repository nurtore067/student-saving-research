# Research protocol (planned; no human data collected)

## Key design choice

This is a **three-arm randomized experiment**, not a factorial design. It supports
**A vs B** for the price-presentation contrast and **B vs C** for the proposed
AI-assisted guidance package. **A vs C cannot identify a single effect** because
both price prominence and guidance differ. Do not interpret that comparison as
an isolated AI effect.

Both visual cards show 24,000 KZT total and four equal 6,000 KZT payments,
with the same total cost and other conditions. Only emphasis changes from A to
B. B and C see the same card; only the type of guidance changes. A and B receive
identical non-personalized guidance. The future AI treatment should use a frozen
model/prompt/temperature or pre-generated, fixed, reviewed outputs.

## Questions and their exact scale

Use exactly the same 1-7 anchors whenever possible:
- Baseline/post attainability: "How achievable is your saving goal?" (1 = Not at all achievable, 7 = Very achievable)
- Baseline/post saving intention: "How likely are you to put money toward this goal in the next month?" (1 = Very unlikely, 7 = Very likely)
- Post purchase intention: "How likely are you to buy these headphones at the shown terms?" (1 = Very unlikely, 7 = Very likely)
- Price comprehension: "What is the full amount you would pay for the headphones?" (numeric KZT, correct answer 24000)

Collect a goal label and age bracket for the eventual AI-generated treatment;
collect only the minimum financial variables that are needed, without bank
account numbers. See `docs/survey_instrument.md`.

## Analysis plan for future real data

- Main two-sided contrast: average (post - pre attainability) C minus B, with
  95% CI. No p-value is computed from nine fake sample rows.
- Secondary A vs B: difference in mean purchase intention, with 95% CI.
- Observational RQ1: baseline saving intention regressed on baseline
  attainability and prespecified covariates (age, disposable budget,
  employment, family support, installment obligations). Interpretation is
  association only.
- Exploratory RQ3: interaction between A/B price emphasis and **centered**
  baseline attainability; avoid turning continuous A into a median split.
- Decide the main-study target N from a power calculation before recruiting,
  taking the three arms and primary B/C comparison into account. Pilot ~10-15
  volunteers are excluded from final main analysis.
- Record exclusions, allocation failures, missing data and protocol deviations.

## Validity boundaries

Matched exposure controls attention as much as possible, but the design cannot
separate the advantage of a language model from generic personalization or
extra information. Comparing to a personalized non-AI algorithm in a fourth arm
would be necessary to isolate that mechanism. No actual spending, debt, or
wealth accumulation is measured here. No causal inference about baseline
attainability in RQ1.
