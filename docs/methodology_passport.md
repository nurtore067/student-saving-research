# METHODOLOGY PASSPORT CARD | RESEARCH METHODS - TASK 2

**Research title:** Why Saving Seems Pointless to Students: The Role of Financial Expectations and Digital Purchase Incentives  
**Authors:** Gumar Nurtore; Kydyralina Akniet  
**GitHub:** **[REPLACE WITH THE ACTUAL PUBLIC GITHUB REPOSITORY URL BEFORE SUBMISSION]**  
**Version:** 1.0 | 12 October 2026 | Study design / no real participant results

## 1. Project information and IT solution

Many students may believe that saving is difficult because their financial goals feel far away. Digital installment offers may also make purchases seem easier. Our study examines these ideas; it does **not** assume that all students have these beliefs.

Our proposed IT solution is a **mobile AI Saving Coach for students in Kazakhstan**. Students will manually enter income, expenses and a saving goal, or later import a bank statement. The planned assistant will explain the total cost of installments, show how a purchase may delay a saving goal, and suggest small saving steps. Widgets and simple financial lessons are planned. Direct bank integration is **future work**, not a feature of this Task 2 repository.

The repository delivered for Task 2 contains a **working research measurement pipeline** and a separate **rule-based calculation preview**. It does not contain a deployed mobile app or a tested generative AI model. The planned AI-assisted intervention must be built, frozen and piloted before actual human testing.

## 2. Research type, population and questions

**Research type:** Mainly **quantitative**: a short survey and a randomized online three-group vignette experiment. Open comments may be collected in the pilot for clarity, but they are not the primary study data.

**Population:** Adult university students aged 18-24 studying in Almaty, Kazakhstan. Recruitment: a disclosed convenience sample. A pilot with about 10-15 students checks understanding and is excluded from the main study. The main target sample size will be chosen by a power analysis before recruitment; no sample size or effect is claimed yet.

**RQ1 (from Task 1):** Is higher perceived financial-goal attainability associated with stronger saving intention?

**RQ2 (from Task 1):** Does emphasizing the installment amount instead of the total price change purchase intention when the payment terms are identical?

**RQ3 (from Task 1; exploratory):** Does the effect of price emphasis differ by baseline goal attainability?

**RQ4 (Task 2 extension):** Compared with a generic financial summary, does the proposed AI-assisted saving coach change how achievable a saving goal feels when students see an installment offer?

**Priority:** RQ4 is the primary intervention question for this AI extension. RQ2 is a prespecified secondary question that keeps the Task 1 price-framing experiment. RQ1 is observational; RQ3 is exploratory.

## 3. Testable hypotheses

**RQ1 - Association**  
- **H0_1:** The adjusted coefficient for baseline goal attainability in a model of baseline saving intention equals 0.  
- **H1_1:** The coefficient differs from 0 (a positive association is expected).  
This relationship is observational, **not causal**.

**RQ2 - Price emphasis**  
- **H0_2:** Mean purchase intention is the same in Groups A and B.  
- **H1_2:** Mean purchase intention differs between Groups A and B.  
We expect installment emphasis may increase purchase intention, but do not assume it will.

**RQ3 - Exploratory moderation**  
- **H0_3:** The interaction coefficient (price emphasis x baseline attainability) equals 0 in Groups A and B.  
- **H1_3:** The interaction coefficient differs from 0.  
We do not specify an interaction direction in advance.

**RQ4 - Proposed AI-coach intervention**  
- **H0_4:** Mean change in perceived saving-goal attainability is equal in Groups B and C.  
- **H1_4:** Mean change differs between Groups B and C.  
We expect more positive change in C, but the test is two-sided to avoid assuming the outcome.

## 4. Groups and variable matrix

Every group sees the **same headphones**, total price **24,000 KZT**, installment schedule **4 x 6,000 KZT**, no extra fees, identical descriptions and eligibility. **Both price figures are visible in every condition; only their visual prominence changes.** The guidance shown in A and B is the same generic financial summary. C sees the same installment-emphasis card as B but receives a personalized AI-coach explanation instead of the generic summary. Time, length and reading conditions should be matched as far as possible.

| Group | Price prominence | Guidance | Used for |
|---|---|---|---|
| A | Full total emphasized; installment amount still visible | Generic, non-personalized summary | A vs B: price display |
| B | Installment amount emphasized; full total still visible | Same generic summary as A | Baseline for AI; price display |
| C | Same installment emphasis as B | Planned AI-assisted personalized saving plan | C vs B: intervention package |

| Role | Variables | Measurement / controls |
|---|---|---|
| Independent, randomized | Price-emphasis assignment (A vs B); guidance assignment (B vs C) | Three mutually exclusive randomized groups |
| Outcome, primary | Change in goal attainability | Post score - pre score, each scored 1-7 |
| Outcome, secondary | Purchase intention; saving intention | Each scored 1-7; baseline and post saving intention |
| Predictor, observational | Baseline perceived goal attainability | 1-7, measured before group exposure |
| Baseline covariates | Age; monthly disposable money; employment; family support; existing installment obligation | Measured before treatment and not changed by it |
| Controlled | Product, total price, payment terms, image, copy, platform, time, question wording, currency, exposure order | Identical or pre-specified wherever possible |

**Interpretation caution:** B vs C tests the **AI-assisted personalized guidance package** versus a generic summary. It cannot independently prove that an AI model is better than a non-AI personalized coach. Testing that would require a separate matched personalized non-AI condition.

## 5. Primary, secondary and guardrail metrics

**Primary metric - RQ4:**

For student *i*, `goal_change_i = attainability_post_i - attainability_pre_i`.  
**Primary estimate:** `mean(goal_change in C) - mean(goal_change in B)` (scale points, possible range -12 to +12).  
**Main baseline:** Group **B**, with installment emphasis and generic information. A positive value would favor C descriptively. For real data, report a two-sided 95% confidence interval and use a pre-specified two-sided two-sample comparison; a baseline-adjusted regression can be a sensitivity analysis.

**Secondary metrics:**

- **RQ2 price-framing estimate:** mean purchase intention in **B - A** (1-7 scale points). Group **A** is the baseline for framing.
- **RQ1:** adjusted baseline attainability coefficient predicting baseline saving intention (plus descriptive Pearson correlation in the demo).
- **RQ3:** interaction term of group A/B price emphasis and centered baseline attainability (exploratory; do not interpret tiny synthetic samples).
- Saving intention change (`post - pre`) as another outcome for B vs C; exploratory.

**Guardrail metrics and pre-defined thresholds:**

- Invalid/incomplete answers among consented rows: **at most 10%** in the pilot (revise the questionnaire if higher).
- Correct understanding of total installment price: **at least 80%** of complete answers report **24,000 KZT** (comprehension check, not evidence of behavior change).
- Product arithmetic: `4 * 6,000 = 24,000 KZT`, **0 errors**; an automated test must reject an inconsistent configuration.
- No real bank credentials, account statements or personally identifying participant data in the public repository.

**Important:** Hardware performance metrics such as GPU usage or latency are not primary measures here because the research outcome is a student response, not software speed. Runtime correctness is checked by reproducible unit tests.

## 6. Procedure, validity and reproducibility

1. Explain the study, obtain consent and screen for adult students aged 18-24. Assign a random anonymous participant ID (not a name, email or bank account number).
2. Ask the same baseline questions about attainability, saving intention, financial background and installment obligations **before** revealing group assignment.
3. Randomly allocate eligible participants to A, B or C; use balanced assignment and keep any test seed separate from the real study allocation.
4. Display the identical product/payment terms. A and B receive the same generic summary; C receives the proposed, previously tested personalized AI guidance. Use the same exposure duration and platform when feasible.
5. Ask the same post-exposure questions, including purchase intention and total-cost comprehension.
6. Exclude pilot participants from the real analysis. Apply documented missing-data and consent rules. Report sample sizes, uncertainty and deviations, not only favorable differences.
7. Run the repository script on **synthetic sample data** during Task 2. Real participant data are not collected or published in this deliverable.

**Threats to validity and mitigation:** Convenience sampling limits generalization; self-reported intention does not prove actual savings; short-term change may fade; the personalized treatment combines AI wording and individual feedback; self-selection, attention or model variability may bias results. Mitigate with randomization, a matched generic comparison, frozen stimuli and prompts, safe deterministic cost calculations, pilot checks and transparent reporting. RQ1 remains correlational.

**Reproducibility:** CPython **3.13.5**, PyYAML **6.0.3**, `configs/config.yaml`, nine clearly marked **synthetic** sample rows, tested `python -m src.benchmark`, deterministic financial preview, results written to `outputs/`, and automated `unittest` checks. See README for the complete 3-command Quickstart.

## 7. What is delivered now versus later

**Task 2 deliverables:** public GitHub repository with `README.md`, `.gitignore`, `environment.yml` and `requirements.txt` (direct versions pinned), `configs/config.yaml`, `src/benchmark.py`, a test CSV in `data/sample/`, unit tests, MIT license, this card in PDF/Markdown, and a verified demo log on the author's machine.

**Later stages, not falsely claimed in Task 2:** deployed mobile app, actual model-backed AI treatment, a randomized participant sample, real questionnaire answers, power analysis based on a defensible effect-size assumption, confidence intervals on real results, and bank integration (only if legally and technically available).

**Ethics:** participation is voluntary; obtain appropriate course/institutional approval before collecting human data. Do not ask for passwords, real bank logins, full statements or other sensitive financial details in the public test project. AI financial recommendations must clearly distinguish calculations, uncertainty and financial advice.
