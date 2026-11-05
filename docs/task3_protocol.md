# Task 3 technical experiment

The original Task 1/2 question concerns students, price framing and perceived saving attainability.
That question remains untested on humans. Task 3 implements a narrower technical question:
what is the execution cost of adding the existing personalized calculator to generic guidance?

Baseline returns a fixed total-cost reminder. Proposed calls the existing plan_preview function.
The two outputs have different capabilities. We measure the cost of additional work; this is not
an algorithm speedup comparison between equivalent implementations, nor proof of better advice.
The generic reminder is a technical analogue of group B; Proposed is a technical analogue of C.
A is retained in the synthetic survey only. Each technical method processes the SAME financial
inputs regardless of the assigned survey group; generated post-treatment scores are never inputs.

## Predefined configuration

- Seed 3242; fixed shuffled subsets of 10, 100 and 330 profiles.
- 20 warm-up batches and 200 measured batches per method and load.
- Both method order and load order are randomized within each repeat block.
- Six configurations: 2 methods x 3 loads. Total 1320 logs, 1200 retained.
- Each timer measures one batch, including output construction. No I/O inside the timed region.
- No network requests or retries. Exceptions and failed invariants count as batch errors.
- Median, mean, sample SD, p25, p75, p95 and p99 use successful batches.
- Error rate = failed batches / ALL measured batches for that configuration.
- 2000 bootstrap resamples, percentile 95% CI for median, seed 3242.
- Error guardrail target is 0% on this valid-input scenario set. A nonzero rate requires investigation.

330 is a chosen scenario budget with 110 records per survey arm, not a population sample-size calculation.
200 repeated runs provide an inexpensive teaching benchmark; no precision-based stopping or power claim
is made. p99 is exploratory because only about two observations occupy the top 1% in each configuration.

## Scope and limitations

Timing was collected on Nurtore's Windows 11 computer. See data/raw/run_metadata.json for actual
Python, platform, UTC time and hashes. These are real measurements, not generated timing values.
Operating-system scheduling, interpreter overhead and memory allocation affect these small durations.
Only one session and one environment were used. No dedicated CPU affinity or memory limit was set.
Bootstrap CIs describe resampling variability of recorded runs on these fixed inputs. Temporal dependence
and host noise can make them optimistic; they do not measure uncertainty about real students.
A second machine and multiple sessions are future improvements. No RAM, energy, LLM quality or
end-to-end application latency is claimed. The survey outcomes are produced by chosen rules,
so their contrasts cannot establish a behavioral treatment effect.

## Protocol changes from Task 2

The original human experiment and questionnaire are retained. The new Russian questionnaire adds
financial details and headphone need for future piloting. The original instrument was not overwritten.
The 330-row extension is marked synthetic. The technical experiment is an added feasibility check;
it does not replace the planned human experiment or claim completion of its hypotheses.
