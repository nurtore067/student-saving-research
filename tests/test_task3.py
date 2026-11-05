import unittest
import pandas as pd
from src.mentor_preview import plan_preview
from src.task3_benchmark import load_profiles
from src.process_data import summarize

class Task3Tests(unittest.TestCase):
    def test_profiles_match_monthly_simulation(self):
        for p in load_profiles():
            r=plan_preview(**p)
            free=p['income']-p['essential_spend']-p['existing_payments']
            goal=max(0,p['target']-p['already_saved'])
            for purchase,key in [(False,'months_to_goal_without_purchase'),(True,'months_to_goal_with_installments')]:
                if goal==0:
                    expected=0
                elif free<=0 or (purchase and free<6000):
                    expected=None
                else:
                    total=0
                    expected=0
                    while total<goal:
                        expected+=1
                        total+=free-(6000 if purchase and expected<=4 else 0)
                        self.assertLess(expected,100000)
                self.assertEqual(r[key],expected)

    def test_warmup_and_failures_are_separate(self):
        df=pd.DataFrame([
            dict(phase='warmup',load=10,method='Baseline',ok=True,latency_ms=10000),
            dict(phase='benchmark',load=10,method='Baseline',ok=True,latency_ms=1),
            dict(phase='benchmark',load=10,method='Baseline',ok=True,latency_ms=3),
            dict(phase='benchmark',load=10,method='Baseline',ok=False,latency_ms=100)])
        s=summarize(df,bootstrap_samples=100).iloc[0]
        self.assertEqual(s.median_ms,2)
        self.assertEqual(s.attempts,3)
        self.assertAlmostEqual(s.error_rate,1/3)
        pd.testing.assert_frame_equal(summarize(df),summarize(df))

    def test_zero_free_during_installments(self):
        r=plan_preview(income=6000,essential_spend=0,existing_payments=0,target=12000,already_saved=0)
        self.assertEqual(r['months_to_goal_with_installments'],6)

if __name__=='__main__':
    unittest.main()
