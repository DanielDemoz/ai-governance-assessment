"use client";

import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { CategoryScore } from "@/types/assessment";
import { scoreColor } from "@/lib/results-utils";

interface CategoryBarChartProps {
  categoryScores: CategoryScore[];
}

export function CategoryBarChart({ categoryScores }: CategoryBarChartProps) {
  const data = [...categoryScores]
    .sort((a, b) => b.score - a.score)
    .map((cat) => ({
      name: cat.name,
      score: cat.score,
      weight: cat.weight_percent,
    }));

  return (
    <div>
      <div
        role="img"
        aria-label={`Horizontal bar chart of category scores: ${data
          .map((d) => `${d.name} ${d.score}%`)
          .join(", ")}`}
      >
        <ResponsiveContainer width="100%" height={Math.max(280, data.length * 36)}>
          <BarChart data={data} layout="vertical" margin={{ top: 4, right: 24, left: 8, bottom: 4 }}>
            <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
            <XAxis type="number" domain={[0, 100]} tick={{ fill: "#64748b", fontSize: 12 }} />
            <YAxis
              type="category"
              dataKey="name"
              width={160}
              tick={{ fill: "#334155", fontSize: 11 }}
            />
            <Tooltip
              formatter={(value: number) => [`${value}%`, "Score"]}
              labelFormatter={(label) => String(label)}
              contentStyle={{ borderRadius: 6, border: "1px solid #e2e8f0" }}
            />
            <Bar dataKey="score" radius={[0, 4, 4, 0]} barSize={20}>
              {data.map((entry) => (
                <Cell key={entry.name} fill={scoreColor(entry.score)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <table className="sr-only">
        <caption>Category scores bar chart data</caption>
        <thead>
          <tr>
            <th scope="col">Category</th>
            <th scope="col">Score</th>
            <th scope="col">Weight</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.name}>
              <td>{row.name}</td>
              <td>{row.score}%</td>
              <td>{row.weight}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
