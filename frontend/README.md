# Frontend

Next.js / React / TypeScript frontend for the AI Governance Readiness Assessment.

## Phase 4 Status

Rule-based recommendation engine and improvement roadmap integrated into the results dashboard.

## Dashboard Components

| Component | Description |
|-----------|-------------|
| `ScoreGauge` | Overall readiness gauge (0–100) |
| `CategoryRadarChart` | Nine-dimension maturity radar |
| `CategoryBarChart` | Horizontal category comparison |
| `RiskIndicator` | AI system risk vs governance gap |
| `PriorityAreasList` | Lowest-scoring categories |
| `RecommendationsList` | Rule-based priority recommendations |
| `ImprovementRoadmap` | Timeframe-grouped action plan |
| `CategoryDetailPanel` | Drill-down with calculation trace |
| `ResultsDashboard` | Full dashboard composition |

All charts include screen-reader table alternatives.

## Run Locally

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).
