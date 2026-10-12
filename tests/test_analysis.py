"""Standard-library unit tests. Run: python -m unittest discover -s tests -v"""

import copy
import unittest
from pathlib import Path
import yaml

from src.analysis import analyze, load_csv, pearson
from src.benchmark import ROOT, run


class TestStudyMetrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = ROOT / 'configs/config.yaml'
        cls.config = yaml.safe_load(cls.config_path.read_text(encoding='utf-8'))
        cls.rows = load_csv(ROOT / cls.config['files']['sample_csv'])

    def test_nine_synthetic_rows_three_groups(self):
        result = analyze(self.rows, self.config)
        self.assertEqual(result['sample']['consented_complete'], 9)
        self.assertEqual([result['group_means'][g]['n'] for g in 'ABC'], [3, 3, 3])
        self.assertIn('SYNTHETIC', result['data_type'])

    def test_primary_formula_is_c_minus_b(self):
        result = analyze(self.rows, self.config)
        mean_b = result['group_means']['B']['mean_goal_change']
        mean_c = result['group_means']['C']['mean_goal_change']
        self.assertAlmostEqual(result['primary_metric']['value_scale_points'], mean_c - mean_b, places=4)

    def test_secondary_formula_is_b_minus_a(self):
        result = analyze(self.rows, self.config)
        expected = (result['group_means']['B']['mean_purchase_intention_post']
                    - result['group_means']['A']['mean_purchase_intention_post'])
        self.assertAlmostEqual(result['secondary_metrics']['price_emphasis_purchase_intention_B_minus_A'],
                               expected, places=4)

    def test_guardrails_and_math(self):
        result = analyze(self.rows, self.config)
        self.assertTrue(result['guardrails']['installment_total_math_valid'])
        self.assertEqual(result['guardrails']['price_comprehension_rate'], 1.0)
        self.assertEqual(result['guardrails']['incomplete_response_rate'], 0)

    def test_duplicate_id_rejected(self):
        rows = copy.deepcopy(self.rows)
        rows[1]['participant_id'] = rows[0]['participant_id']
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            analyze(rows, self.config)

    def test_wrong_group_rejected(self):
        rows = copy.deepcopy(self.rows)
        rows[0]['group'] = 'Z'
        with self.assertRaisesRegex(ValueError, 'Unknown group'):
            analyze(rows, self.config)

    def test_out_of_range_score_rejected(self):
        rows = copy.deepcopy(self.rows)
        rows[0]['goal_attainability_post'] = '8'
        with self.assertRaisesRegex(ValueError, 'outside 1-7'):
            analyze(rows, self.config)

    def test_incomplete_row_is_counted_not_invented(self):
        rows = copy.deepcopy(self.rows)
        rows[0]['saving_intention_post'] = ''
        result = analyze(rows, self.config)
        self.assertEqual(result['sample']['incomplete_excluded'], 1)
        self.assertEqual(result['sample']['consented_complete'], 8)

    def test_unconsented_row_is_excluded(self):
        rows = copy.deepcopy(self.rows)
        rows[0]['consent'] = '0'
        result = analyze(rows, self.config)
        self.assertEqual(result['sample']['unconsented_excluded'], 1)

    def test_price_mismatch_rejected(self):
        wrong = copy.deepcopy(self.config)
        wrong['experiment']['installment_kzt'] = 6500
        with self.assertRaisesRegex(ValueError, 'Price arithmetic'):
            analyze(self.rows, wrong)

    def test_no_correlation_when_constant(self):
        self.assertIsNone(pearson([3, 3, 3], [1, 2, 3]))

    def test_cli_pipeline_produces_expected_files(self):
        report = run(self.config_path)
        self.assertEqual(report['sample']['rows_total'], 9)
        for file_name in ('output_json', 'output_csv', 'output_log'):
            self.assertTrue((ROOT / self.config['files'][file_name]).is_file())


if __name__ == '__main__':
    unittest.main()
