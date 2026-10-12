"""Rule-based financial-coach preview, NOT a trained AI or financial advice.

The future treatment is a controlled, evaluated AI-assisted interface. This
preview demonstrates safe deterministic arithmetic; no API keys or bank access.
"""

from __future__ import annotations

import argparse
import json
import math


def plan_preview(*, income: int, essential_spend: int, existing_payments: int,
                 target: int, already_saved: int, installments: int = 4,
                 installment_payment: int = 6000) -> dict:
    values = [income, essential_spend, existing_payments, target, already_saved,
              installments, installment_payment]
    if any(not isinstance(item, int) or item < 0 for item in values) or installments == 0:
        raise ValueError('Enter non-negative whole KZT values and positive installments.')
    free_before = income - essential_spend - existing_payments
    remaining_goal = max(0, target - already_saved)
    if remaining_goal == 0:
        months_without_purchase = 0
    elif free_before <= 0:
        months_without_purchase = None
    else:
        months_without_purchase = math.ceil(remaining_goal / free_before)

    free_during_installments = free_before - installment_payment
    total_purchase = installment_payment * installments
    if remaining_goal == 0:
        months_if_installments = 0
    elif free_before <= 0 or free_during_installments < 0:
        months_if_installments = None
    else:
        # Assume every month starts now, the first N months include installments,
        # and non-negative remaining cash can be saved each month.
        saved_by_payment_end = max(0, free_during_installments) * installments
        if remaining_goal <= saved_by_payment_end and free_during_installments > 0:
            months_if_installments = math.ceil(remaining_goal / free_during_installments)
        else:
            months_if_installments = installments + math.ceil(
                max(0, remaining_goal - saved_by_payment_end) / free_before
            )
    return {
        'tool_type': 'RULE_BASED_PREVIEW_NOT_AN_AI_MODEL',
        'currency': 'KZT',
        'monthly_free_before_purchase': free_before,
        'installment_count': installments,
        'monthly_installment': installment_payment,
        'installment_total_cost': total_purchase,
        'free_during_installments': free_during_installments,
        'remaining_goal': remaining_goal,
        'months_to_goal_without_purchase': months_without_purchase,
        'months_to_goal_with_installments': months_if_installments,
        'affordability_warning': free_during_installments < 0,
        'assumptions': 'No interest, fees, emergencies, inflation or income changes; not financial advice.',
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Demo of basic financial arithmetic')
    parser.add_argument('--income', type=int, default=90000)
    parser.add_argument('--essential', type=int, default=55000)
    parser.add_argument('--existing-payments', type=int, default=10000)
    parser.add_argument('--target', type=int, default=100000)
    parser.add_argument('--saved', type=int, default=20000)
    args = parser.parse_args()
    result = plan_preview(income=args.income, essential_spend=args.essential,
                          existing_payments=args.existing_payments, target=args.target,
                          already_saved=args.saved)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
