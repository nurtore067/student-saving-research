# 2-minute reproducibility checklist

- [ ] Public repo opens in a logged-out browser; authors and title appear.
- [ ] `README.md` explains RQ/H0/H1, conditions, system needs, Quickstart,
      example output, license and citation.
- [ ] `requirements.txt` and `environment.yml` pin Python and direct package
      versions; `config.yaml` contains inputs, settings and group labels.
- [ ] `python -m src.benchmark` runs from the repo root and creates three
      `outputs/demo_*` artifacts using nine **synthetic** CSV rows.
- [ ] `python -m unittest discover -s tests -v` passes, including malformed
      data and invalid installment math checks.
- [ ] `.gitignore` excludes caches, environments, secrets, real participant
      data and generated logs; Git history shows meaningful team contributions.
- [ ] The methodology card PDF includes the **real GitHub URL** and is
      uploaded to LMS with the same public link.

## Rubric crosswalk (Task 2, total 100 points)

| Item | Max | Current file(s) to review |
|---|---:|---|
| Methodology: H0/H1, variables, baseline, primary/guardrail | 30 | `docs/methodology_passport.md`, external PDF |
| Executable measured pipeline, pinned environment, sample, config | 30 | `environment.yml`, `requirements.txt`, `configs/config.yaml`, `src/benchmark.py`, `data/sample/`, `tests/` |
| Academic English README, benchmark and 2-3-command quickstart | 20 | `README.md` |
| Git hygiene and informative commit history | 20 | `.gitignore`, directory layout; **real contributor commits must be made on GitHub** |

**Not externally verified here:** a live GitHub public URL, a GitHub contribution
history from both authors, an independent reviewer environment, and any real
AI-assisted participant experiment. These require actions outside this zip.
