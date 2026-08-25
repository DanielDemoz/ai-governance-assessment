import { CLASSIFICATION_LABELS, RISK_LABELS } from "@/types/assessment";
import { getRiskStyles } from "@/lib/results-utils";
import type { AISystemRiskProfile } from "@/types/assessment";

interface AISystemRiskProfilePanelProps {
  profile: AISystemRiskProfile;
}

export function AISystemRiskProfilePanel({ profile }: AISystemRiskProfilePanelProps) {
  const styles = getRiskStyles(profile.level);
  const activeFactors = profile.factors.filter((f) => f.present);

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6" aria-labelledby="ai-risk-profile-heading">
      <h2 id="ai-risk-profile-heading" className="text-lg font-semibold text-[var(--color-primary)]">
        AI System Risk Profile
      </h2>
      <p className="mt-1 text-sm text-slate-600">
        Derived from the system profile. Separate from governance readiness.
      </p>

      <div className={`mt-4 rounded-lg border p-4 ${styles.bg} ${styles.border}`}>
        <p className="text-xs font-medium uppercase tracking-wide text-slate-600">Classification</p>
        <p className={`mt-1 text-2xl font-semibold ${styles.text}`}>
          {RISK_LABELS[profile.level] ?? profile.level}
        </p>
        <p className="mt-2 text-sm text-slate-700">{profile.summary}</p>
      </div>

      {activeFactors.length > 0 && (
        <div className="mt-4">
          <h3 className="text-sm font-semibold text-slate-800">Contributing factors</h3>
          <ul className="mt-2 space-y-1 text-sm text-slate-600">
            {activeFactors.map((factor) => (
              <li key={factor.code} className="flex justify-between border-b border-slate-50 py-1">
                <span>{factor.label}</span>
                <span className="font-medium text-slate-800">Weight {factor.weight}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}

export function getMatrixCellStyles(classification: string): string {
  const map: Record<string, string> = {
    low: "bg-emerald-100 border-emerald-200 text-emerald-900",
    moderate: "bg-amber-100 border-amber-200 text-amber-900",
    high: "bg-orange-100 border-orange-200 text-orange-900",
    critical: "bg-red-200 border-red-300 text-red-950",
  };
  return map[classification] ?? "bg-slate-100 border-slate-200 text-slate-800";
}

export function MatrixLegend() {
  return (
    <div className="flex flex-wrap gap-3 text-xs text-slate-600" aria-label="Risk matrix legend">
      {(["low", "moderate", "high", "critical"] as const).map((level) => (
        <span key={level} className="flex items-center gap-1.5">
          <span className={`inline-block h-3 w-3 rounded border ${getMatrixCellStyles(level)}`} aria-hidden="true" />
          {CLASSIFICATION_LABELS[level]}
        </span>
      ))}
    </div>
  );
}
