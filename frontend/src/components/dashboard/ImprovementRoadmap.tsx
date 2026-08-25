import type { RoadmapPhase, Recommendation } from "@/types/assessment";
import { PRIORITY_LABELS } from "@/types/assessment";
import { getPriorityStyles } from "@/components/dashboard/RecommendationsList";

function RoadmapItem({ rec }: { rec: Recommendation }) {
  const styles = getPriorityStyles(rec.priority);
  return (
    <li className={`rounded-md border p-3 ${styles.bg} ${styles.border}`}>
      <div className="flex flex-wrap items-center gap-2">
        <span className={`text-xs font-semibold uppercase ${styles.text}`}>
          {PRIORITY_LABELS[rec.priority] ?? rec.priority}
        </span>
        <span className="text-xs text-slate-500">{rec.category_name}</span>
      </div>
      <p className="mt-1 text-sm text-slate-800">{rec.recommendation}</p>
      <p className="mt-1 text-xs text-slate-500">Owner: {rec.responsible_role}</p>
    </li>
  );
}

interface ImprovementRoadmapProps {
  phases: RoadmapPhase[];
}

export function ImprovementRoadmap({ phases }: ImprovementRoadmapProps) {
  if (phases.length === 0) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-semibold text-[var(--color-primary)]">Improvement Roadmap</h2>
        <p className="mt-2 text-sm text-slate-600">
          No improvement actions required based on current assessment responses.
        </p>
      </section>
    );
  }

  return (
    <section aria-labelledby="roadmap-heading">
      <h2 id="roadmap-heading" className="text-lg font-semibold text-[var(--color-primary)]">
        Improvement Roadmap
      </h2>
      <p className="mt-1 text-sm text-slate-600">
        Prioritized governance actions organized by timeframe, based on assessment results.
      </p>

      <div className="mt-4 space-y-6">
        {phases.map((phase) => (
          <article key={phase.key} className="rounded-lg border border-slate-200 bg-white p-6">
            <header className="border-b border-slate-100 pb-3">
              <h3 className="text-base font-semibold text-[var(--color-primary)]">{phase.label}</h3>
              <p className="text-sm text-slate-600">{phase.description}</p>
            </header>
            <ul className="mt-4 space-y-3">
              {phase.recommendations.map((rec, index) => (
                <RoadmapItem key={`${rec.source_rule_key ?? rec.category_code}-${index}`} rec={rec} />
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
}
