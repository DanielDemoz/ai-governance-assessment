import type { CategoryScore } from "@/types/assessment";
import { RESPONSE_OPTIONS } from "@/types/assessment";

export interface TraceQuestion {
  question_id?: number;
  code: string;
  text: string;
  response_value: number;
  normalized_score: number | null;
  excluded: boolean;
}

export interface TraceCategory {
  code: string;
  name: string;
  score: number;
  weight_percent?: number;
  applicable_questions?: number;
  questions: TraceQuestion[];
}

export function parseTraceCategories(calculationTrace: Record<string, unknown> | null): TraceCategory[] {
  if (!calculationTrace?.categories) return [];
  return calculationTrace.categories as TraceCategory[];
}

export function getResponseLabel(value: number): string {
  const option = RESPONSE_OPTIONS.find((o) => o.value === value);
  return option?.label ?? String(value);
}

export function getRiskStyles(level: string): { bg: string; text: string; border: string; dot: string } {
  const map: Record<string, { bg: string; text: string; border: string; dot: string }> = {
    low: {
      bg: "bg-emerald-50",
      text: "text-emerald-800",
      border: "border-emerald-200",
      dot: "bg-emerald-600",
    },
    moderate: {
      bg: "bg-amber-50",
      text: "text-amber-900",
      border: "border-amber-200",
      dot: "bg-amber-600",
    },
    high: {
      bg: "bg-red-50",
      text: "text-red-800",
      border: "border-red-200",
      dot: "bg-red-600",
    },
    critical: {
      bg: "bg-red-100",
      text: "text-red-950",
      border: "border-red-300",
      dot: "bg-red-900",
    },
  };
  return map[level] ?? map.moderate;
}

export function getReadinessStyles(level: string): { bg: string; text: string } {
  const map: Record<string, { bg: string; text: string }> = {
    initial: { bg: "bg-red-50", text: "text-red-800" },
    developing: { bg: "bg-orange-50", text: "text-orange-800" },
    established: { bg: "bg-amber-50", text: "text-amber-900" },
    advanced: { bg: "bg-blue-50", text: "text-blue-800" },
    leading: { bg: "bg-emerald-50", text: "text-emerald-800" },
  };
  return map[level] ?? { bg: "bg-slate-50", text: "text-slate-800" };
}

export function getReadinessDescription(level: string): string {
  const map: Record<string, string> = {
    initial: "Fundamental governance controls require attention before consequential deployment.",
    developing: "Foundational practices are emerging. Material gaps remain in key areas.",
    established: "Core governance practices are in place. Targeted strengthening is recommended.",
    advanced: "Governance maturity is well developed with limited outstanding gaps.",
    leading: "Governance practices are mature. Maintain controls through ongoing review.",
  };
  return map[level] ?? "";
}

export function getPriorityCategories(categoryScores: CategoryScore[], limit = 3): CategoryScore[] {
  return [...categoryScores].sort((a, b) => a.score - b.score).slice(0, limit);
}

export function getCategoryStrengths(questions: TraceQuestion[]): TraceQuestion[] {
  return questions.filter((q) => !q.excluded && (q.normalized_score ?? 0) >= 0.75);
}

export function getCategoryWeaknesses(questions: TraceQuestion[]): TraceQuestion[] {
  return questions.filter((q) => !q.excluded && (q.normalized_score ?? 1) <= 0.25);
}

export function shortenCategoryName(name: string, maxLength = 22): string {
  if (name.length <= maxLength) return name;
  return `${name.slice(0, maxLength - 1)}…`;
}

export function scoreColor(score: number): string {
  if (score >= 75) return "var(--color-primary)";
  if (score >= 60) return "#2d5a87";
  if (score >= 40) return "#d97706";
  return "#dc2626";
}
