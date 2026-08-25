import Link from "next/link";
import { Disclaimer } from "@/components/Disclaimer";

export function SiteHeader() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-lg font-semibold text-[var(--color-primary)]">
          AI Governance Readiness Assessment
        </Link>
        <nav aria-label="Main navigation" className="flex gap-4 text-sm">
          <Link href="/methodology" className="text-slate-600 hover:text-[var(--color-primary)]">
            Methodology
          </Link>
        </nav>
      </div>
    </header>
  );
}

export function AssessmentShell({
  title,
  subtitle,
  children,
  wide = false,
  hideHeader = false,
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  wide?: boolean;
  hideHeader?: boolean;
}) {
  return (
    <div className="min-h-screen bg-[var(--color-surface)]">
      <SiteHeader />
      <main className={`mx-auto px-6 py-8 ${wide ? "max-w-6xl" : "max-w-4xl"}`}>
        {!hideHeader && (
          <div className="mb-8 space-y-3">
            <h1 className="text-2xl font-semibold text-[var(--color-primary)]">{title}</h1>
            {subtitle && <p className="text-slate-600">{subtitle}</p>}
            <Disclaimer />
          </div>
        )}
        {hideHeader && (
          <div className="mb-6">
            <Disclaimer />
          </div>
        )}
        {children}
      </main>
    </div>
  );
}
