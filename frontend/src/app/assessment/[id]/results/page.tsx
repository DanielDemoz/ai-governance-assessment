"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ResultsDashboard } from "@/components/dashboard/ResultsDashboard";
import { AssessmentShell } from "@/components/Layout";
import {
  calculateAssessment,
  getAssessment,
  getRecommendations,
  getRiskMatrix,
  getRoadmap,
} from "@/lib/api";
import type {
  Assessment,
  AssessmentResult,
  Recommendation,
  RiskMatrixResponse,
  RoadmapPhase,
} from "@/types/assessment";

export default function ResultsPage() {
  const params = useParams<{ id: string }>();
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [roadmapPhases, setRoadmapPhases] = useState<RoadmapPhase[]>([]);
  const [riskMatrix, setRiskMatrix] = useState<RiskMatrixResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadResults = useCallback(async () => {
    const data = await getAssessment(params.id);
    setAssessment(data);
    if (data.result) {
      setResult(data.result);
    } else {
      const calculated = await calculateAssessment(params.id);
      setResult(calculated);
    }
    const [recData, roadmapData, matrixData] = await Promise.all([
      getRecommendations(params.id),
      getRoadmap(params.id),
      getRiskMatrix(params.id),
    ]);
    setRecommendations(recData.recommendations);
    setRoadmapPhases(roadmapData.phases);
    setRiskMatrix(matrixData);
  }, [params.id]);

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

  if (error || !result || !assessment) {
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
          getRiskMatrix(params.id).then(setRiskMatrix).catch(() => undefined);
        }}
      />
    </AssessmentShell>
  );
}
