# Proposed AI Saving Coach: scope and safe architecture

**Future mobile MVP** (not implemented in Task 2):
1. Manual entry or user-controlled import of bank statements.
2. Saving-goal dashboard with target, amount saved and monthly free budget.
3. Deterministic money calculations in application code (installment totals,
   monthly commitments, possible months to goal).
4. An optional LLM explanation layer, which receives **minimal** relevant
   financial totals, not account numbers, and explains choices in simple
   language with clear uncertainty and safety instructions.
5. Goal progress widgets and short financial-literacy reminders.
6. Real bank connections only after technical, security, legal and consent
   checks; no automatic bank integration is claimed.

`src/mentor_preview.py` is a **working rule-based calculator only**. It is not
an AI model and is not used to fabricate or validate a treatment effect.
Its outputs are not financial advice. The deterministic calculation is useful:
a language model should not be trusted to invent payment math.

**Evaluation path:**
- Verify payment arithmetic and basic safety with unit tests.
- Freeze and review a future model's prompt, generation settings and version,
  or use reviewed fixed messages as treatment stimuli.
- Pilot user comprehension and equalize guidance length/reading conditions.
- Only then recruit participants for the B vs C experiment.
- Treat evidence as short-term self-reported intention/attainability, not
  measured increases in bank savings.

**Possible privacy safeguards:** data minimization, explicit consent, clear
retention policy, local preprocessing, no bank passwords, encryption for any
future user financial records, and human review for problematic recommendations.
