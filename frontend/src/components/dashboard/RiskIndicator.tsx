import { GAP_LABELS, RISK_LABELS } from "@/types/assessment";
import { getRiskStyles } from "@/lib/results-utils";

interface RiskIndicatorProps {
  aiSystemRisk: string;
  governanceGap: string;
  readinessScore: number;
}

export function RiskIndicator({ aiSystemRisk, governanceGap, readinessScore }: RiskIndicatorProps) {
  const riskStyles = getRiskStyles(aiSystemRisk);
  const gapStyles = getRiskStyles(governanceGap);

  return (
    <section
      className="rounded-lg border border-slate-200 bg-white p-6"
      aria-labelledby="risk-profile-heading"
    >
      <h2 id="risk-profile-heading" className="text-lg font-semibold text-[var(--color-primary)]">
        Risk Profile
      </h2>
      <p className="mt-1 text-sm text-slate-600">
        Governance readiness and AI system risk are separate indicators.
      </p>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <div className={`rounded-lg border p-4 ${riskStyles.bg} ${riskStyles.border}`}>
          <div className="flex items-center gap-2">
            <span
              className={`inline-block h-2.5 w-2.5 rounded-full ${riskStyles.dot}`}
              aria-hidden="true"
            />
            <p className="text-xs font-medium uppercase tracking-wide text-slate-600">AI System Risk</p>
          </div>
          <p className={`mt-2 text-2xl font-semibold ${riskStyles.text}`}>
            {RISK_LABELS[aiSystemRisk] ?? aiSystemRisk}
          </p>
          <p className="mt-1 text-sm text-slate-600">
            How potentially consequential the AI system may be based on its profile.
          </p>
        </div>

        <div className={`rounded-lg border p-4 ${gapStyles.bg} ${gapStyles.border}`}>
          <div className="flex items-center gap-2">
            <span
              className={`inline-block h-2.5 w-2.5 rounded-full ${gapStyles.dot}`}
              aria-hidden="true"
            />
            <p className="text-xs font-medium uppercase tracking-wide text-slate-600">Governance Gap</p>
          </div>
          <p className={`mt-2 text-2xl font-semibold ${gapStyles.text}`}>
            {GAP_LABELS[governanceGap] ?? governanceGap}
          </p>
          <p className="mt-1 text-sm text-slate-600">
            Urgency of governance improvements relative to readiness ({readinessScore}/100) and system
            risk.
          </p>
        </div>
      </div>

      <div className="mt-6 overflow-x-auto">
        <table className="w-full min-w-[320px] border-collapse text-sm">
          <caption className="sr-only">
            Comparison of governance readiness versus AI system risk
          </caption>
          <thead>
            <tr className="border-b border-slate-200 text-left text-slate-500">
              <th scope="col" className="pb-2 pr-4 font-medium">
                Indicator
              </th>
              <th scope="col" className="pb-2 font-medium">
                Value
              </th>
            </tr>
          </thead>
          <tbody className="text-slate-700">
            <tr className="border-b border-slate-100">
              <td className="py-2 pr-4">Governance Readiness</td>
              <td className="py-2 font-medium">{readinessScore} / 100</td>
            </tr>
            <tr className="border-b border-slate-100">
              <td className="py-2 pr-4">AI System Risk</td>
              <td className="py-2 font-medium">{RISK_LABELS[aiSystemRisk] ?? aiSystemRisk}</td>
            </tr>
            <tr>
              <td className="py-2 pr-4">Governance Gap</td>
              <td className="py-2 font-medium">{GAP_LABELS[governanceGap] ?? governanceGap}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  );
}
