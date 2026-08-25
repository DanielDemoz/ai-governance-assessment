import { Button } from "@/components/Button";
import { Disclaimer } from "@/components/Disclaimer";
import { SiteHeader } from "@/components/Layout";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-[var(--color-surface)]">
      <SiteHeader />
      <main>
        <section className="mx-auto max-w-6xl px-6 py-16 text-center">
          <p className="text-sm font-medium uppercase tracking-wide text-[var(--color-accent)]">
            AI Governance Assessment Platform
          </p>
          <h1 className="mt-4 text-4xl font-semibold tracking-tight text-[var(--color-primary)] sm:text-5xl">
            AI Governance Readiness Assessment
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-600">
            Evaluate your organization&apos;s capacity to govern AI systems responsibly.
            Measure maturity across nine governance dimensions, identify material gaps,
            assess system risk, and build a structured improvement plan.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Button href="/assessment/new">Start Assessment</Button>
            <Button href="/methodology" variant="secondary">
              View Methodology
            </Button>
          </div>
          <div className="mx-auto mt-8 max-w-2xl">
            <Disclaimer />
          </div>
        </section>

        <section className="border-t border-slate-200 bg-white py-16">
          <div className="mx-auto grid max-w-6xl gap-8 px-6 md:grid-cols-3">
            <article className="rounded-lg border border-slate-200 p-6">
              <h2 className="text-lg font-semibold text-[var(--color-primary)]">Assess</h2>
              <p className="mt-2 text-sm text-slate-600">
                Measure governance maturity across accountability, oversight, privacy,
                fairness, transparency, security, risk management, lifecycle, and
                stakeholder accountability.
              </p>
            </article>
            <article className="rounded-lg border border-slate-200 p-6">
              <h2 className="text-lg font-semibold text-[var(--color-primary)]">Identify</h2>
              <p className="mt-2 text-sm text-slate-600">
                Pinpoint governance gaps, profile AI system risk, and prioritize areas
                requiring attention prior to deployment or expanded use.
              </p>
            </article>
            <article className="rounded-lg border border-slate-200 p-6">
              <h2 className="text-lg font-semibold text-[var(--color-primary)]">Improve</h2>
              <p className="mt-2 text-sm text-slate-600">
                Receive prioritized recommendations and a timeframe-based roadmap
                derived from your assessment responses.
              </p>
            </article>
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-6 py-12">
          <p className="text-center text-sm text-slate-500">
            This platform supports governance planning. It does not provide legal advice,
            regulatory certification, or assurance of compliance or safety.
          </p>
        </section>
      </main>
    </div>
  );
}
