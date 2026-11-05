"""Synthetic persona-based questionnaire fixture. No human or separate LLM respondents.

Standard library only. Run: python generate_dataset.py
Seeds and all behavior assumptions are explicit below. Do not tune them to obtain
significance or to pass comprehension guardrails. Outputs go beside this script.
"""
import csv
import hashlib
import json
import math
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'data' / 'synthetic'
N = 330
SEEDS = dict(profiles=3242, allocation=3243, responses=3244, row_order=3245)
VERSION = 'persona_rules_v1.0'

# Fictional situations, not population frequencies. All monetary ranges are
# design assumptions in KZT; none are estimates of the Almaty student population.
SITUATIONS = [
    ('parents_study', 'Живёт с родителями, основное время отдаёт учёбе', 'none', 'parents'),
    ('dorm_study', 'Живёт в общежитии, учится без постоянной работы', 'none', 'dorm'),
    ('rent_study', 'Снимает жильё с поддержкой семьи, сосредоточен на учёбе', 'none', 'shared_rent'),
    ('waiter', 'Работает официантом по сменам и совмещает работу с парами', 'part_time', None),
    ('barista', 'Работает бариста несколько дней в неделю', 'part_time', None),
    ('tutor', 'Подрабатывает репетиторством после занятий', 'freelance', None),
    ('design', 'Берёт небольшие заказы на дизайн', 'freelance', None),
    ('video', 'Монтирует короткие видео на заказ', 'freelance', None),
    ('courier', 'Подрабатывает курьером в свободные дни', 'part_time', None),
    ('shop', 'Работает продавцом на неполной ставке', 'part_time', None),
    ('intern', 'Проходит оплачиваемую стажировку', 'part_time', None),
    ('support', 'Работает в клиентской поддержке полный день', 'full_time', None),
    ('assistant', 'Работает помощником в офисе и учится', 'full_time', None),
    ('smm', 'Ведёт страницы небольших организаций', 'freelance', None),
    ('translation', 'Периодически переводит тексты на заказ', 'freelance', None),
    ('campus', 'Подрабатывает на университетских мероприятиях', 'part_time', None),
    ('seasonal', 'Сейчас не работает, ранее имел сезонную подработку', 'none', None),
    ('family_business', 'Помогает в семейном деле за оплату', 'part_time', 'parents'),
    ('junior_it', 'Работает начинающим специалистом в IT', 'full_time', None),
    ('photography', 'Снимает мероприятия по отдельным заказам', 'freelance', None),
    ('lab', 'Подрабатывает помощником в учебной лаборатории', 'part_time', None),
    ('callcenter', 'Выходит на вечерние смены в контактном центре', 'part_time', None),
    ('delivery_weekend', 'Работает на доставке только по выходным', 'part_time', None),
    ('exam_break', 'Сделал перерыв в подработке ради экзаменов', 'none', None),
]
GOALS = [
    ('laptop', 'ноутбук для учёбы', 180000, 650000),
    ('emergency_fund', 'резерв на непредвиденные расходы', 60000, 400000),
    ('education', 'учебный курс', 40000, 250000),
    ('tuition', 'оплату обучения', 250000, 1200000),
    ('phone', 'замену телефона', 100000, 500000),
    ('trip', 'поездку', 60000, 450000),
    ('rent_deposit', 'депозит за жильё', 100000, 400000),
    ('family_gift', 'подарок семье', 30000, 200000),
    ('health', 'плановые расходы на здоровье', 50000, 300000),
    ('equipment', 'оборудование для подработки', 80000, 500000),
    ('driving', 'обучение в автошколе', 150000, 350000),
    ('hobby', 'оборудование для хобби', 40000, 300000),
]
HOUSING_RU = dict(parents='с родителями', dorm='в общежитии', shared_rent='в съёмном жилье с другими', relatives='у родственников')
BUDGET_RU = ['не ведёт бюджет', 'иногда проверяет остаток', 'ведёт примерный бюджет', 'записывает большинство расходов', 'регулярно планирует расходы']
FREQ_RU = ['никогда', 'редко', 'иногда', 'часто', 'каждый месяц']

def money(rng, low, high, step=1000):
    return rng.randrange(math.ceil(low / step), math.floor(high / step) + 1) * step

def scale(x, lo=1, hi=7):
    return max(lo, min(hi, int(round(x))))

def write_csv(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def profiles():
    rng = random.Random(SEEDS['profiles'])
    result = []
    for i in range(N):
        situation, context, job, home = rng.choice(SITUATIONS)
        age = rng.choices(range(18, 25), [15, 20, 20, 18, 13, 8, 6])[0]
        year = rng.randint(max(1, min(4, age - 20)), min(6, age - 17))
        home = home or rng.choices(list(HOUSING_RU), [35, 25, 32, 8])[0]
        # Traits are sampled independently of income, housing and job status.
        discipline, impulse, optimism, trust, attention = [rng.randint(1, 5) for _ in range(5)]
        need = rng.randint(1, 7)
        literacy = rng.randint(0, 3)
        irregular = int(job in ('freelance', 'part_time') and rng.random() < .65)
        work = 0 if job == 'none' else money(rng, *(dict(part_time=(45000, 190000), freelance=(20000, 260000), full_time=(150000, 360000))[job]))
        scholarship = rng.choice([0, 0, 45000, 55000, 70000])
        family = money(rng, 20000, 200000) if job == 'none' else money(rng, 0, 100000)
        income = work + scholarship + family
        housing = 0 if home in ('parents', 'relatives') else money(rng, 10000, 35000) if home == 'dorm' else money(rng, 45000, 120000)
        living = money(rng, 15000, 90000)
        family_out = money(rng, 5000, 40000) if rng.random() < .18 else 0
        debt = money(rng, 5000, 40000) if rng.random() < .30 else 0
        # Include deficit cases explicitly; do not erase them by silently capping expenses.
        essential = housing + living + family_out + debt
        signed_balance = income - essential
        available = max(0, signed_balance)
        budget = scale(discipline + rng.gauss(0, 1), 1, 5)
        frequency = scale(1 + .55 * discipline + min(available / 50000, 1.5) - .25 * impulse + rng.gauss(0, .8), 1, 5)
        if available == 0:
            frequency = min(frequency, 3)  # prior six months can differ from current month
        actual_saved = 0 if available == 0 or rng.random() < .18 else int(available * min(.9, max(.02, .1 * discipline + rng.uniform(-.1, .25))) / 1000) * 1000
        spending = available - actual_saved
        goal, goal_ru, low, high = rng.choice(GOALS)
        target = money(rng, low, high, 5000)
        saved = int(target * rng.uniform(0, .75) / 1000) * 1000
        months = rng.choice([3, 4, 6, 9, 12, 18, 24])
        required = (target - saved) / months
        capacity_ratio = available / max(required, 1)
        pre_goal = scale(2.5 + 1.7 * math.log1p(capacity_ratio) + .45 * (optimism - 3) + rng.gauss(0, 1.1))
        pre_save = scale(1.5 + .38 * pre_goal + .48 * discipline - .22 * impulse + rng.gauss(0, 1.0))
        barrier = ('not_enough_income' if signed_balance <= 0 else rng.choice(['unexpected_costs', 'unstable_income' if irregular else 'competing_goals', 'impulse_spending' if impulse >= 3 else 'no_regular_plan', 'none']))
        note = f"{context}. Живёт {HOUSING_RU[home]}. Получает за месяц {income:,} ₸, обязательные платежи составляют {essential:,} ₸. Хочет накопить на {goal_ru}: {target:,} ₸ за {months} мес., уже есть {saved:,} ₸. {BUDGET_RU[budget-1].capitalize()}. Дисциплина {discipline}/5, импульсивность {impulse}/5, оптимизм {optimism}/5, доверие цифровым подсказкам {trust}/5. Потребность в наушниках {need}/7."
        result.append(dict(
            participant_id=f'SYN_{i+1:04d}', data_origin='synthetic', generation_method=VERSION,
            consent=1, consent_is_simulated=1, is_student_almaty=1, age=age, study_year=year,
            employment_status=job, housing=home, situation_code=situation,
            monthly_work_income_kzt=work, monthly_scholarship_kzt=scholarship,
            monthly_family_support_kzt=family, monthly_income_kzt=income,
            income_irregular=irregular, monthly_housing_kzt=housing,
            monthly_living_kzt=living, monthly_family_transfer_kzt=family_out,
            monthly_installment_kzt=debt, has_installment_debt=int(debt > 0),
            monthly_essential_kzt=essential, monthly_balance_kzt=signed_balance,
            monthly_available_kzt=available, monthly_shortfall_kzt=max(0, -signed_balance),
            monthly_other_spending_kzt=spending, last_month_saved_kzt=actual_saved,
            saving_frequency=frequency, budget_tracking=budget, saving_barrier=barrier,
            goal_category=goal, goal_label_ru=goal_ru, goal_target_kzt=target,
            current_goal_savings_kzt=saved, goal_horizon_months=months,
            required_monthly_saving_kzt=round(required, 2),
            headphone_need=need, digital_coach_trust=trust,
            knowledge_answer_kzt=15000 if literacy >= 1 else rng.choice([5000, 10000, 20000]),
            persona_discipline=discipline, persona_impulsivity=impulse,
            persona_optimism=optimism, persona_attention=attention,
            persona_literacy= literacy, persona_description_ru=note,
            goal_attainability_pre=pre_goal, saving_intention_pre=pre_save,
        ))
    return result

GENERIC = 'Сопоставьте стоимость покупки со своим бюджетом и целью накопления. Проверьте обязательные расходы и регулярные платежи. Подумайте, останутся ли средства на цель после покупки. Можно купить товар сейчас, отложить решение или отказаться. Выбирайте подходящий вам вариант.'

def expose_and_answer(rows):
    groups = list('A' * 110 + 'B' * 110 + 'C' * 110)
    random.Random(SEEDS['allocation']).shuffle(groups)
    rng = random.Random(SEEDS['responses'])
    for p, group in zip(rows, groups):
        available = p['monthly_available_kzt']
        required = p['required_monthly_saving_kzt']
        after = max(0, p['monthly_balance_kzt'] - 6000)
        sufficient = after >= required
        c_text = f"На вашу цель нужно примерно {required:.0f} ₸ в месяц. После обязательных расходов сейчас доступно {available} ₸. Платёж 6000 ₸ в течение четырёх месяцев оставит не более {after} ₸ в месяц. "
        if p['monthly_shortfall_kzt']:
            c_text += f"Текущий дефицит составляет {p['monthly_shortfall_kzt']} ₸. Бюджет не покрывает обязательные расходы; новый платёж увеличит дефицит."
        elif sufficient:
            c_text += 'По этим упрощённым расчётам средства на цель остаются; непредвиденные расходы здесь не учтены.'
        else:
            c_text += 'По этим упрощённым расчётам нужная сумма на цель не остаётся. Можно пересмотреть покупку, сумму цели или срок.'
        # All coefficients below are invented simulation assumptions, not fitted
        # effects. Heterogeneous C response can be positive, zero or negative.
        sensitivity = (p['digital_coach_trust'] - 1) / 4
        c_shift = (0.7 if sufficient else -0.7) * sensitivity if group == 'C' else 0
        goal_post = scale(p['goal_attainability_pre'] + c_shift + rng.gauss(0, .9))
        save_post = scale(p['saving_intention_pre'] + .25 * (goal_post - p['goal_attainability_pre']) + rng.gauss(0, .9))
        # No imposed mean A/B framing advantage. Direction depends on an
        # uncalibrated impulse-vs-discipline response; not an empirical mechanism.
        framing = .16 * (p['persona_impulsivity'] - p['persona_discipline']) if group in 'BC' else 0
        affordability = .5 if available >= 6000 else -1.0
        purchase = scale(.8 + .62 * p['headphone_need'] + .25 * p['persona_impulsivity'] - .18 * p['persona_discipline'] + affordability + framing - (.4 * sensitivity if group == 'C' and not sufficient else 0) + rng.gauss(0, 1.0))
        correct_prob = min(.97, .66 + .045 * p['persona_attention'] + .035 * p['persona_literacy'])
        cost = 24000 if rng.random() < correct_prob else rng.choice([6000, 12000, 18000, 30000])
        change = goal_post - p['goal_attainability_pre']
        reaction = 'positive' if change > 0 else 'negative' if change < 0 else 'neutral'
        reason = ('После карточки цель кажется мне немного ближе.' if change > 0 else 'После карточки цель кажется мне сложнее.' if change < 0 else 'Карточка не изменила мою оценку цели.')
        need_reason = 'Наушники мне сейчас почти не нужны.' if p['headphone_need'] <= 2 else 'Наушники могут пригодиться, но покупка не срочная.' if p['headphone_need'] <= 5 else 'Наушники мне сейчас очень нужны.'
        reasoning = f"{reason} Моя цель — {p['goal_label_ru']}; до неё осталось {p['goal_target_kzt'] - p['current_goal_savings_kzt']} ₸. {need_reason} Сейчас после обязательных расходов у меня доступно {available} ₸, поэтому вероятность покупки оцениваю на {purchase} из 7."
        confusion = rng.choice(['', '', '', 'Хочу понять, что будет при пропуске платежа.', 'Не хватает информации о гарантии наушников.', 'Нужен пример с непредвиденными расходами.']) if cost == 24000 else 'Я мог перепутать размер одного платежа и полную стоимость.'
        p.update(group=group,
            stimulus_id='total_generic_v2' if group == 'A' else 'installment_generic_v2' if group == 'B' else 'installment_personalized_rule_preview_v2',
            price_primary_text='24 000 ₸ за наушники' if group == 'A' else '4 платежа по 6 000 ₸',
            price_secondary_text='4 платежа по 6 000 ₸' if group == 'A' else '24 000 ₸ за наушники',
            guidance_method='generic_fixed_text' if group in 'AB' else 'rule_based_personalized_preview',
            guidance_text_ru=GENERIC if group in 'AB' else c_text,
            goal_attainability_post=goal_post, saving_intention_post=save_post,
            purchase_intention_post=purchase, total_cost_estimate_kzt=cost,
            confusion_comment_ru=confusion, simulated_response_reason_ru=reasoning,
            reaction_label= reaction, goal_change=change,
            saving_intention_change=save_post-p['saving_intention_pre'],
            price_comprehension_correct=int(cost == 24000))
    random.Random(SEEDS['row_order']).shuffle(rows)
    return rows

def validate(rows):
    assert len(rows) == N
    assert Counter(r['group'] for r in rows) == dict(A=110, B=110, C=110)
    assert len({r['participant_id'] for r in rows}) == N
    assert len({r['persona_description_ru'] for r in rows}) == N
    required_fields = {'participant_id','group','age','consent','goal_attainability_pre','goal_attainability_post','saving_intention_pre','saving_intention_post','purchase_intention_post','total_cost_estimate_kzt','monthly_available_kzt','employment_status','monthly_family_support_kzt','has_installment_debt'}
    assert required_fields <= rows[0].keys()
    for r in rows:
        assert 18 <= r['age'] <= 24 and r['is_student_almaty'] == 1
        assert r['monthly_income_kzt'] == r['monthly_work_income_kzt'] + r['monthly_scholarship_kzt'] + r['monthly_family_support_kzt']
        assert r['monthly_essential_kzt'] == sum(r[k] for k in ['monthly_housing_kzt','monthly_living_kzt','monthly_family_transfer_kzt','monthly_installment_kzt'])
        assert r['monthly_income_kzt'] + r['monthly_shortfall_kzt'] == r['monthly_essential_kzt'] + r['monthly_other_spending_kzt'] + r['last_month_saved_kzt']
        assert r['monthly_available_kzt'] == max(0, r['monthly_balance_kzt'])
        assert 0 <= r['current_goal_savings_kzt'] < r['goal_target_kzt']
        assert bool(r['has_installment_debt']) == bool(r['monthly_installment_kzt'])
        for k in ['goal_attainability_pre','goal_attainability_post','saving_intention_pre','saving_intention_post','purchase_intention_post','headphone_need']:
            assert 1 <= r[k] <= 7
        for k in ['saving_frequency','budget_tracking','digital_coach_trust','persona_discipline','persona_impulsivity','persona_optimism','persona_attention']:
            assert 1 <= r[k] <= 5
        assert r['data_origin'] == 'synthetic' and r['consent_is_simulated'] == 1
        assert r['goal_change'] == r['goal_attainability_post'] - r['goal_attainability_pre']
        assert r['saving_intention_change'] == r['saving_intention_post'] - r['saving_intention_pre']
        assert r['price_comprehension_correct'] == int(r['total_cost_estimate_kzt'] == 24000)
    return dict(status='passed', rows=N, columns=len(rows[0]), unique_ids=N, unique_persona_descriptions=N,
                groups=dict(Counter(r['group'] for r in rows)),
                ages=dict(sorted(Counter(r['age'] for r in rows).items())),
                circumstances=len({r['situation_code'] for r in rows}),
                deficit_cases=sum(r['monthly_shortfall_kzt'] > 0 for r in rows),
                group_reactions={g: dict(Counter(r['reaction_label'] for r in rows if r['group']==g)) for g in 'ABC'},
                price_comprehension_rate=sum(r['price_comprehension_correct'] for r in rows)/N,
                checked=['counts','unique IDs and descriptions','scale bounds','financial arithmetic','synthetic markers','required Task 2 columns','derived outcomes'],
                not_claimed=['population realism','human responses','independent LLM interviews','AI treatment efficacy'])

def main():
    rows = expose_and_answer(profiles())
    report = validate(rows)
    # Put core analysis fields first, followed by complete persona and exposure data.
    core = ['participant_id','data_origin','group','age','consent','consent_is_simulated','goal_attainability_pre','goal_attainability_post','saving_intention_pre','saving_intention_post','purchase_intention_post','total_cost_estimate_kzt','monthly_available_kzt','employment_status','monthly_family_support_kzt','has_installment_debt']
    order = core + [k for k in rows[0] if k not in core]
    rows = [{k:r[k] for k in order} for r in rows]
    target = ROOT / 'synthetic_responses_330.csv'
    write_csv(target, rows)
    with target.open(encoding='utf-8-sig', newline='') as f:
        roundtrip = list(csv.DictReader(f))
    assert len(roundtrip) == N and list(roundtrip[0]) == order
    assert all(all(str(v) == roundtrip[i][k] for k,v in row.items()) for i,row in enumerate(rows))
    report['csv_roundtrip'] = 'passed'
    report['sha256_csv'] = hashlib.sha256(target.read_bytes()).hexdigest()
    (ROOT / 'validation_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (ROOT / 'generation_manifest.json').write_text(json.dumps(dict(version=VERSION, n=N, seeds=SEEDS,
        method='LLM-designed rule-based persona simulation; Python-generated records and templated narratives',
        separate_llm_calls=0, human_participants=0, allocation='shuffle fixed multiset A*110+B*110+C*110 after generating baseline profiles',
        output_order='independent shuffle', missingness='only optional confusion_comment may be empty',
        financial_units='KZT', encoding='UTF-8 with BOM', delimiter=',',
        source_documents=['survey_instrument.md (Task 2)', 'experimental_protocol.md (Task 2)', 'methodology_passport.md v1.0', 'analysis.py (Task 2 schema)'],
        limitations=['330 is a scenario budget, not a statistically justified human sample size',
          'All profile frequencies and response coefficients are invented, not population-calibrated',
          'C uses a deterministic personalized preview; no generative AI intervention is tested',
          'All personas have a defined saving goal and simulated consent',
          'Deficit cases are explicitly represented; future real protocol must specify their treatment',
          'Synthetic responses are not benchmark timing measurements']), ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
