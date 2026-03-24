"use client";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell
} from "recharts";
import type { RegionalComparison } from "@/types";

interface Props {
  data: RegionalComparison[];
  title?: string;
}

const REGION_LABELS: Record<string, string> = {
  Riyadh: "الرياض",
  Jeddah: "جدة",
  Dammam: "الدمام",
  Makkah: "مكة",
  Madinah: "المدينة",
};

const COLORS = ["#0ea5e9", "#f59e0b", "#10b981", "#8b5cf6", "#ef4444"];

export default function RegionalComparisonChart({ data, title }: Props) {
  const chartData = data.map((d, i) => ({
    ...d,
    label: REGION_LABELS[d.region] || d.region,
    color: COLORS[i % COLORS.length],
  }));

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
      {title && (
        <h3 className="text-base font-semibold text-slate-800 mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={chartData} margin={{ top: 5, right: 10, left: -10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
          <XAxis
            dataKey="label"
            tick={{ fontSize: 12, fontFamily: "Tajawal" }}
            stroke="#cbd5e1"
          />
          <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} stroke="#cbd5e1" />
          <Tooltip
            formatter={(value: number) => [`${value.toFixed(1)}`, "مؤشر النشاط"]}
            contentStyle={{ fontFamily: "Tajawal", direction: "rtl", fontSize: 12 }}
          />
          <Bar dataKey="index" radius={[8, 8, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
