"""Warm-up exclusion and bootstrap summaries of measured batch times."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_logs(path=None):
    df = pd.read_json(path or ROOT/'data/raw/test_run.jsonl', lines=True)
    if df.duplicated(['phase','repeat','load','method']).any():
        raise ValueError('Duplicate measurement key')
    if not df['phase'].isin(['warmup','benchmark']).all() or (df.latency_ms < 0).any():
        raise ValueError('Invalid phase or time')
    return df


def summarize(df, seed=3242, bootstrap_samples=2000):
    rng = np.random.default_rng(seed)
    results = []
    measured = df[df.phase == 'benchmark']
    for (load, method), group in measured.groupby(['load','method'], sort=True):
        # Successful latency and error rate have separate, explicit denominators.
        x = group.loc[group.ok, 'latency_ms'].to_numpy()
        row = dict(load=load, method=method, attempts=len(group), successes=len(x),
                   errors=int((~group.ok).sum()), error_rate=float((~group.ok).mean()))
        if len(x):
            boot = np.median(rng.choice(x, size=(bootstrap_samples,len(x)),replace=True),axis=1)
            row.update(mean_ms=x.mean(), sd_ms=x.std(ddof=1), median_ms=np.median(x),
                       p25_ms=np.percentile(x,25), p75_ms=np.percentile(x,75),
                       p95_ms=np.percentile(x,95), p99_ms=np.percentile(x,99),
                       ci_low_ms=np.percentile(boot,2.5), ci_high_ms=np.percentile(boot,97.5))
        else:
            row.update({k:np.nan for k in ['mean_ms','sd_ms','median_ms','p25_ms','p75_ms',
                         'p95_ms','p99_ms','ci_low_ms','ci_high_ms']})
        results.append(row)
    return pd.DataFrame(results)


def main():
    result = summarize(load_logs())
    target = ROOT/'data/processed/metrics_summary.csv'
    target.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(target,index=False)
    print(result.to_string(index=False))


if __name__ == '__main__':
    main()
