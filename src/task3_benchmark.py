"""Measure real CPU execution of generic and personalized guidance."""
import csv
import hashlib
import json
import platform
import random
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from src.mentor_preview import plan_preview

ROOT = Path(__file__).resolve().parents[1]
SEED = 3242
LOADS = [10, 100, 330]
WARMUP = 20
REPEATS = 200


def load_profiles():
    with (ROOT / 'data/synthetic/synthetic_responses_330.csv').open(encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    # essential_kzt already includes existing installments: subtract them here
    # because plan_preview receives that cost separately.
    return [dict(income=int(r['monthly_income_kzt']),
                 essential_spend=int(r['monthly_essential_kzt'])-int(r['monthly_installment_kzt']),
                 existing_payments=int(r['monthly_installment_kzt']),
                 target=int(r['goal_target_kzt']), already_saved=int(r['current_goal_savings_kzt']))
            for r in rows]


def generic(profile):
    return {'installment_total_cost': 24000,
            'message': 'Check your budget and saving goal before buying. Four payments of 6000 KZT cost 24000 KZT.'}


def personalized(profile):
    return plan_preview(**profile)


METHODS = {'Baseline': generic, 'Proposed': personalized}


def run_batch(method, profiles):
    return [METHODS[method](p) for p in profiles]


def valid_output(method, output, profiles):
    if len(output) != len(profiles):
        return False
    for result, p in zip(output, profiles):
        if result['installment_total_cost'] != 24000:
            return False
        if method == 'Proposed':
            free = p['income']-p['essential_spend']-p['existing_payments']
            if result['monthly_free_before_purchase'] != free:
                return False
            if result['affordability_warning'] != (free < 6000):
                return False
    return True


def main():
    profiles = load_profiles()
    rng = random.Random(SEED)
    rng.shuffle(profiles)
    batches = {n: profiles[:n] for n in LOADS}
    logs = []
    started = datetime.now(timezone.utc).isoformat()
    # Each block runs all loads and both methods in randomized order.
    # One measurement = one whole batch, not one student.
    for phase, count in [('warmup', WARMUP), ('benchmark', REPEATS)]:
        for repeat in range(count):
            order = [(n, method) for n in LOADS for method in METHODS]
            rng.shuffle(order)
            for load, method in order:
                error = None
                start = time.perf_counter_ns()
                try:
                    output = run_batch(method, batches[load])
                except Exception as exc:
                    error = type(exc).__name__
                elapsed = time.perf_counter_ns()-start
                # Validation and file writing are outside the timed region.
                if error is None and not valid_output(method, output, batches[load]):
                    error = 'InvalidOutput'
                logs.append(dict(phase=phase, repeat=repeat, load=load, method=method,
                                 latency_ms=elapsed/1e6, ok=error is None, error=error))
    raw = ROOT / 'data/raw/test_run.jsonl'
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw.write_text(''.join(json.dumps(r)+'\n' for r in logs), encoding='utf-8')
    metadata = dict(started_utc=started, ended_utc=datetime.now(timezone.utc).isoformat(),
                    python=sys.version, platform=platform.platform(), processor=platform.processor(),
                    timer=time.get_clock_info('perf_counter')._asdict() if hasattr(time.get_clock_info('perf_counter'), '_asdict') else str(time.get_clock_info('perf_counter')),
                    seed=SEED, loads=LOADS, warmup_per_configuration=WARMUP,
                    measurements_per_configuration=REPEATS, unit='batch latency in ms',
                    execution_location='ChatGPT execution environment, not student laptop',
                    workload='fixed nested subsets of the same 330 synthetic profiles; sequential CPU batches',
                    baseline_revision=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True).stdout.strip(),
                    files_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in [raw, ROOT/'data/synthetic/synthetic_responses_330.csv',
                                  Path(__file__), ROOT/'src/mentor_preview.py']})
    (ROOT/'data/raw/run_metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    print(f'Saved {len(logs)} actual measurements; errors: {sum(not r["ok"] for r in logs)}')


if __name__ == '__main__':
    main()
