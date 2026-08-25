"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AssessmentShell } from "@/components/Layout";
import { createAssessment } from "@/lib/api";

export default function NewAssessmentPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    createAssessment()
      .then((data) => router.replace(`/assessment/${data.public_id}/profile`))
      .catch((err: Error) => setError(err.message));
  }, [router]);

  return (
    <AssessmentShell title="Starting Assessment" subtitle="Preparing your new governance assessment.">
      {error ? (
        <p className="text-red-600" role="alert">
          {error}
        </p>
      ) : (
        <p className="text-slate-600">Creating assessment…</p>
      )}
    </AssessmentShell>
  );
}
