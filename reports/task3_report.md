# Task 3: Results, analysis and visualization

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

| Profiles | Method | Median (p25–p75), ms | 95% CI of median, ms | p95 / p99, ms | Errors |
|---:|---|---|---|---|---:|
| 10 | Baseline | 0.0045 (0.0021–0.0074) | 0.0042–0.0047 | 0.0154 / 0.0237 | 0/200 |
| 10 | Proposed | 0.0178 (0.0157–0.0239) | 0.0171–0.0191 | 0.0332 / 0.0470 | 0/200 |
| 100 | Baseline | 0.0106 (0.0077–0.0164) | 0.0104–0.0111 | 0.0215 / 0.0349 | 0/200 |
| 100 | Proposed | 0.1342 (0.1239–0.1510) | 0.1305–0.1397 | 0.2231 / 0.3748 | 0/200 |
| 330 | Baseline | 0.0260 (0.0229–0.0335) | 0.0251–0.0280 | 0.0519 / 0.0786 | 0/200 |
| 330 | Proposed | 0.4291 (0.4021–0.4835) | 0.4134–0.4402 | 0.7008 / 0.8677 | 0/200 |

At 330 profiles, Baseline took a median of 0.0260 ms per batch and
Proposed took 0.4291 ms. The observed ratio of medians was 16.5.
This is an overhead comparison: Proposed performs personalized calculations and creates a larger output.
It is not a fair comparison of two algorithms solving an identical task, and no speed improvement is claimed.
There were 0 failed batches out of 1200 measured attempts.
The 0% target guardrail is met in this run.
Successful timings alone do not hide failures: the table retains all attempts in the error denominator.


The synthetic survey has 3 groups and 330 rows. Its score means are
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

## AI Assistance

ChatGPT was used as a supporting tool for code development, synthetic data generation, statistical analysis, and documentation.

The project was developed collaboratively by Gumar Nurtore and Kydyralina Akniet. Nurtore conducted the technical benchmarks on Windows, while Akniet performed the statistical analysis and prepared the visualizations on macOS.

The authors are responsible for the final research results, interpretation, and conclusions.
