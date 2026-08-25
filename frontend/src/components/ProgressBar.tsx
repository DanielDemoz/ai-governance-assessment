interface ProgressBarProps {
  current: number;
  total: number;
  label?: string;
}

export function ProgressBar({ current, total, label }: ProgressBarProps) {
  const percent = total > 0 ? Math.round((current / total) * 100) : 0;

  return (
    <div aria-label={label ?? "Progress"}>
      <div className="mb-1 flex justify-between text-xs text-slate-600">
        <span>{label ?? "Progress"}</span>
        <span>
          {current} of {total} ({percent}%)
        </span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-slate-200">
        <div
          className="h-full rounded-full bg-[var(--color-primary)] transition-all"
          style={{ width: `${percent}%` }}
          role="progressbar"
          aria-valuenow={current}
          aria-valuemin={0}
          aria-valuemax={total}
        />
      </div>
    </div>
  );
}
