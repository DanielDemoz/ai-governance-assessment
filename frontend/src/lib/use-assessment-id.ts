"use client";

import { useSearchParams } from "next/navigation";

export function useAssessmentId(): string | null {
  return useSearchParams().get("id");
}
