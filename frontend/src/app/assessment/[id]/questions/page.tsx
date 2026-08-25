"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/Button";
import { AssessmentShell } from "@/components/Layout";
import { ProgressBar } from "@/components/ProgressBar";
import { ResponseScale } from "@/components/ResponseScale";
import { getAssessment, getCategories, updateResponses } from "@/lib/api";
import type { Category, ResponseItem } from "@/types/assessment";

export default function QuestionsPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const [categories, setCategories] = useState<Category[]>([]);
  const [responses, setResponses] = useState<Record<number, number>>({});
  const [categoryIndex, setCategoryIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const totalQuestions = useMemo(
    () => categories.reduce((sum, c) => sum + c.questions.length, 0),
    [categories],
  );

  const answeredCount = useMemo(() => Object.keys(responses).length, [responses]);

  useEffect(() => {
    Promise.all([getCategories(), getAssessment(params.id)])
      .then(([cats, assessment]) => {
        setCategories(cats);
        const existing: Record<number, number> = {};
        assessment.responses.forEach((r) => {
          existing[r.question_id] = r.response_value;
        });
        setResponses(existing);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [params.id]);

  const currentCategory = categories[categoryIndex];

  const setResponse = (questionId: number, value: number) => {
    setResponses((prev) => ({ ...prev, [questionId]: value }));
  };

  const currentCategoryComplete = currentCategory?.questions.every(
    (q) => responses[q.id] !== undefined,
  );

  const allComplete = categories.every((cat) =>
    cat.questions.every((q) => responses[q.id] !== undefined),
  );

  const saveAndContinue = async () => {
    if (!currentCategoryComplete) {
      setError("Please answer all questions in this category before continuing.");
      return;
    }
    setError(null);

    if (categoryIndex < categories.length - 1) {
      setCategoryIndex((i) => i + 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }

    if (!allComplete) {
      setError("Please complete all categories before submitting.");
      return;
    }

    setSaving(true);
    try {
      const payload: ResponseItem[] = Object.entries(responses).map(([questionId, value]) => ({
        question_id: Number(questionId),
        response_value: value,
      }));
      await updateResponses(params.id, payload);
      router.push(`/assessment/${params.id}/results`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save responses");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <AssessmentShell title="Governance Questionnaire" subtitle="Loading questions…">
        <p className="text-slate-600">Loading…</p>
      </AssessmentShell>
    );
  }

  if (!currentCategory) {
    return (
      <AssessmentShell title="Governance Questionnaire">
        <p className="text-red-600">No questions available.</p>
      </AssessmentShell>
    );
  }

  return (
    <AssessmentShell
      title="Governance Questionnaire"
      subtitle="Rate each governance control using the maturity scale. Select Not applicable where a question does not apply."
    >
      <div className="mb-8 space-y-4">
        <ProgressBar
          current={answeredCount}
          total={totalQuestions}
          label="Questions answered"
        />
        <p className="text-sm text-slate-600">
          Category {categoryIndex + 1} of {categories.length}:{" "}
          <span className="font-medium text-[var(--color-primary)]">{currentCategory.name}</span>{" "}
          ({currentCategory.weight}% weight)
        </p>
      </div>

      {error && (
        <p className="mb-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700" role="alert">
          {error}
        </p>
      )}

      <div className="space-y-8">
        {currentCategory.questions.map((question, index) => (
          <article
            key={question.id}
            className="rounded-lg border border-slate-200 bg-white p-6"
            aria-labelledby={`question-${question.id}`}
          >
            <h2 id={`question-${question.id}`} className="text-base font-medium text-slate-900">
              {index + 1}. {question.text}
            </h2>
            {question.governance_objective && (
              <p className="mt-1 text-sm text-slate-500">{question.governance_objective}</p>
            )}
            <div className="mt-4">
              <ResponseScale
                name={`q-${question.id}`}
                value={responses[question.id]}
                onChange={(value) => setResponse(question.id, value)}
              />
            </div>
          </article>
        ))}
      </div>

      <div className="mt-8 flex items-center justify-between">
        <Button
          type="button"
          variant="ghost"
          disabled={categoryIndex === 0}
          onClick={() => setCategoryIndex((i) => i - 1)}
        >
          Previous category
        </Button>
        <Button type="button" onClick={saveAndContinue} disabled={saving || !currentCategoryComplete}>
          {saving
            ? "Submitting…"
            : categoryIndex < categories.length - 1
              ? "Next category"
              : "Submit & calculate score"}
        </Button>
      </div>
    </AssessmentShell>
  );
}
