"use client";

import { useState } from "react";
import { Button } from "@/components/Button";
import { AISystemRiskProfilePanel, getMatrixCellStyles, MatrixLegend } from "@/components/dashboard/AISystemRiskProfile";
import { addRisk, deleteRisk } from "@/lib/api";
import type { GovernanceRisk, RiskMatrixResponse } from "@/types/assessment";
import { CLASSIFICATION_LABELS, RISK_TYPE_LABELS } from "@/types/assessment";

interface RiskMatrixPanelProps {
  publicId: string;
  data: RiskMatrixResponse;
  onUpdate: () => void;
}

export function RiskMatrixPanel({ publicId, data, onUpdate }: RiskMatrixPanelProps) {
  const [adding, setAdding] = useState(false);
  const [riskType, setRiskType] = useState("privacy_breach");
  const [description, setDescription] = useState("");
  const [likelihood, setLikelihood] = useState(3);
  const [impact, setImpact] = useState(3);
  const [error, setError] = useState<string | null>(null);

  const handleAdd = async () => {
    setAdding(true);
    setError(null);
    try {
      await addRisk(publicId, { risk_type: riskType, description: description || undefined, likelihood, impact });
      setDescription("");
      onUpdate();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to add risk");
    } finally {
      setAdding(false);
    }
  };

  const handleDelete = async (riskId: number) => {
    try {
      await deleteRisk(publicId, riskId);
      onUpdate();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to remove risk");
    }
  };

  return (
    <div className="space-y-6">
      <AISystemRiskProfilePanel profile={data.ai_system_risk_profile} />

      <section className="rounded-lg border border-slate-200 bg-white p-6" aria-labelledby="risk-matrix-heading">
        <h2 id="risk-matrix-heading" className="text-lg font-semibold text-[var(--color-primary)]">
          Governance Risk Matrix
        </h2>
        <p className="mt-1 text-sm text-slate-600">
          Likelihood and impact ratings for identified AI-related risks. Score equals likelihood multiplied by impact.
        </p>

        <div className="mt-4 overflow-x-auto">
          <table className="mx-auto border-collapse text-center text-xs" role="grid" aria-label="5 by 5 risk matrix">
            <caption className="sr-only">
              Risk matrix showing likelihood on rows and impact on columns
            </caption>
            <thead>
              <tr>
                <th scope="col" className="p-2 text-slate-500">
                  Likelihood / Impact
                </th>
                {[1, 2, 3, 4, 5].map((i) => (
                  <th key={i} scope="col" className="p-2 font-medium text-slate-600">
                    {i}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[5, 4, 3, 2, 1].map((l) => (
                <tr key={l}>
                  <th scope="row" className="p-2 font-medium text-slate-600">
                    {l}
                  </th>
                  {[1, 2, 3, 4, 5].map((i) => {
                    const cell = data.cells.find((c) => c.likelihood === l && c.impact === i);
                    const classification = cell?.classification ?? "low";
                    return (
                      <td key={i} className="p-1">
                        <div
                          className={`flex h-12 w-12 flex-col items-center justify-center rounded border text-xs ${getMatrixCellStyles(classification)}`}
                          title={`Likelihood ${l}, Impact ${i}: ${CLASSIFICATION_LABELS[classification]}`}
                        >
                          <span className="font-semibold">{l * i}</span>
                          {cell && cell.count > 0 && (
                            <span className="text-[10px]">{cell.count} risk{cell.count > 1 ? "s" : ""}</span>
                          )}
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-3">
          <MatrixLegend />
        </div>

        <div className="mt-6">
          <h3 className="text-sm font-semibold text-slate-800">Identified risks</h3>
          {data.risks.length === 0 ? (
            <p className="mt-2 text-sm text-slate-600">No risks recorded.</p>
          ) : (
            <ul className="mt-3 space-y-2">
              {data.risks.map((risk: GovernanceRisk) => (
                <li key={risk.id} className="flex items-start justify-between gap-3 rounded-md border border-slate-100 bg-slate-50 p-3 text-sm">
                  <div>
                    <p className="font-medium text-slate-800">
                      {RISK_TYPE_LABELS[risk.risk_type] ?? risk.risk_type}
                    </p>
                    {risk.description && <p className="text-slate-600">{risk.description}</p>}
                    <p className="mt-1 text-xs text-slate-500">
                      L{risk.likelihood} x I{risk.impact} = {risk.risk_score} ({CLASSIFICATION_LABELS[risk.classification]})
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleDelete(risk.id)}
                    className="text-xs text-slate-500 hover:text-red-700 focus:outline-none focus-visible:underline"
                  >
                    Remove
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="mt-6 rounded-md border border-slate-200 p-4">
          <h3 className="text-sm font-semibold text-slate-800">Add a risk</h3>
          <div className="mt-3 grid gap-3 sm:grid-cols-2">
            <label className="text-sm">
              <span className="text-slate-600">Risk type</span>
              <select
                className="mt-1 w-full rounded-md border border-slate-300 px-2 py-1.5 text-sm"
                value={riskType}
                onChange={(e) => setRiskType(e.target.value)}
              >
                {Object.entries(RISK_TYPE_LABELS).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </label>
            <label className="text-sm sm:col-span-2">
              <span className="text-slate-600">Description (optional)</span>
              <input
                className="mt-1 w-full rounded-md border border-slate-300 px-2 py-1.5 text-sm"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </label>
            <label className="text-sm">
              <span className="text-slate-600">Likelihood (1-5)</span>
              <input
                type="number"
                min={1}
                max={5}
                className="mt-1 w-full rounded-md border border-slate-300 px-2 py-1.5 text-sm"
                value={likelihood}
                onChange={(e) => setLikelihood(Number(e.target.value))}
              />
            </label>
            <label className="text-sm">
              <span className="text-slate-600">Impact (1-5)</span>
              <input
                type="number"
                min={1}
                max={5}
                className="mt-1 w-full rounded-md border border-slate-300 px-2 py-1.5 text-sm"
                value={impact}
                onChange={(e) => setImpact(Number(e.target.value))}
              />
            </label>
          </div>
          {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
          <div className="mt-3">
            <Button type="button" onClick={handleAdd} disabled={adding}>
              {adding ? "Adding..." : "Add risk"}
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
