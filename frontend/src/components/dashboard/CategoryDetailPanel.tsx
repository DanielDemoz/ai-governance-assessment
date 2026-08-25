"use client";

import type { CategoryScore } from "@/types/assessment";
import {
  getCategoryStrengths,
  getCategoryWeaknesses,
  getResponseLabel,
  scoreColor,
  type TraceCategory,
} from "@/lib/results-utils";

interface CategoryDetailPanelProps {
  category: CategoryScore;
  trace?: TraceCategory;
  expanded: boolean;
  onToggle: () => void;
}

export function CategoryDetailPanel({
  category,
  trace,
  expanded,
  onToggle,
}: CategoryDetailPanelProps) {
  const questions = trace?.questions ?? [];
  const strengths = getCategoryStrengths(questions);
  const weaknesses = getCategoryWeaknesses(questions);
  const applicableCount = questions.filter((q) => !q.excluded).length;

  return (
    <article className="rounded-lg border border-slate-200 bg-white">
      <button
        type="button"
        className="flex w-full items-center justify-between gap-4 px-5 py-4 text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[var(--color-primary)]"
        onClick={onToggle}
        aria-expanded={expanded}
        aria-controls={`category-detail-${category.code}`}
      >
        <div className="min-w-0 flex-1">
          <h3 className="font-medium text-slate-900">{category.name}</h3>
          <p className="mt-0.5 text-xs text-slate-500">
            {applicableCount} applicable questions · {category.weight_percent}% weight
          </p>
        </div>
        <div className="text-right">
          <p className="text-xl font-semibold tabular-nums" style={{ color: scoreColor(category.score) }}>
            {category.score}%
          </p>
        </div>
      </button>

      <div className="px-5 pb-4">
        <div className="h-2 overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full rounded-full transition-all"
            style={{ width: `${category.score}%`, backgroundColor: scoreColor(category.score) }}
            role="presentation"
          />
        </div>
      </div>

      {expanded && (
        <div id={`category-detail-${category.code}`} className="border-t border-slate-100 px-5 py-4">
          <section aria-labelledby={`calc-heading-${category.code}`}>
            <h4
              id={`calc-heading-${category.code}`}
              className="text-sm font-semibold text-[var(--color-primary)]"
            >
              How was this score calculated?
            </h4>
            <p className="mt-1 text-sm text-slate-600">
              Category score = (sum of question scores ÷ applicable questions) × 100. Not
              applicable responses are excluded.
            </p>

            <div className="mt-4 overflow-x-auto">
              <table className="w-full min-w-[480px] border-collapse text-sm">
                <caption className="sr-only">Question responses for {category.name}</caption>
                <thead>
                  <tr className="border-b border-slate-200 text-left text-slate-500">
                    <th scope="col" className="pb-2 pr-3 font-medium">
                      Question
                    </th>
                    <th scope="col" className="pb-2 pr-3 font-medium">
                      Response
                    </th>
                    <th scope="col" className="pb-2 font-medium">
                      Score
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {questions.map((q) => (
                    <tr key={q.code} className="border-b border-slate-50">
                      <td className="py-2 pr-3 text-slate-700">{q.text}</td>
                      <td className="py-2 pr-3 text-slate-600">
                        {q.excluded ? "Not applicable" : getResponseLabel(q.response_value)}
                      </td>
                      <td className="py-2 font-medium text-slate-800">
                        {q.excluded ? "Excluded" : `${((q.normalized_score ?? 0) * 100).toFixed(0)}%`}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          {strengths.length > 0 && (
            <section className="mt-6" aria-labelledby={`strengths-${category.code}`}>
              <h4 id={`strengths-${category.code}`} className="text-sm font-semibold text-emerald-800">
                Strengths
              </h4>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-600">
                {strengths.map((q) => (
                  <li key={q.code}>{q.text}</li>
                ))}
              </ul>
            </section>
          )}

          {weaknesses.length > 0 && (
            <section className="mt-6" aria-labelledby={`weaknesses-${category.code}`}>
              <h4 id={`weaknesses-${category.code}`} className="text-sm font-semibold text-red-800">
                Governance Gaps
              </h4>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-600">
                {weaknesses.map((q) => (
                  <li key={q.code}>{q.text}</li>
                ))}
              </ul>
              <p className="mt-2 text-xs text-slate-500">
                Review priority recommendations for suggested actions in this area.
              </p>
            </section>
          )}
        </div>
      )}
    </article>
  );
}
