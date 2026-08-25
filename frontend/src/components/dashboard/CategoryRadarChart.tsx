"use client";

import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer } from "recharts";
import type { CategoryScore } from "@/types/assessment";
import { shortenCategoryName } from "@/lib/results-utils";

interface CategoryRadarChartProps {
  categoryScores: CategoryScore[];
}

export function CategoryRadarChart({ categoryScores }: CategoryRadarChartProps) {
  const data = categoryScores.map((cat) => ({
    category: shortenCategoryName(cat.name, 18),
    fullName: cat.name,
    score: cat.score,
  }));

  return (
    <div>
      <div
        role="img"
        aria-label={`Radar chart of category scores: ${data
          .map((d) => `${d.fullName} ${d.score}%`)
          .join(", ")}`}
      >
        <ResponsiveContainer width="100%" height={320}>
          <RadarChart data={data} cx="50%" cy="50%" outerRadius="70%">
            <PolarGrid stroke="#e2e8f0" />
            <PolarAngleAxis dataKey="category" tick={{ fill: "#475569", fontSize: 11 }} />
            <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: "#94a3b8", fontSize: 10 }} />
            <Radar
              name="Score"
              dataKey="score"
              stroke="var(--color-primary)"
              fill="var(--color-primary)"
              fillOpacity={0.25}
              strokeWidth={2}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
      <table className="sr-only">
        <caption>Category scores radar chart data</caption>
        <thead>
          <tr>
            <th scope="col">Category</th>
            <th scope="col">Score</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.fullName}>
              <td>{row.fullName}</td>
              <td>{row.score}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
