"use client";

import { useParams, useRouter } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";
import { Button } from "@/components/Button";
import { AssessmentShell } from "@/components/Layout";
import { checkboxClassName, FormField, inputClassName, selectClassName } from "@/components/FormField";
import { getAssessment, updateProfile } from "@/lib/api";
import type { AISystemProfile, OrganizationProfile } from "@/types/assessment";

const ORG_TYPES = [
  { value: "smb", label: "Small / Medium Business" },
  { value: "education", label: "Educational Institution" },
  { value: "nonprofit", label: "Non-profit Organization" },
  { value: "government", label: "Government / Public Sector" },
  { value: "consulting", label: "Consulting Firm" },
  { value: "other", label: "Other" },
];

const DATA_FLAGS: { key: keyof AISystemProfile; label: string }[] = [
  { key: "processes_personal_info", label: "Personal information" },
  { key: "processes_sensitive_info", label: "Sensitive information" },
  { key: "processes_public_data", label: "Public data" },
  { key: "processes_employee_data", label: "Employee data" },
  { key: "processes_customer_data", label: "Customer data" },
  { key: "processes_student_data", label: "Student data" },
  { key: "processes_health_info", label: "Health information" },
  { key: "processes_financial_info", label: "Financial information" },
];

const IMPACT_FLAGS: { key: keyof AISystemProfile; label: string }[] = [
  { key: "makes_decisions_about_people", label: "Makes decisions about people" },
  { key: "recommends_decisions", label: "Recommends decisions" },
  { key: "can_materially_affect_individual", label: "Can materially affect an individual" },
  { key: "affects_employment", label: "Employment" },
  { key: "affects_education", label: "Education" },
  { key: "affects_healthcare", label: "Healthcare" },
  { key: "affects_financial_access", label: "Financial access" },
  { key: "affects_public_services", label: "Public services" },
  { key: "affects_housing", label: "Housing" },
  { key: "affects_insurance", label: "Insurance" },
  { key: "affects_legal_rights", label: "Legal rights or opportunities" },
];

export default function ProfilePage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [organization, setOrganization] = useState<OrganizationProfile>({
    name: "",
    organization_type: "smb",
    industry: "",
    country: "",
    assessment_owner: "",
    assessment_date: new Date().toISOString().slice(0, 10),
  });

  const [aiSystem, setAiSystem] = useState<AISystemProfile>({
    name: "",
    description: "",
    primary_purpose: "",
    technology_type: "machine_learning",
    vendor_type: "in_house",
    development_status: "development",
    deployment_status: "pilot",
  });

  useEffect(() => {
    getAssessment(params.id)
      .then((assessment) => {
        if (assessment.organization) setOrganization(assessment.organization);
        if (assessment.ai_system) setAiSystem(assessment.ai_system);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [params.id]);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await updateProfile(params.id, organization, aiSystem);
      router.push(`/assessment/${params.id}/questions`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save profile");
    } finally {
      setSaving(false);
    }
  };

  const toggleFlag = (key: keyof AISystemProfile) => {
    setAiSystem((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  if (loading) {
    return (
      <AssessmentShell title="Organization & AI System Profile" subtitle="Loading…">
        <p className="text-slate-600">Loading profile…</p>
      </AssessmentShell>
    );
  }

  return (
    <AssessmentShell
      title="Organization & AI System Profile"
      subtitle="Describe the organization and AI system before answering governance questions."
    >
      <form onSubmit={handleSubmit} className="space-y-10">
        {error && (
          <p className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700" role="alert">
            {error}
          </p>
        )}

        <section className="space-y-4 rounded-lg border border-slate-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-[var(--color-primary)]">Organization</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <FormField label="Organization name" htmlFor="org-name" required>
              <input
                id="org-name"
                required
                className={inputClassName}
                value={organization.name}
                onChange={(e) => setOrganization({ ...organization, name: e.target.value })}
              />
            </FormField>
            <FormField label="Organization type" htmlFor="org-type" required>
              <select
                id="org-type"
                required
                className={selectClassName}
                value={organization.organization_type}
                onChange={(e) =>
                  setOrganization({
                    ...organization,
                    organization_type: e.target.value as OrganizationProfile["organization_type"],
                  })
                }
              >
                {ORG_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </FormField>
            <FormField label="Industry" htmlFor="org-industry">
              <input
                id="org-industry"
                className={inputClassName}
                value={organization.industry ?? ""}
                onChange={(e) => setOrganization({ ...organization, industry: e.target.value })}
              />
            </FormField>
            <FormField label="Country / jurisdiction" htmlFor="org-country">
              <input
                id="org-country"
                className={inputClassName}
                value={organization.country ?? ""}
                onChange={(e) => setOrganization({ ...organization, country: e.target.value })}
              />
            </FormField>
            <FormField label="Assessment owner" htmlFor="org-owner">
              <input
                id="org-owner"
                className={inputClassName}
                value={organization.assessment_owner ?? ""}
                onChange={(e) => setOrganization({ ...organization, assessment_owner: e.target.value })}
              />
            </FormField>
            <FormField label="Assessment date" htmlFor="org-date">
              <input
                id="org-date"
                type="date"
                className={inputClassName}
                value={organization.assessment_date ?? ""}
                onChange={(e) => setOrganization({ ...organization, assessment_date: e.target.value })}
              />
            </FormField>
          </div>
        </section>

        <section className="space-y-4 rounded-lg border border-slate-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-[var(--color-primary)]">AI System</h2>
          <div className="grid gap-4">
            <FormField label="AI system name" htmlFor="ai-name" required>
              <input
                id="ai-name"
                required
                className={inputClassName}
                value={aiSystem.name}
                onChange={(e) => setAiSystem({ ...aiSystem, name: e.target.value })}
              />
            </FormField>
            <FormField label="Description" htmlFor="ai-desc">
              <textarea
                id="ai-desc"
                rows={3}
                className={inputClassName}
                value={aiSystem.description ?? ""}
                onChange={(e) => setAiSystem({ ...aiSystem, description: e.target.value })}
              />
            </FormField>
            <FormField label="Primary purpose" htmlFor="ai-purpose">
              <textarea
                id="ai-purpose"
                rows={2}
                className={inputClassName}
                value={aiSystem.primary_purpose ?? ""}
                onChange={(e) => setAiSystem({ ...aiSystem, primary_purpose: e.target.value })}
              />
            </FormField>
          </div>
        </section>

        <section className="space-y-4 rounded-lg border border-slate-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-[var(--color-primary)]">Data Processed</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {DATA_FLAGS.map(({ key, label }) => (
              <label key={key} className="flex items-center gap-2 text-sm text-slate-700">
                <input
                  type="checkbox"
                  className={checkboxClassName}
                  checked={Boolean(aiSystem[key])}
                  onChange={() => toggleFlag(key)}
                />
                {label}
              </label>
            ))}
          </div>
        </section>

        <section className="space-y-4 rounded-lg border border-slate-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-[var(--color-primary)]">Impact Profile</h2>
          <p className="text-sm text-slate-500">
            Used to establish AI system risk classification. Reported separately from governance readiness.
          </p>
          <div className="grid gap-3 sm:grid-cols-2">
            {IMPACT_FLAGS.map(({ key, label }) => (
              <label key={key} className="flex items-center gap-2 text-sm text-slate-700">
                <input
                  type="checkbox"
                  className={checkboxClassName}
                  checked={Boolean(aiSystem[key])}
                  onChange={() => toggleFlag(key)}
                />
                {label}
              </label>
            ))}
          </div>
        </section>

        <div className="flex justify-end">
          <Button type="submit" disabled={saving}>
            {saving ? "Saving…" : "Continue to Questionnaire"}
          </Button>
        </div>
      </form>
    </AssessmentShell>
  );
}
