"use client";

import dynamic from "next/dynamic";
import { Button } from "@/components/Button";
import { CategoryDetailPanel } from "@/components/dashboard/CategoryDetailPanel";
import { ImprovementRoadmap } from "@/components/dashboard/ImprovementRoadmap";
import { PriorityAreasList } from "@/components/dashboard/PriorityAreasList";
import { RecommendationsList } from "@/components/dashboard/RecommendationsList";
import { RiskIndicator } from "@/components/dashboard/RiskIndicator";
import { RiskMatrixPanel } from "@/components/dashboard/RiskMatrixPanel";
import { ScoreGauge } from "@/components/dashboard/ScoreGauge";
import type { Assessment, AssessmentResult, Recommendation, RiskMatrixResponse, RoadmapPhase } from "@/types/assessment";
import { READINESS_LABELS } from "@/types/assessment";
import {
  getPriorityCategories,
  getReadinessDescription,
  getReadinessStyles,
  parseTraceCategories,
} from "@/lib/results-utils";
import { useState } from "react";

const CategoryRadarChart = dynamic(
  () => import("@/components/dashboard/CategoryRadarChart").then((m) => m.CategoryRadarChart),
  { ssr: false, loading: () => <ChartPlaceholder label="Loading radar chart…" /> },
);

const CategoryBarChart = dynamic(
  () => import("@/components/dashboard/CategoryBarChart").then((m) => m.CategoryBarChart),
  { ssr: false, loading: () => <ChartPlaceholder label="Loading bar chart…" /> },
);

function ChartPlaceholder({ label }: { label: string }) {
  return (
    <div className="flex h-[280px] items-center justify-center rounded-md bg-slate-50 text-sm text-slate-500">
      {label}
    </div>
  );
}

interface ResultsDashboardProps {
  assessment: Assessment;
  result: AssessmentResult;
  recommendations: Recommendation[];
  roadmapPhases: RoadmapPhase[];
  riskMatrix: RiskMatrixResponse | null;
  onRiskMatrixUpdate: () => void;
}

export function ResultsDashboard({
  assessment,
  result,
  recommendations,
  roadmapPhases,
  riskMatrix,
  onRiskMatrixUpdate,
}: ResultsDashboardProps) {
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);
  const traceCategories = parseTraceCategories(result.calculation_trace);
  const priorityCategories = getPriorityCategories(result.category_scores, 3);
  const readinessStyles = getReadinessStyles(result.readiness_level);

  const orgName = assessment.organization?.name ?? "Organization";
  const aiSystemName = assessment.ai_system?.name ?? "AI System";

  return (
    <div className="space-y-8">
      {/* Executive summary header */}
      <header className="rounded-lg border border-slate-200 bg-white p-6 sm:p-8">
        <p className="text-sm font-medium uppercase tracking-wide text-[var(--color-accent)]">
          AI Governance Readiness Assessment
        </p>
        <h1 className="mt-2 text-2xl font-semibold text-[var(--color-primary)] sm:text-3xl">
          Assessment Results
        </h1>
        <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
          <div>
            <dt className="text-slate-500">Prepared for</dt>
            <dd className="font-medium text-slate-800">{orgName}</dd>
          </div>
          <div>
            <dt className="text-slate-500">AI System</dt>
            <dd className="font-medium text-slate-800">{aiSystemName}</dd>
          </div>
          {assessment.organization?.assessment_date && (
            <div>
              <dt className="text-slate-500">Assessment date</dt>
              <dd className="font-medium text-slate-800">{assessment.organization.assessment_date}</dd>
            </div>
          )}
        </dl>
      </header>

      {/* Primary metrics row */}
      <div className="grid gap-6 lg:grid-cols-3">
        <section
          className="flex flex-col items-center justify-center rounded-lg border border-slate-200 bg-white p-6 lg:col-span-1"
          aria-labelledby="overall-score-heading"
        >
          <h2 id="overall-score-heading" className="sr-only">
            Overall Governance Readiness
          </h2>
          <ScoreGauge score={result.overall_score} />
          <div className={`mt-4 rounded-full px-4 py-1.5 text-sm font-medium ${readinessStyles.bg} ${readinessStyles.text}`}>
            {READINESS_LABELS[result.readiness_level] ?? result.readiness_level}
          </div>
          <p className="mt-3 max-w-xs text-center text-sm text-slate-600">
            {getReadinessDescription(result.readiness_level)}
          </p>
        </section>

        <div className="space-y-6 lg:col-span-2">
          <RiskIndicator
            aiSystemRisk={result.ai_system_risk}
            governanceGap={result.governance_gap}
            readinessScore={result.overall_score}
          />
        </div>
      </div>

      {/* Charts */}
      <div className="grid gap-6 xl:grid-cols-2">
        <section
          className="rounded-lg border border-slate-200 bg-white p-6"
          aria-labelledby="radar-chart-heading"
        >
          <h2 id="radar-chart-heading" className="text-lg font-semibold text-[var(--color-primary)]">
            Governance Maturity Profile
          </h2>
          <p className="mt-1 text-sm text-slate-600">Category scores across all nine dimensions.</p>
          <div className="mt-4">
            <CategoryRadarChart categoryScores={result.category_scores} />
          </div>
        </section>

        <section
          className="rounded-lg border border-slate-200 bg-white p-6"
          aria-labelledby="bar-chart-heading"
        >
          <h2 id="bar-chart-heading" className="text-lg font-semibold text-[var(--color-primary)]">
            Category Comparison
          </h2>
          <p className="mt-1 text-sm text-slate-600">Horizontal comparison of dimension scores.</p>
          <div className="mt-4">
            <CategoryBarChart categoryScores={result.category_scores} />
          </div>
        </section>
      </div>

      {riskMatrix && (
        <RiskMatrixPanel
          publicId={assessment.public_id}
          data={riskMatrix}
          onUpdate={onRiskMatrixUpdate}
        />
      )}

      {/* Priority areas and recommendations */}
      <PriorityAreasList priorityCategories={priorityCategories} />

      <RecommendationsList
        recommendations={recommendations.slice(0, 8)}
        title="Priority Recommendations"
      />
      {recommendations.length > 8 && (
        <p className="text-sm text-slate-500">
          Showing 8 of {recommendations.length} recommendations. The improvement roadmap contains the full list.
        </p>
      )}

      <ImprovementRoadmap phases={roadmapPhases} />

      {/* Category drill-down */}
      <section aria-labelledby="category-details-heading">
        <h2 id="category-details-heading" className="text-lg font-semibold text-[var(--color-primary)]">
          Category Details
        </h2>
        <p className="mt-1 text-sm text-slate-600">
          Select a category to review responses, scoring methodology, strengths, and gaps.
        </p>
        <div className="mt-4 space-y-3">
          {result.category_scores.map((cat) => (
            <CategoryDetailPanel
              key={cat.code}
              category={cat}
              trace={traceCategories.find((t) => t.code === cat.code)}
              expanded={expandedCategory === cat.code}
              onToggle={() =>
                setExpandedCategory((prev) => (prev === cat.code ? null : cat.code))
              }
            />
          ))}
        </div>
      </section>

      {/* Disclaimer */}
      <div className="rounded-md border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
        <p>
          These scores reflect self-reported governance maturity and do not constitute a compliance
          determination, safety certification, or legal approval. Governance readiness (
          {result.overall_score}/100) and AI system risk ({result.ai_system_risk}) are independent
          measures that should be reviewed together by qualified professionals.
        </p>
      </div>

      <div className="flex flex-wrap gap-4">
        <Button href="/assessment/new">Start Another Assessment</Button>
        <Button href="/" variant="secondary">
          Return Home
        </Button>
      </div>
    </div>
  );
}
