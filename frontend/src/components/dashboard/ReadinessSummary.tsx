import { READINESS_LABELS } from "@/types/assessment";
import { getReadinessDescription, getReadinessStyles } from "@/lib/results-utils";

interface ReadinessSummaryProps {
  overallScore: number;
  readinessLevel: string;
  organizationName?: string;
  aiSystemName?: string;
  assessmentDate?: string;
}

export function ReadinessSummary({
  overallScore,
  readinessLevel,
  organizationName,
  aiSystemName,
  assessmentDate,
}: ReadinessSummaryProps) {
  const styles = getReadinessStyles(readinessLevel);
  const label = READINESS_LABELS[readinessLevel] ?? readinessLevel;

  return (
    <section
      className="rounded-lg border border-slate-200 bg-white p-6"
      aria-labelledby="readiness-summary-heading"
    >
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h2 id="readiness-summary-heading" className="text-lg font-semibold text-[var(--color-primary)]">
            Executive Summary
          </h2>
          {organizationName && (
            <p className="mt-1 text-sm text-slate-600">
              Prepared for: <span className="font-medium text-slate-800">{organizationName}</span>
            </p>
          )}
          {aiSystemName && (
            <p className="text-sm text-slate-600">
              AI system: <span className="font-medium text-slate-800">{aiSystemName}</span>
            </p>
          )}
          {assessmentDate && (
            <p className="text-sm text-slate-500">Assessment date: {assessmentDate}</p>
          )}
        </div>
        <div className={`rounded-full px-4 py-1.5 text-sm font-semibold ${styles.bg} ${styles.text}`}>
          {label}
        </div>
      </div>
      <p className="mt-4 text-sm leading-relaxed text-slate-600">
        {getReadinessDescription(readinessLevel)} Overall indicative readiness score:{" "}
        <span className="font-semibold text-[var(--color-primary)]">{overallScore} / 100</span>.
        This does not certify compliance, safety, or legal approval.
      </p>
    </section>
  );
}
