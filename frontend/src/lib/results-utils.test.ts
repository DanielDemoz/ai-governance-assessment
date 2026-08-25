import { describe, expect, it } from "vitest";
import {
  getCategoryStrengths,
  getCategoryWeaknesses,
  getPriorityCategories,
  getReadinessDescription,
  getResponseLabel,
  parseTraceCategories,
} from "@/lib/results-utils";
import type { CategoryScore } from "@/types/assessment";

describe("results-utils", () => {
  const sampleCategories: CategoryScore[] = [
    { code: "a", name: "Accountability", weight_percent: 15, score: 40, applicable_questions: 7 },
    { code: "b", name: "Human Oversight", weight_percent: 15, score: 80, applicable_questions: 7 },
    { code: "c", name: "Privacy", weight_percent: 15, score: 60, applicable_questions: 9 },
  ];

  it("returns lowest scoring categories as priorities", () => {
    const priorities = getPriorityCategories(sampleCategories, 2);
    expect(priorities).toHaveLength(2);
    expect(priorities[0].code).toBe("a");
    expect(priorities[1].code).toBe("c");
  });

  it("identifies strengths and weaknesses from trace", () => {
    const questions = [
      { code: "q1", text: "Strong control", response_value: 4, normalized_score: 1.0, excluded: false },
      { code: "q2", text: "Weak control", response_value: 0, normalized_score: 0.0, excluded: false },
      { code: "q3", text: "N/A", response_value: -1, normalized_score: null, excluded: true },
    ];
    expect(getCategoryStrengths(questions)).toHaveLength(1);
    expect(getCategoryWeaknesses(questions)).toHaveLength(1);
  });

  it("parses trace categories", () => {
    const trace = {
      categories: [{ code: "privacy", name: "Privacy", score: 70, questions: [] }],
    };
    expect(parseTraceCategories(trace)).toHaveLength(1);
  });

  it("maps response labels", () => {
    expect(getResponseLabel(4)).toBe("Fully implemented");
    expect(getResponseLabel(-1)).toBe("Not applicable");
  });

  it("provides readiness descriptions", () => {
    expect(getReadinessDescription("initial")).toContain("Fundamental governance controls");
  });
});
