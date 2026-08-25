import type { Recommendation } from "@/types/assessment";
import { PRIORITY_LABELS } from "@/types/assessment";

export function getPriorityStyles(priority: string): { bg: string; text: string; border: string } {
  const map: Record<string, { bg: string; text: string; border: string }> = {
    critical: { bg: "bg-red-100", text: "text-red-950", border: "border-red-300" },
    high: { bg: "bg-orange-50", text: "text-orange-900", border: "border-orange-200" },
    medium: { bg: "bg-amber-50", text: "text-amber-900", border: "border-amber-200" },
    low: { bg: "bg-slate-50", text: "text-slate-700", border: "border-slate-200" },
  };
  return map[priority] ?? map.medium;
}

interface RecommendationsListProps {
  recommendations: Recommendation[];
  title?: string;
  compact?: boolean;
}

export function RecommendationsList({
  recommendations,
  title = "Priority Recommendations",
  compact = false,
}: RecommendationsListProps) {
  if (recommendations.length === 0) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-semibold text-[var(--color-primary)]">{title}</h2>
        <p className="mt-2 text-sm text-slate-600">
          No governance gaps requiring recommendations were identified based on your responses.
        </p>
      </section>
    );
  }

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6" aria-labelledby="rec-list-heading">
      <h2 id="rec-list-heading" className="text-lg font-semibold text-[var(--color-primary)]">
        {title}
      </h2>
      <p className="mt-1 text-sm text-slate-600">
        Rule-based recommendations generated from identified governance gaps. For planning purposes only.
      </p>

      <ul className={`mt-4 space-y-4 ${compact ? "" : ""}`}>
        {recommendations.map((rec, index) => {
          const styles = getPriorityStyles(rec.priority);
          return (
            <li
              key={`${rec.source_rule_key ?? rec.category_code}-${index}`}
              className={`rounded-lg border p-4 ${styles.bg} ${styles.border}`}
            >
              <div className="flex flex-wrap items-center gap-2">
                <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold uppercase ${styles.text} ${styles.bg} border ${styles.border}`}>
                  {PRIORITY_LABELS[rec.priority] ?? rec.priority}
                </span>
                <span className="text-xs text-slate-500">{rec.category_name}</span>
                <span className="text-xs text-slate-400">· {rec.suggested_timeframe}</span>
              </div>

              <p className="mt-2 text-sm font-medium text-slate-800">{rec.recommendation}</p>

              {!compact && (
                <dl className="mt-3 space-y-2 text-sm">
                  <div>
                    <dt className="font-medium text-slate-700">Identified gap</dt>
                    <dd className="text-slate-600">{rec.identified_gap}</dd>
                  </div>
                  <div>
                    <dt className="font-medium text-slate-700">Why it matters</dt>
                    <dd className="text-slate-600">{rec.why_it_matters}</dd>
                  </div>
                  <div>
                    <dt className="font-medium text-slate-700">Suggested action</dt>
                    <dd className="text-slate-600">{rec.suggested_action}</dd>
                  </div>
                  <div>
                    <dt className="font-medium text-slate-700">Responsible role</dt>
                    <dd className="text-slate-600">{rec.responsible_role}</dd>
                  </div>
                </dl>
              )}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
