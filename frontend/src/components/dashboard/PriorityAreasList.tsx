import type { CategoryScore } from "@/types/assessment";
import { scoreColor } from "@/lib/results-utils";

interface PriorityAreasListProps {
  priorityCategories: CategoryScore[];
}

export function PriorityAreasList({ priorityCategories }: PriorityAreasListProps) {
  if (priorityCategories.length === 0) return null;

  return (
    <section
      className="rounded-lg border border-slate-200 bg-white p-6"
      aria-labelledby="priority-areas-heading"
    >
      <h2 id="priority-areas-heading" className="text-lg font-semibold text-[var(--color-primary)]">
        Priority Areas
      </h2>
      <p className="mt-1 text-sm text-slate-600">
        Categories with the lowest scores indicate the greatest governance gaps.
      </p>

      <ol className="mt-4 space-y-3">
        {priorityCategories.map((cat, index) => (
          <li
            key={cat.code}
            className="flex items-start gap-3 rounded-md border border-slate-100 bg-slate-50 px-4 py-3"
          >
            <span
              className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[var(--color-primary)] text-sm font-semibold text-white"
              aria-hidden="true"
            >
              {index + 1}
            </span>
            <div className="min-w-0 flex-1">
              <p className="font-medium text-slate-800">{cat.name}</p>
              <p className="text-sm text-slate-600">
                Score: <span className="font-semibold">{cat.score}%</span> · Weight:{" "}
                {cat.weight_percent}%
              </p>
              <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-200">
                <div
                  className="h-full rounded-full"
                  style={{ width: `${cat.score}%`, backgroundColor: scoreColor(cat.score) }}
                  role="presentation"
                />
              </div>
              <p className="mt-2 text-xs text-slate-500">
                Priority areas for governance review.
              </p>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
