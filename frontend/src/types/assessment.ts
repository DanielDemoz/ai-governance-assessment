export type OrganizationType =
  | "smb"
  | "education"
  | "nonprofit"
  | "government"
  | "consulting"
  | "other";

export type AITechnologyType =
  | "machine_learning"
  | "deep_learning"
  | "nlp"
  | "computer_vision"
  | "rule_based"
  | "generative_ai"
  | "hybrid"
  | "other";

export type VendorType = "in_house" | "vendor" | "both";
export type DevelopmentStatus = "concept" | "development" | "testing" | "production" | "retired";
export type DeploymentStatus = "not_deployed" | "pilot" | "limited" | "full";

export interface Question {
  id: number;
  code: string;
  text: string;
  governance_objective: string | null;
  risk_level: string;
  sort_order: number;
}

export interface Category {
  id: number;
  code: string;
  name: string;
  description: string | null;
  weight: number;
  sort_order: number;
  questions: Question[];
}

export interface OrganizationProfile {
  name: string;
  organization_type: OrganizationType;
  industry?: string;
  country?: string;
  assessment_owner?: string;
  assessment_date?: string;
}

export interface AISystemProfile {
  name: string;
  description?: string;
  primary_purpose?: string;
  technology_type?: AITechnologyType;
  vendor_type?: VendorType;
  development_status?: DevelopmentStatus;
  deployment_status?: DeploymentStatus;
  processes_personal_info?: boolean;
  processes_sensitive_info?: boolean;
  processes_public_data?: boolean;
  processes_employee_data?: boolean;
  processes_customer_data?: boolean;
  processes_student_data?: boolean;
  processes_health_info?: boolean;
  processes_financial_info?: boolean;
  makes_decisions_about_people?: boolean;
  recommends_decisions?: boolean;
  can_materially_affect_individual?: boolean;
  affects_employment?: boolean;
  affects_education?: boolean;
  affects_healthcare?: boolean;
  affects_financial_access?: boolean;
  affects_public_services?: boolean;
  affects_housing?: boolean;
  affects_insurance?: boolean;
  affects_legal_rights?: boolean;
}

export interface ResponseItem {
  question_id: number;
  response_value: number;
  notes?: string;
}

export interface CategoryScore {
  code: string;
  name: string;
  weight_percent: number;
  score: number;
  applicable_questions: number;
}

export interface AssessmentResult {
  overall_score: number;
  readiness_level: string;
  ai_system_risk: string;
  governance_gap: string;
  category_scores: CategoryScore[];
  calculation_trace: Record<string, unknown> | null;
  calculated_at: string;
}

export interface Assessment {
  public_id: string;
  status: string;
  is_demo: boolean;
  organization: OrganizationProfile | null;
  ai_system: AISystemProfile | null;
  responses: ResponseItem[];
  result: AssessmentResult | null;
  created_at: string;
  completed_at: string | null;
}

export const RESPONSE_OPTIONS = [
  { value: 4, label: "Fully implemented" },
  { value: 3, label: "Mostly implemented" },
  { value: 2, label: "Partially implemented" },
  { value: 1, label: "Planned" },
  { value: 0, label: "Not implemented" },
  { value: -1, label: "Not applicable" },
] as const;

export const READINESS_LABELS: Record<string, string> = {
  initial: "Initial",
  developing: "Developing",
  established: "Established",
  advanced: "Advanced",
  leading: "Leading",
};

export const RISK_LABELS: Record<string, string> = {
  low: "Low",
  moderate: "Moderate",
  high: "High",
  critical: "Critical",
};

export const GAP_LABELS: Record<string, string> = {
  low: "Low",
  moderate: "Moderate",
  high: "High",
  critical: "Critical",
};

export const PRIORITY_LABELS: Record<string, string> = {
  critical: "Critical",
  high: "High",
  medium: "Medium",
  low: "Low",
};

export interface Recommendation {
  id?: number;
  category_code: string;
  category_name: string;
  question_id?: number;
  priority: string;
  identified_gap: string;
  recommendation: string;
  why_it_matters: string;
  suggested_action: string;
  responsible_role: string;
  suggested_timeframe: string;
  source_rule_key?: string;
}

export interface RecommendationsResponse {
  total: number;
  recommendations: Recommendation[];
}

export interface RoadmapPhase {
  key: string;
  label: string;
  description: string;
  recommendations: Recommendation[];
}

export interface RoadmapResponse {
  phases: RoadmapPhase[];
}

export interface GovernanceRisk {
  id: number;
  risk_type: string;
  description: string | null;
  likelihood: number;
  impact: number;
  risk_score: number;
  classification: string;
}

export interface RiskMatrixCell {
  likelihood: number;
  impact: number;
  classification: string;
  count: number;
}

export interface AISystemRiskProfile {
  level: string;
  score: number;
  summary: string;
  factors: Array<{ code: string; label: string; present: boolean; weight: number }>;
}

export interface RiskMatrixResponse {
  cells: RiskMatrixCell[];
  risks: GovernanceRisk[];
  ai_system_risk_profile: AISystemRiskProfile;
}

export const RISK_TYPE_LABELS: Record<string, string> = {
  privacy_breach: "Privacy breach",
  algorithmic_bias: "Algorithmic bias",
  incorrect_decisions: "Incorrect decisions",
  lack_of_transparency: "Lack of transparency",
  automation_bias: "Automation bias",
  security_attack: "Security attack",
  data_leakage: "Data leakage",
  model_failure: "Model failure",
  vendor_dependency: "Vendor dependency",
  lack_of_human_oversight: "Lack of human oversight",
  other: "Other",
};

export const CLASSIFICATION_LABELS: Record<string, string> = {
  low: "Low",
  moderate: "Moderate",
  high: "High",
  critical: "Critical",
};
