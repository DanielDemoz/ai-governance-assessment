"use client";

interface ScoreGaugeProps {
  score: number;
  label?: string;
}

export function ScoreGauge({ score, label = "Governance Readiness" }: ScoreGaugeProps) {
  const clamped = Math.max(0, Math.min(100, score));
  const rotation = (clamped / 100) * 180 - 90;

  const arcColor =
    clamped >= 75
      ? "var(--color-primary)"
      : clamped >= 60
        ? "#2d5a87"
        : clamped >= 40
          ? "#d97706"
          : "#dc2626";

  return (
    <div className="flex flex-col items-center" role="img" aria-label={`${label}: ${score} out of 100`}>
      <div className="relative h-36 w-64">
        <svg viewBox="0 0 200 110" className="h-full w-full" aria-hidden="true">
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="#e2e8f0"
            strokeWidth="16"
            strokeLinecap="round"
          />
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke={arcColor}
            strokeWidth="16"
            strokeLinecap="round"
            strokeDasharray={`${(clamped / 100) * 251.2} 251.2`}
          />
          <g transform={`rotate(${rotation} 100 100)`}>
            <line x1="100" y1="100" x2="100" y2="35" stroke="#334155" strokeWidth="3" strokeLinecap="round" />
            <circle cx="100" cy="100" r="6" fill="#334155" />
          </g>
        </svg>
        <div className="absolute inset-x-0 bottom-0 text-center">
          <p className="text-4xl font-semibold tabular-nums text-[var(--color-primary)]">{score}</p>
          <p className="text-sm text-slate-500">/ 100</p>
        </div>
      </div>
      <p className="mt-2 text-sm font-medium text-slate-600">{label}</p>
      <p className="sr-only">
        Gauge showing {score} percent governance readiness on a scale of 0 to 100.
      </p>
    </div>
  );
}
