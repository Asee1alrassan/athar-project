import clsx from "clsx";

interface KPICardProps {
  title: string;
  value: string | number;
  unit?: string;
  trend?: number;
  icon: string;
  color: "blue" | "green" | "amber" | "purple";
  description?: string;
}

const colorMap = {
  blue:   { bg: "bg-sky-50",    border: "border-sky-200",   text: "text-sky-700",   icon: "bg-sky-100" },
  green:  { bg: "bg-emerald-50", border: "border-emerald-200", text: "text-emerald-700", icon: "bg-emerald-100" },
  amber:  { bg: "bg-amber-50",  border: "border-amber-200", text: "text-amber-700", icon: "bg-amber-100" },
  purple: { bg: "bg-purple-50", border: "border-purple-200", text: "text-purple-700", icon: "bg-purple-100" },
};

export default function KPICard({
  title,
  value,
  unit,
  trend,
  icon,
  color,
  description,
}: KPICardProps) {
  const c = colorMap[color];
  const isPositive = trend !== undefined && trend >= 0;

  return (
    <div className={clsx("rounded-2xl border p-5 shadow-sm", c.bg, c.border)}>
      <div className="flex items-start justify-between mb-3">
        <div className={clsx("w-10 h-10 rounded-xl flex items-center justify-center text-xl", c.icon)}>
          {icon}
        </div>
        {trend !== undefined && (
          <span
            className={clsx(
              "text-xs font-semibold px-2 py-1 rounded-full",
              isPositive
                ? "bg-emerald-100 text-emerald-700"
                : "bg-red-100 text-red-700"
            )}
          >
            {isPositive ? "▲" : "▼"} {Math.abs(trend).toFixed(1)}%
          </span>
        )}
      </div>
      <div className={clsx("text-3xl font-bold mb-1", c.text)}>
        {value}
        {unit && <span className="text-base font-normal mr-1">{unit}</span>}
      </div>
      <div className="text-sm text-slate-600 font-medium">{title}</div>
      {description && (
        <div className="text-xs text-slate-400 mt-1">{description}</div>
      )}
    </div>
  );
}
