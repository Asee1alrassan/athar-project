import type { DataQuality } from "@/types";

interface Props {
  quality: DataQuality;
}

export default function DataQualityBadge({ quality }: Props) {
  const bars = [
    { label: "حقيقية", value: quality.real_percentage, color: "bg-emerald-500" },
    { label: "مقدّرة", value: quality.estimated_percentage, color: "bg-amber-500" },
    { label: "اصطناعية", value: quality.synthetic_percentage, color: "bg-purple-500" },
  ];

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
      <h3 className="text-base font-semibold text-slate-800 mb-4">جودة البيانات</h3>

      <div className="flex items-center gap-2 mb-4">
        <div className="text-2xl font-bold text-sky-700">
          {Math.round(quality.overall_reliability * 100)}%
        </div>
        <div className="text-sm text-slate-500">موثوقية إجمالية</div>
      </div>

      {/* Stacked progress bar */}
      <div className="flex h-4 rounded-full overflow-hidden mb-4 gap-0.5">
        {bars.map((bar) => (
          <div
            key={bar.label}
            className={`${bar.color} transition-all`}
            style={{ width: `${bar.value}%` }}
          />
        ))}
      </div>

      <div className="grid grid-cols-3 gap-2">
        {bars.map((bar) => (
          <div key={bar.label} className="text-center">
            <div className={`text-lg font-bold ${bar.color.replace("bg-", "text-")}`}>
              {bar.value}%
            </div>
            <div className="text-xs text-slate-500">{bar.label}</div>
          </div>
        ))}
      </div>

      <div className="mt-3 pt-3 border-t border-slate-100 flex justify-between text-xs text-slate-400">
        <span>الإشارات النشطة: {quality.active_signals}</span>
        <span>إجمالي السجلات: {quality.total_records.toLocaleString("ar")}</span>
      </div>
    </div>
  );
}
