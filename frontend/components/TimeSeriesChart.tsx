"use client";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from "recharts";
import type { TimeSeriesPoint } from "@/types";

interface Props {
  data: TimeSeriesPoint[];
  title?: string;
}

const REGION_COLORS: Record<string, string> = {
  Riyadh: "#0ea5e9",
  Jeddah: "#f59e0b",
  Dammam: "#10b981",
  Makkah: "#8b5cf6",
  Madinah: "#ef4444",
};

const REGION_LABELS: Record<string, string> = {
  Riyadh: "الرياض",
  Jeddah: "جدة",
  Dammam: "الدمام",
  Makkah: "مكة",
  Madinah: "المدينة",
};

function formatDate(dateStr: string) {
  const d = new Date(dateStr);
  return `${d.getMonth() + 1}/${d.getFullYear().toString().slice(2)}`;
}

// Thin out data points for display
function sampleData(data: TimeSeriesPoint[], maxPoints = 30): TimeSeriesPoint[] {
  if (data.length <= maxPoints) return data;
  const step = Math.floor(data.length / maxPoints);
  return data.filter((_, i) => i % step === 0 || i === data.length - 1);
}

export default function TimeSeriesChart({ data, title }: Props) {
  const sampled = sampleData(data);
  const regions = Object.keys(REGION_COLORS).filter(
    (r) => sampled.length > 0 && r in sampled[0]
  );

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
      {title && (
        <h3 className="text-base font-semibold text-slate-800 mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={sampled} margin={{ top: 5, right: 10, left: -10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis
            dataKey="date"
            tickFormatter={formatDate}
            tick={{ fontSize: 11, fontFamily: "Tajawal" }}
            stroke="#cbd5e1"
          />
          <YAxis
            domain={[0, 100]}
            tick={{ fontSize: 11 }}
            stroke="#cbd5e1"
          />
          <Tooltip
            formatter={(value: number, name: string) => [
              value.toFixed(1),
              REGION_LABELS[name] || name,
            ]}
            labelFormatter={(label) => `التاريخ: ${label}`}
            contentStyle={{ fontFamily: "Tajawal", direction: "rtl", fontSize: 12 }}
          />
          <Legend
            formatter={(value) => REGION_LABELS[value] || value}
            wrapperStyle={{ fontFamily: "Tajawal", fontSize: 12 }}
          />
          {regions.map((region) => (
            <Line
              key={region}
              type="monotone"
              dataKey={region}
              stroke={REGION_COLORS[region]}
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
