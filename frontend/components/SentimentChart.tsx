"use client";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

const COLORS = ["#ff6fb5", "#b794f6", "#ffd1dc"];

const LABELS: Record<string, string> = {
  positive: "Positive 💖",
  neutral: "Neutral 🌸",
  negative: "Negative 🥺",
};

export default function SentimentChart({
  sentiment,
}: {
  sentiment: Record<string, number>;
}) {
  const data = Object.entries(sentiment).map(([name, value]) => ({
    name: LABELS[name] || name,
    value,
  }));

  return (
    <div style={{ width: "100%", height: 340 }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            outerRadius={95}
            label={({ name, value }) => `${name}: ${value}%`}
          >
            {data.map((_, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>

          <Tooltip formatter={(value) => `${value}%`} />
          <Legend iconType="circle" />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}