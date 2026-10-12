import unittest
from src.mentor_preview import plan_preview


class TestRuleBasedPreview(unittest.TestCase):
    def test_normal_plan(self):
        report = plan_preview(income=90000, essential_spend=55000, existing_payments=10000,
                              target=100000, already_saved=20000)
        self.assertEqual(report['installment_total_cost'], 24000)
        self.assertEqual(report['monthly_free_before_purchase'], 25000)
        self.assertEqual(report['months_to_goal_without_purchase'], 4)
        self.assertEqual(report['months_to_goal_with_installments'], 5)
        self.assertFalse(report['affordability_warning'])

    def test_no_free_cash(self):
        report = plan_preview(income=40000, essential_spend=38000, existing_payments=6000,
                              target=100000, already_saved=0)
        self.assertIsNone(report['months_to_goal_without_purchase'])
        self.assertIsNone(report['months_to_goal_with_installments'])
        self.assertTrue(report['affordability_warning'])

    def test_goal_already_reached(self):
        report = plan_preview(income=20000, essential_spend=15000, existing_payments=0,
                              target=20000, already_saved=25000)
        self.assertEqual(report['months_to_goal_without_purchase'], 0)
        self.assertEqual(report['months_to_goal_with_installments'], 0)

    def test_negative_input_rejected(self):
        with self.assertRaises(ValueError):
            plan_preview(income=-1, essential_spend=0, existing_payments=0,
                         target=20000, already_saved=0)


if __name__ == '__main__':
    unittest.main()
