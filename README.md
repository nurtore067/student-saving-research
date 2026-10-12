# Why Saving Seems Pointless to Students

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Status: research prototype](https://img.shields.io/badge/Status-Task%202%20prototype-64748b)
![Data: synthetic](https://img.shields.io/badge/Data-Synthetic%20only-orange)

**Full title:** Why Saving Seems Pointless to Students: The Role of Financial Expectations and Digital Purchase Incentives  
**Authors:** Gumar Nurtore and Kydyralina Akniet  
**Research Methods - Task 2 / Methodology Passport Card and Reproducible Research Repository**  
**Status:** Planned quantitative study, tested analysis pipeline; **not** a completed AI intervention or human study.

## 1. Project overview, research question and hypotheses

We study whether students' views about their ability to save are connected to
saving intention and whether highlighting installment payments changes purchase
intention. We also propose an **AI Saving Coach** for students in Kazakhstan:
a future mobile app with manual income and expense entry, saving goals, step-by-step
plans, progress widgets and clear total-installment-cost explanations. Bank
integration is only a future possibility. No real bank account data is used here.

**Primary RQ (Task 2 extension):** Does a proposed AI-assisted personalized saving
coach increase perceived saving-goal attainability compared with generic
financial information when the same installment offer is shown?

**Primary H0:** Mean pre-to-post attainability change is the same in B and C.  
**Primary H1:** Mean change differs between B and C; we predict higher change in C.

**Task 1 questions retained:** (1) goal attainability and saving intention;
(2) total-price vs installment *emphasis* and purchase intention;
(3) exploratory moderation by baseline goal attainability. Their full H0/H1
and covariates are in [the Methodology Card](docs/methodology_passport.md).

**Important scientific boundary:** the current Python code validates the
measurement pipeline on synthetic data. `src/mentor_preview.py` is a **rule-based
calculation demonstration, not a generative AI model**. Real AI treatment and
human outcome validation are planned for later, not claimed in this repo.

## 2. Experimental design and variables

| Group | Product card (BOTH prices remain visible) | Guidance | Valid comparison |
|---|---|---|---|
| A | Total **24,000 KZT** visually emphasized; 4 x 6,000 also present | Generic financial summary | A vs B for price prominence |
| B | **4 x 6,000 KZT** visually emphasized; 24,000 total also present | Same generic summary | Baseline for C |
| C | Same card as B | Planned personalized AI-assisted guidance | B vs C for guidance package |

**Independent:** randomized price prominence (A/B) or assigned guidance (B/C).
**Dependent:** perceived goal attainability change, purchase intention,
saving intention (1-7 response scales). **Controlled:** exact product, total
price, credit terms, fees, copy, platform, pre/post wording and comparable
exposure. Baseline financial status and attainability are measured, not
experimentally assigned. The B/C comparison tests a *package*, not proof
that LLMs outperform matched personalized non-AI advice.

**Primary metric:** `mean(attainability_post - attainability_pre in C) -
mean(attainability_post - attainability_pre in B)` (points on the 1-7 scale).
**Secondary:** `mean(purchase_intention in B) - mean(... in A)`;
pre-treatment correlation of attainability/saving intention.
**Guardrails:** <=10% incomplete responses, >=80% exact 24,000 KZT price
comprehension, `4 * 6,000 = 24,000` verified; no private financial data.

## 3. Repository structure

```text
student-saving-research/
├── README.md                     Academic overview and Quickstart
├── LICENSE                       MIT license
├── .gitignore                    No secrets, virtualenvs, logs, or raw human data
├── .python-version               CPython 3.13.5
├── requirements.txt              Direct packages with exact versions
├── environment.yml              Pinned Conda alternative
├── configs/
│   └── config.yaml               Groups, prices, sample paths, thresholds
├── data/
│   └── sample/
│       └── sample_responses.csv  9 invented records; NO participants
├── src/
│   ├── analysis.py               Score validation, group statistics, guardrails
│   ├── benchmark.py              Executable measurement pipeline
│   └── mentor_preview.py         Rule-based financial arithmetic demonstration
├── tests/                        Automated tests with invalid data cases
├── outputs/                      Created on run; ignored by git
└── docs/
    ├── methodology_passport.md   Full methodology card
    ├── experimental_protocol.md  Conditions, design, limitations
    ├── survey_instrument.md      Draft survey wording
    ├── ai_system_design.md       Proposed AI MVP architecture and privacy
    ├── reproducibility_checklist.md
    └── demo_run_output.txt       Verified example of synthetic test run
```

## 4. System requirements

- **Tested** with **CPython 3.13.5** and **PyYAML 6.0.3**.
- Windows, macOS or Linux terminal; no GPU, CUDA, database or bank account.
- Rough guide: 1 CPU core and 512 MB of RAM for the nine-row sample.
- Run commands from the repository root. Conda users can alternatively create
  the pinned environment with `conda env create -f environment.yml` and
  `conda activate saving-research-task2`.

## 5. Quickstart (3 commands)

```bash
python -m pip install -r requirements.txt
python -m src.benchmark
python -m unittest discover -s tests -v
```

`python -m src.benchmark` reads `configs/config.yaml`, validates synthetic
`data/sample/sample_responses.csv`, and generates:

- `outputs/demo_results.json` - machine-readable metrics and guardrails.
- `outputs/demo_group_summary.csv` - group aggregates.
- `outputs/demo_run.log` - short test log.

For a separate **non-AI** money calculator demonstration, optionally run
`python -m src.mentor_preview`. It shows how installments can affect projected
saving time, under explicit simplifying assumptions.

## 6. Expected benchmark / evaluation results

The following are **output definitions, not findings** from real students.

| Evaluation metric | Source | Unit / expected behavior |
|---|---|---|
| Goal attainment change (C - B) | Synthetic pilot CSV | Mean difference in scale points; the sample output is only a test |
| Purchase intention (B - A) | Synthetic pilot CSV | Difference of means, 1-7 scale points |
| Initial attainability vs saving intention | Synthetic pilot CSV | Descriptive Pearson r; future adjusted model on real data |
| Missing response rate | Pilot CSV | <= 10% target; reports current fraction |
| Price comprehension rate | Pilot CSV | >= 80% target; correct total is 24,000 KZT |
| Runtime / pipeline | Local machine | Script succeeds, 3 files created, tests pass |

**Do not report these synthetic numbers as an experimental result.** An actual
AI intervention is not present; no real survey outcomes have been collected.
For a later participant study, report sample sizes, group means, 95% CIs,
pre-specified comparisons and limitations. The earlier Task 1 exploratory
interaction is not computed from just nine invented rows.

## 7. Reproducibility, limitations and ethics

Environment file pins direct versions and config controls the inputs. All demo
calculations are deterministic, with no remote APIs, model downloads or private
bank accounts. Both payment representations keep the exact same terms; only
visual prominence varies. The sample is synthetic; other researchers can
re-run the pipeline but **cannot reproduce evidence that has not yet been
collected**. The direct environment has been tested locally; installation on
every OS is not guaranteed and must be verified by independent reviewers.

Real recruitment requires voluntary consent, careful handling of sensitive
financial information and appropriate institutional/course approval. Human data
must not be committed to the public repository. Use fixed prompts and review
future AI messages for arithmetic errors and unsafe financial claims.

## 8. Citation and license

If referencing this repository, cite:

```bibtex
@misc{gumar_kydyralina_2026_saving_research,
  author = {Gumar, Nurtore and Kydyralina, Akniet},
  title = {Why Saving Seems Pointless to Students: The Role of Financial Expectations and Digital Purchase Incentives},
  year = {2026},
  note = {Research Methods Task 2; methodology and reproducible synthetic-data demo},
  howpublished = {Public GitHub repository (insert final URL before submission)}
}
```

Source code and original synthetic files are released under the [MIT License](LICENSE).
Actual participants' identifiable financial data must **not** be public or
implicitly covered by this license.

**Submission:** attach the PDF Methodology Passport Card in Canvas/LMS and
paste the public GitHub repo URL. Replace the PDF/Markdown GitHub placeholder
only when your real GitHub repo exists.
