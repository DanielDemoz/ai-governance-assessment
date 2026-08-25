import { AssessmentShell } from "@/components/Layout";

export default function MethodologyPage() {
  return (
    <AssessmentShell
      title="Assessment Methodology"
      subtitle="Transparent, rule-based scoring with full auditability."
    >
      <div className="prose prose-slate max-w-none space-y-8 rounded-lg border border-slate-200 bg-white p-8">
        <section>
          <h2 className="text-xl font-semibold text-[var(--color-primary)]">Governance dimensions</h2>
          <p className="mt-2 text-slate-600">
            The assessment evaluates nine dimensions aligned with established expectations
            for responsible AI: accountability, human oversight, data governance, fairness,
            transparency, security, risk management, lifecycle management, and accountability
            to affected people.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-[var(--color-primary)]">Scoring approach</h2>
          <p className="mt-2 text-slate-600">
            Each question is scored on a maturity scale from not implemented (0) to fully
            implemented (4). Not applicable responses are excluded from category calculations.
            Category scores are normalized to a 0 to 100 scale and combined using fixed weights
            totaling 100 percent.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-[var(--color-primary)]">Readiness levels</h2>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-slate-600">
            <li>0 to 39: Initial. Fundamental controls require attention.</li>
            <li>40 to 59: Developing. Material gaps remain.</li>
            <li>60 to 74: Established. Core practices in place.</li>
            <li>75 to 89: Advanced. Mature practices with limited gaps.</li>
            <li>90 to 100: Leading. Highly developed governance capability.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-[var(--color-primary)]">
            Readiness and system risk
          </h2>
          <p className="mt-2 text-slate-600">
            Governance readiness measures organizational preparedness. AI system risk reflects
            the potential consequence of the system based on its data use and impact profile.
            These are reported separately. A mature organization may still operate a high-risk
            AI system.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-[var(--color-primary)]">Risk matrix</h2>
          <p className="mt-2 text-slate-600">
            Identified risks are plotted on a 5 by 5 matrix using likelihood and impact ratings.
            Risk score equals likelihood multiplied by impact. Scores of 1 to 4 are low, 5 to 9
            moderate, 10 to 16 high, and 17 to 25 critical.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-[var(--color-primary)]">Limitations</h2>
          <p className="mt-2 text-slate-600">
            Results are based on self-reported responses and do not certify compliance, safety,
            or legal approval. All outputs should be validated by qualified professionals.
            Numerical scores are calculated by deterministic rules, not by a language model.
          </p>
        </section>
      </div>
    </AssessmentShell>
  );
}
