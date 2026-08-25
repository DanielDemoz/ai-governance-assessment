"use client";

import { Suspense, useCallback, useEffect, useState } from "react";
import { ResultsDashboard } from "@/components/dashboard/ResultsDashboard";
import { AssessmentShell } from "@/components/Layout";
import {
  calculateAssessment,
  getAssessment,
  getRecommendations,
  getRiskMatrix,
  getRoadmap,
} from "@/lib/api";
import { useAssessmentId } from "@/lib/use-assessment-id";
import type {
  Assessment,
  AssessmentResult,
  Recommendation,
  RiskMatrixResponse,
  RoadmapPhase,
} from "@/types/assessment";

function ResultsPageContent() {
  const assessmentId = useAssessmentId();
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [roadmapPhases, setRoadmapPhases] = useState<RoadmapPhase[]>([]);
  const [riskMatrix, setRiskMatrix] = useState<RiskMatrixResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadResults = useCallback(async () => {
    if (!assessmentId) {
      throw new Error("Missing assessment ID.");
    }

    const data = await getAssessment(assessmentId);
    setAssessment(data);
    if (data.result) {
      setResult(data.result);
    } else {
      const calculated = await calculateAssessment(assessmentId);
      setResult(calculated);
    }
    const [recData, roadmapData, matrixData] = await Promise.all([
      getRecommendations(assessmentId),
      getRoadmap(assessmentId),
      getRiskMatrix(assessmentId),
    ]);
    setRecommendations(recData.recommendations);
    setRoadmapPhases(roadmapData.phases);
    setRiskMatrix(matrixData);
  }, [assessmentId]);

  useEffect(() => {
    loadResults()
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [loadResults]);

  if (loading) {
    return (
      <AssessmentShell title="Assessment Results" subtitle="Preparing your assessment report." wide>
        <p className="text-slate-600">Calculating scores and risk profile.</p>
      </AssessmentShell>
    );
  }

  if (error || !result || !assessment || !assessmentId) {
    return (
      <AssessmentShell title="Assessment Results" wide>
        <p className="text-red-600" role="alert">
          {error ?? "Unable to load results"}
        </p>
      </AssessmentShell>
    );
  }

  return (
    <AssessmentShell title="Assessment Results" wide hideHeader>
      <ResultsDashboard
        assessment={assessment}
        result={result}
        recommendations={recommendations}
        roadmapPhases={roadmapPhases}
        riskMatrix={riskMatrix}
        onRiskMatrixUpdate={() => {
          getRiskMatrix(assessmentId).then(setRiskMatrix).catch(() => undefined);
        }}
      />
    </AssessmentShell>
  );
}

export default function ResultsPage() {
  return (
    <Suspense
      fallback={
        <AssessmentShell title="Assessment Results" subtitle="Preparing your assessment report." wide>
          <p className="text-slate-600">Calculating scores and risk profile.</p>
        </AssessmentShell>
      }
    >
      <ResultsPageContent />
    </Suspense>
  );
}
