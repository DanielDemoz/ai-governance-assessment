# Risk Methodology

The assessment uses **two separate concepts** that must not be conflated:

## 1. Governance Readiness

**Question:** How prepared is the organization to govern AI?

Measured by the weighted questionnaire score (0–100) and readiness level.

## 2. AI System Risk

**Question:** How potentially consequential is the AI system?

Derived from the AI system profile collected before the questionnaire:

### Data Factors

- Personal information processed
- Sensitive information processed
- Employee, customer, student, health, financial data

### Impact Factors

- Makes decisions about people
- Recommends decisions
- Can materially affect individuals
- Affects employment, education, healthcare, financial access, public services, housing, insurance, legal rights

### Risk Classification

| Level | Criteria (indicative) |
|-------|----------------------|
| Low | Limited personal data, no consequential decisions |
| Moderate | Some personal data or advisory role |
| High | Consequential decisions affecting individuals |
| Critical | High-impact domains (health, employment, legal rights) with automated decisions |

A highly mature organization (82/100 readiness) can still deploy a **HIGH** risk AI system. Both values are displayed independently.

## Governance Risk Matrix

Users identify specific AI risks on a **5 × 5 matrix**:

### Axes

- **Likelihood:** 1 (rare) to 5 (almost certain)
- **Impact:** 1 (negligible) to 5 (severe)

### Calculation

```
Risk Score = Likelihood × Impact
```

### Classification

| Score Range | Classification |
|-------------|----------------|
| 1–4 | Low |
| 5–9 | Moderate |
| 10–16 | High |
| 17–25 | Critical |

### Predefined Risk Types

- Privacy breach
- Algorithmic bias
- Incorrect decisions
- Lack of transparency
- Automation bias
- Security attack
- Data leakage
- Model failure
- Vendor dependency
- Lack of human oversight

## Governance Gap

Combines readiness and system risk to indicate how urgently governance improvements are needed. Implemented in Phase 5.
