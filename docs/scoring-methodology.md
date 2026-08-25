# Scoring Methodology

All scores are **deterministic and reproducible**. No LLM participates in numerical scoring.

## Question Score

```
Question Score = response_value / 4
```

Where `response_value` is 0–4. "Not applicable" (-1) is excluded from the category denominator.

## Category Score

```
Category Score = (sum of question scores / number of applicable questions) × 100
```

Example: 5 applicable questions with responses [4, 3, 2, 0, 4]:

```
Scores: 1.0 + 0.75 + 0.5 + 0.0 + 1.0 = 3.25
Category Score = (3.25 / 5) × 100 = 65.0
```

## Overall Score

```
Overall Score =
  Accountability × 15% +
  Human Oversight × 15% +
  Privacy × 15% +
  Fairness × 15% +
  Transparency × 10% +
  Security × 10% +
  Risk Management × 10% +
  Lifecycle × 5% +
  Affected People × 5%
```

Rounded to **one decimal place**.

## Readiness Levels

| Score Range | Level | Description |
|-------------|-------|-------------|
| 0–39 | Initial | Major governance gaps |
| 40–59 | Developing | Some practices, significant gaps |
| 60–74 | Established | Core practices in place, improvements needed |
| 75–89 | Advanced | Strong maturity, limited gaps |
| 90–100 | Leading | Highly mature governance approach |

## Governance Gap

Derived from the inverse of readiness relative to AI system risk:

- High AI system risk + low readiness = Critical governance gap
- High AI system risk + high readiness = Moderate governance gap
- Low AI system risk + low readiness = High governance gap

Exact formula will be implemented in Phase 2 with unit tests.

## Explainability

Every score includes a calculation trace stored in `assessment_results.calculation_trace_json`:

- Questions answered per category
- Individual response values and normalized scores
- Category aggregation formula
- Weighted overall calculation

Users can click any category to see "How was this score calculated?"

## Important Limitations

> The score does NOT mean the AI system is safe, compliant, or legally approved.
> Results are **indicative readiness** and should be reviewed by qualified professionals.
