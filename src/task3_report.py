"""Create a concise submission report from the actual saved results."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def write_reports(summary, survey_summary):
    lines=['| Profiles | Method | Median (p25–p75), ms | 95% CI of median, ms | p95 / p99, ms | Errors |',
           '|---:|---|---|---|---|---:|']
    for r in summary.itertuples():
        lines.append(f'| {r.load} | {r.method} | {r.median_ms:.4f} ({r.p25_ms:.4f}–{r.p75_ms:.4f}) | {r.ci_low_ms:.4f}–{r.ci_high_ms:.4f} | {r.p95_ms:.4f} / {r.p99_ms:.4f} | {r.errors}/{r.attempts} |')
    table='\n'.join(lines)
    d=summary[summary.load==330].set_index('method')
    b,p=d.loc['Baseline'],d.loc['Proposed']
    discussion=f'''At 330 profiles, Baseline took a median of {b.median_ms:.4f} ms per batch and
Proposed took {p.median_ms:.4f} ms. The observed ratio of medians was {p.median_ms/b.median_ms:.1f}.
This is an overhead comparison: Proposed performs personalized calculations and creates a larger output.
It is not a fair comparison of two algorithms solving an identical task, and no speed improvement is claimed.
There were {int(summary.errors.sum())} failed batches out of {int(summary.attempts.sum())} measured attempts.
The 0% target guardrail is {'met' if summary.errors.sum()==0 else 'NOT met'} in this run.
Successful timings alone do not hide failures: the table retains all attempts in the error denominator.
'''
    report=f'''# Task 3: Results, analysis and visualization

**Authors:** Gumar Nurtore and Kydyralina Akniet  
**Project:** Why Saving Seems Pointless to Students  
**Status:** Technical prototype evaluation; synthetic profiles; no human study.

## Aim and connection to Task 2

The planned study examines saving-goal attainability, installment price emphasis and personalized guidance.
Task 2 provided a questionnaire, an A/B/C design and a rule-based calculator. This task measures the execution
cost of that calculator compared with fixed generic guidance. The human hypotheses remain open.
No language model is called by either method.

## Data and methods

We use 330 synthetic profiles, assigned to A/B/C in equal groups of 110. Profiles and post-scores were
created with explicit rules and fixed seeds; their frequencies are not estimates for Almaty students.
Both technical methods receive the same financial inputs irrespective of survey group. B/C in the human
protocol and Baseline/Proposed in this timing test are related concepts but different experimental units.

A measurement is one sequential batch of 10, 100 or 330 profiles. There are 20 warm-up and 200 measured
runs for each of six configurations. Method and load order are randomized within repeat blocks.
A monotonic high-resolution timer surrounds only batch execution. CSV reading, output checking and
log writes are outside the timed interval. Errors are retained in the logs. We filter warm-up by phase.
The bootstrap median CI uses 2000 resamples and seed 3242; the error rate uses all attempts.

## Results & Discussion

{table}

{discussion}

The synthetic survey has {len(survey_summary)} groups and {int(survey_summary.n.sum())} rows. Its score means are
saved in data/processed/synthetic_survey_summary.csv for pipeline inspection only. They do not test the
human hypothesis: the post-scores depend on invented generation rules. A meaningful behavioral study
still requires real voluntary participants, a frozen treatment and prespecified outcome analysis.

## Domain model and outputs

The C4 component model in docs/domain_model.md shows the implemented calculator, generic reminder,
measurement boundary, validation and log store. The notebook is executed in sequential order with visible
outputs. Both figures show latency in milliseconds, use distinct colors and markers, and include median
95% confidence intervals. PNG exports use 300 DPI and PDF exports are vector graphics.

## Limitations

One execution environment and one session were measured. These small timings are sensitive to interpreter
and shared-host noise. Bootstrap intervals may understate uncertainty if observations are temporally
dependent. With 200 runs, p99 describes very few tail observations. Zero errors on valid profiles does not
prove all possible inputs are safe. The fixed arithmetic assumes stable income and saving every free tenge.
RAM, API response time, LLM quality, actual saving and student satisfaction were not measured.
The next practical steps are repeated sessions on the students' computers, a real pilot questionnaire,
and evaluation of a controlled AI-assisted intervention. No claim about population behavior follows here.

## Reproduction

Install requirements.txt and run `python run_task3.py` to reprocess the supplied logs and execute the
notebook. Run `python run_task3.py --measure` to replace timings with new local measurements and refresh
all results. If your environment blocks Jupyter kernel sockets, add `--in-process`.
The delivered outputs were obtained with this IPython mode, not a separate Jupyter kernel.
The input CSV and bootstrap are reproducible; execution times naturally vary.
The source of the recorded run, Python, platform, timestamps and file hashes are in data/raw/run_metadata.json.

## AI assistance

ChatGPT assisted with code, synthetic data, analysis and explanatory drafts. This is a review draft for the
two named students. The names identify the project team; no claim is made that they independently wrote
or reviewed every generated line. Team members should review, run and explain their assigned parts before
submitting, and follow their course's AI disclosure rules.
'''
    (ROOT/'reports/task3_report.md').write_text(report,encoding='utf-8')
    readme=f'''# Why Saving Seems Pointless to Students

**Gumar Nurtore and Kydyralina Akniet — Research Methods, Task 3**

Technical evaluation of a rule-based saving coach prototype. Inputs are synthetic;
recorded timings are real. No human participants or generative AI intervention were tested.

## Research context

The original A/B/C design studies total-price emphasis, installment emphasis and personalized guidance.
The [Task 2 overview](docs/task2_overview.md) and [original protocol](docs/experimental_protocol.md)
are retained. This task asks how much computation the personalized calculator adds to a fixed reminder.
It cannot establish whether an AI assistant changes students' behavior.

## Quickstart

Use Python 3.12 in a virtual environment, from this repository root:

```bash
python -m pip install -r requirements.txt
python run_task3.py
```

If kernel startup is blocked, use `python run_task3.py --in-process`.

This executes the notebook and recreates summaries, figures, this README and the report from the supplied
logs. To collect a new run on your own computer, use `python run_task3.py --measure` instead of the second
command. This replaces the saved measurements; results will change. No GPU or API key is needed.
Conda alternative: `conda env create -f environment.yml`, then `conda activate saving-research-task3`.
For interactive editing, open the notebook in VS Code with the Jupyter extension and the same environment.

## Files

| Path | Purpose |
|---|---|
| data/synthetic/ | 330 profiles, generation manifest and checks |
| data/raw/test_run.jsonl | 1320 recorded batch measurements, including warm-up |
| data/raw/run_metadata.json | Measurement environment, timestamps and hashes |
| data/processed/metrics_summary.csv | Latency statistics and error rates |
| notebooks/01_data_analysis.ipynb | Executed notebook with visible outputs |
| src/task3_benchmark.py | Input adapter, fixed reminder and measurement runner |
| src/mentor_preview.py | Existing Task 2 personalized calculator |
| src/process_data.py, src/visualize.py | Statistics and figure export |
| src/task3_report.py | Report/README generation from saved statistics |
| scripts/generate_dataset.py | Reproduce the synthetic input data |
| reports/task3_report.md | Submission report; review before LMS upload |
| docs/domain_model.md | C4 component diagram and arithmetic definitions |
| docs/task3_protocol.md | Measurement design and limitations |
| docs/questionnaire_ru.md | Extended survey for future piloting |

## Results & Discussion

A batch is a sequential list of profiles, not simultaneous users. Each method/load has 200 measured
runs after 20 warm-ups. CI = 2000-resample percentile bootstrap interval for the median.

{table}

{discussion}

![Median batch latency with 95% CI](reports/figures/fig1_latency_vs_load.png)

![Latency distribution and median CI](reports/figures/fig2_distribution_boxplot.png)

The box shows quartiles and 1.5-IQR whiskers; dots show outliers. Adjacent markers show median CIs.
Vector PDF versions are in the same folder. [Domain model](docs/domain_model.md).

## Interpretation and limitations

Proposed performs more work than Baseline. Timing differences are overhead, not evidence of better
financial decisions. There is one host/session; p99 and CIs are sensitive to noise and dependence.
The [synthetic-data notes](docs/synthetic_data_notes.md) explain invented response coefficients.
Synthetic group differences cannot validate the human study. No savings behavior was observed.

## Checks and provenance

`python -m unittest discover -s tests -v` checks the original pipeline and the Task 3 additions.
The delivered notebook cells were executed from start to finish using IPython in a fresh Python process.
Separate kernel sockets are blocked on the authoring host; use Jupyter Restart & Run All locally before submission. New measurements were obtained in the
ChatGPT execution environment; details are in run_metadata.json. Direct dependency versions are pinned.
The old Task 2 sample still runs with `python -m src.benchmark`.
Generated source and report drafts used ChatGPT assistance; the project team must review and understand
its contributions before submission. Review guidance is in [the Russian guide](docs/TASK3_GUIDE_RU.md).

[MIT license](LICENSE). No private student data is included.
'''
    (ROOT/'README.md').write_text(readme,encoding='utf-8')
