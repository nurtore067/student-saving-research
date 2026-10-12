"""Transparent descriptive metrics for the planned student-saving study.

This file measures *synthetic pilot data only*. It does NOT validate an AI
assistant or estimate real treatment effects from participants.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean

REQUIRED = {
    'participant_id', 'group', 'age', 'consent',
    'goal_attainability_pre', 'goal_attainability_post',
    'saving_intention_pre', 'saving_intention_post',
    'purchase_intention_post', 'total_cost_estimate_kzt',
    'monthly_available_kzt', 'employment_status',
    'monthly_family_support_kzt', 'has_installment_debt'
}
SCALE_FIELDS = (
    'goal_attainability_pre', 'goal_attainability_post',
    'saving_intention_pre', 'saving_intention_post', 'purchase_intention_post'
)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open('r', encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            missing = REQUIRED.difference(reader.fieldnames or [])
            raise ValueError(f'CSV missing required columns: {sorted(missing)}')
        return list(reader)


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    x_bar, y_bar = mean(xs), mean(ys)
    num = sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys))
    den_x = sum((x - x_bar) ** 2 for x in xs)
    den_y = sum((y - y_bar) ** 2 for y in ys)
    return round(num / math.sqrt(den_x * den_y), 4) if den_x and den_y else None


def analyze(rows: list[dict[str, str]], config: dict) -> dict:
    experiment = config['experiment']
    guards = config['guardrails']
    expected_groups = set(experiment['groups'])
    if set('ABC') != expected_groups:
        raise ValueError('This analysis expects A, B, C group labels.')
    if int(experiment['installments']) * int(experiment['installment_kzt']) != int(experiment['product_total_kzt']):
        raise ValueError('Price arithmetic is inconsistent in config.yaml.')
    if not rows:
        raise ValueError('The CSV has no rows.')

    identifiers = set()
    complete = []
    incomplete = 0
    unconsented = 0
    for row_number, row in enumerate(rows, start=2):
        ident = row['participant_id'].strip()
        if not ident or ident in identifiers:
            raise ValueError(f'Blank or duplicate participant_id at CSV row {row_number}.')
        identifiers.add(ident)
        if row['group'] not in expected_groups:
            raise ValueError(f'Unknown group in row {row_number}: {row["group"]!r}')
        if row['consent'] not in ('0', '1'):
            raise ValueError(f'Invalid consent flag in row {row_number}.')
        if row['consent'] == '0':
            unconsented += 1
            continue
        try:
            age = int(row['age'])
        except (ValueError, TypeError):
            incomplete += 1
            continue
        if not experiment['eligible_age_min'] <= age <= experiment['eligible_age_max']:
            raise ValueError(f'Participant age outside stated inclusion criteria at row {row_number}.')
        if any(not row[field] or not row[field].strip() for field in SCALE_FIELDS):
            incomplete += 1
            continue
        try:
            scores = {field: int(row[field]) for field in SCALE_FIELDS}
            cost = int(row['total_cost_estimate_kzt'])
            monthly_available = int(row['monthly_available_kzt'])
            family_support = int(row['monthly_family_support_kzt'])
        except (ValueError, TypeError) as exc:
            raise ValueError(f'Non-numeric value at CSV row {row_number}.') from exc
        if any(not experiment['response_scale_min'] <= value <= experiment['response_scale_max'] for value in scores.values()):
            raise ValueError(f'Score outside 1-7 scale at row {row_number}.')
        if cost < 0 or monthly_available < 0 or family_support < 0:
            raise ValueError(f'Negative monetary value at row {row_number}.')
        if row['has_installment_debt'] not in ('0', '1'):
            raise ValueError(f'Invalid installment-debt flag at row {row_number}.')
        complete.append({
            'id': ident,
            'group': row['group'],
            'scores': scores,
            'delta_goal': scores['goal_attainability_post'] - scores['goal_attainability_pre'],
            'cost_correct': cost == experiment['product_total_kzt'],
        })

    grouped = {name: [r for r in complete if r['group'] == name] for name in ('A', 'B', 'C')}
    if any(not member for member in grouped.values()):
        raise ValueError('Need at least one complete, consented row in each A/B/C group.')

    group_means = {}
    for name, values in grouped.items():
        group_means[name] = {
            'n': len(values),
            'mean_attainability_pre': round(mean(r['scores']['goal_attainability_pre'] for r in values), 4),
            'mean_attainability_post': round(mean(r['scores']['goal_attainability_post'] for r in values), 4),
            'mean_goal_change': round(mean(r['delta_goal'] for r in values), 4),
            'mean_saving_intention_pre': round(mean(r['scores']['saving_intention_pre'] for r in values), 4),
            'mean_saving_intention_post': round(mean(r['scores']['saving_intention_post'] for r in values), 4),
            'mean_purchase_intention_post': round(mean(r['scores']['purchase_intention_post'] for r in values), 4),
        }
    rate_base = len(rows) - unconsented
    incomplete_rate = round(incomplete / rate_base, 4) if rate_base else 1.0
    price_rate = round(sum(r['cost_correct'] for r in complete) / len(complete), 4)
    primary_diff = round(group_means['C']['mean_goal_change'] - group_means['B']['mean_goal_change'], 4)
    framing_diff = round(group_means['B']['mean_purchase_intention_post'] - group_means['A']['mean_purchase_intention_post'], 4)
    correlation = pearson(
        [r['scores']['goal_attainability_pre'] for r in complete],
        [r['scores']['saving_intention_pre'] for r in complete],
    )
    return {
        'data_type': 'SYNTHETIC_FIXTURE_NOT_REAL_PARTICIPANTS',
        'research_status': 'pipeline_test_only; no p-values or causal claims',
        'sample': {'rows_total': len(rows), 'consented_complete': len(complete),
                   'unconsented_excluded': unconsented, 'incomplete_excluded': incomplete},
        'group_means': group_means,
        'primary_metric': {'name': 'difference_in_mean_goal_attainability_change_C_minus_B',
                           'value_scale_points': primary_diff,
                           'interpretation': 'descriptive test on synthetic data ONLY'},
        'secondary_metrics': {'price_emphasis_purchase_intention_B_minus_A': framing_diff,
                              'baseline_attainability_vs_saving_intention_pearson_r': correlation,
                              'rq3_interaction': 'planned for adequately powered real sample; not estimated here'},
        'guardrails': {'installment_total_math_valid': True,
                       'incomplete_response_rate': incomplete_rate,
                       'incomplete_rate_within_threshold': incomplete_rate <= guards['max_incomplete_rate'],
                       'price_comprehension_rate': price_rate,
                       'price_comprehension_meets_threshold': price_rate >= guards['min_price_comprehension_rate']},
    }
