"use client";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell
} from "recharts";
import type { SourceContribution } from "@/types";

interface Props {
  data: SourceContribution[];
  title?: string;
}

const SOURCE_LABELS: Record<string, string> = {
  "Google Trends": "اتجاهات البحث",
  "App Ecosystem": "تطبيقات المنصات",
  "Food Delivery": "توصيل الطعام",
  "Freelance Platforms": "العمل الحر",
  "Benchmark Dataset": "بيانات مرجعية",
};

const TYPE_COLORS: Record<string, string> = {
  real: "#10b981",
  estimated: "#f59e0b",
  synthetic: "#8b5cf6",
};

export default function SourceContributionChart({ data, title }: Props) {
  const chartData = data.map((d) => ({
    ...d,
    label: SOURCE_LABELS[d.source] || d.source,
    contribution: Math.round((d.value * d.weight) / 100),
  }));

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
      {title && (
        <h3 className="text-base font-semibold text-slate-800 mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={chartData} layout="vertical" margin={{ right: 20, left: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
          <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11 }} stroke="#cbd5e1" />
          <YAxis
            type="category"
            dataKey="label"
            tick={{ fontSize: 11, fontFamily: "Tajawal" }}
            width={110}
            stroke="#cbd5e1"
          />
          <Tooltip
            formatter={(value: number) => [`${value.toFixed(1)}`, "القيمة"]}
            contentStyle={{ fontFamily: "Tajawal", direction: "rtl", fontSize: 12 }}
          />
          <Bar dataKey="value" radius={[0, 6, 6, 0]}>
            {chartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={TYPE_COLORS[entry.source_type] || "#0ea5e9"}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="flex gap-4 mt-3 justify-center flex-wrap">
        {Object.entries(TYPE_COLORS).map(([type, color]) => (
          <div key={type} className="flex items-center gap-1 text-xs text-slate-500">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
            {type === "real" ? "بيانات حقيقية" : type === "estimated" ? "مقدّرة" : "اصطناعية"}
          </div>
        ))}
      </div>
    </div>
  );
}
