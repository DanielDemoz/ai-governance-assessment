import type {
  AISystemProfile,
  Assessment,
  AssessmentResult,
  Category,
  OrganizationProfile,
  RecommendationsResponse,
  ResponseItem,
  RoadmapResponse,
  RiskMatrixResponse,
  GovernanceRisk,
} from "@/types/assessment";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(typeof error.detail === "string" ? error.detail : "Request failed");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export function createAssessment(): Promise<{ public_id: string; status: string }> {
  return request("/assessments", { method: "POST" });
}

export function getAssessment(publicId: string): Promise<Assessment> {
  return request(`/assessments/${publicId}`);
}

export function updateProfile(
  publicId: string,
  organization: OrganizationProfile,
  ai_system: AISystemProfile,
): Promise<Assessment> {
  return request(`/assessments/${publicId}/profile`, {
    method: "PUT",
    body: JSON.stringify({ organization, ai_system }),
  });
}

export function updateResponses(publicId: string, responses: ResponseItem[]): Promise<Assessment> {
  return request(`/assessments/${publicId}/responses`, {
    method: "PUT",
    body: JSON.stringify({ responses }),
  });
}

export function calculateAssessment(publicId: string): Promise<AssessmentResult> {
  return request(`/assessments/${publicId}/calculate`, { method: "POST" });
}

export function getResults(publicId: string): Promise<AssessmentResult> {
  return request(`/assessments/${publicId}/results`);
}

export function getCategories(): Promise<Category[]> {
  return request("/categories");
}

export function getRecommendations(publicId: string): Promise<RecommendationsResponse> {
  return request(`/assessments/${publicId}/recommendations`);
}

export function getRoadmap(publicId: string): Promise<RoadmapResponse> {
  return request(`/assessments/${publicId}/roadmap`);
}

export function getRiskMatrix(publicId: string): Promise<RiskMatrixResponse> {
  return request(`/assessments/${publicId}/risk-matrix`);
}

export function addRisk(
  publicId: string,
  payload: { risk_type: string; description?: string; likelihood: number; impact: number },
): Promise<GovernanceRisk> {
  return request(`/assessments/${publicId}/risks`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function deleteRisk(publicId: string, riskId: number): Promise<void> {
  return request(`/assessments/${publicId}/risks/${riskId}`, { method: "DELETE" });
}
