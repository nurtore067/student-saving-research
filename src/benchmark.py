"""Run reproducible sample-data benchmark from the repository root.

Usage: python -m src.benchmark [--config configs/config.yaml]
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import yaml

from src.analysis import analyze, load_csv

ROOT = Path(__file__).resolve().parents[1]


def run(config_path: Path) -> dict:
    with config_path.open('r', encoding='utf-8') as stream:
        config = yaml.safe_load(stream)
    input_path = ROOT / config['files']['sample_csv']
    output_json = ROOT / config['files']['output_json']
    output_csv = ROOT / config['files']['output_csv']
    output_log = ROOT / config['files']['output_log']

    report = analyze(load_csv(input_path), config)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    with output_csv.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['group', 'n', 'mean_goal_change', 'mean_purchase_intention_post'])
        for group in ('A', 'B', 'C'):
            item = report['group_means'][group]
            writer.writerow([group, item['n'], item['mean_goal_change'], item['mean_purchase_intention_post']])
    message = (
        'SYNTHETIC DATA ONLY - THIS IS NOT A HUMAN EXPERIMENT RESULT\n'
        f'Valid rows: {report["sample"]["consented_complete"]}\n'
        f'Primary (C minus B, goal-change points): {report["primary_metric"]["value_scale_points"]:+.4f}\n'
        f'Secondary (B minus A, purchase-intention points): '
        f'{report["secondary_metrics"]["price_emphasis_purchase_intention_B_minus_A"]:+.4f}\n'
        'Files: outputs/demo_results.json, outputs/demo_group_summary.csv\n'
    )
    output_log.write_text(message, encoding='utf-8')
    print(message, end='')
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description='Validate and summarize synthetic experiment data')
    parser.add_argument('--config', type=Path, default=ROOT / 'configs/config.yaml')
    args = parser.parse_args()
    config_path = args.config if args.config.is_absolute() else ROOT / args.config
    run(config_path)


if __name__ == '__main__':
    main()
