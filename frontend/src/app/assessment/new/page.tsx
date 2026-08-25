"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AssessmentShell } from "@/components/Layout";
import { createAssessment } from "@/lib/api";

function NewAssessmentStarter({ onCreated }: { onCreated: (publicId: string) => void }) {
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    createAssessment()
      .then((data) => onCreated(data.public_id))
      .catch((err: Error) => setError(err.message));
  }, [onCreated]);

  if (error) {
    return (
      <p className="text-red-600" role="alert">
        {error}
      </p>
    );
  }

  return <p className="text-slate-600">Creating assessment…</p>;
}

function NewAssessmentContent() {
  const router = useRouter();

  return (
    <AssessmentShell title="Starting Assessment" subtitle="Preparing your new governance assessment.">
      <NewAssessmentStarter
        onCreated={(publicId) => router.replace(`/assessment/profile?id=${publicId}`)}
      />
    </AssessmentShell>
  );
}

export default function NewAssessmentPage() {
  return (
    <Suspense
      fallback={
        <AssessmentShell title="Starting Assessment" subtitle="Preparing your new governance assessment.">
          <p className="text-slate-600">Creating assessment…</p>
        </AssessmentShell>
      }
    >
      <NewAssessmentContent />
    </Suspense>
  );
}
