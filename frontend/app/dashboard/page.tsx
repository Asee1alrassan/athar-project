"use client";
import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import KPICard from "@/components/KPICard";
import TimeSeriesChart from "@/components/TimeSeriesChart";
import SourceContributionChart from "@/components/SourceContributionChart";
import RegionalComparisonChart from "@/components/RegionalComparisonChart";
import DataQualityBadge from "@/components/DataQualityBadge";
import type { DashboardData } from "@/types";
import { getDashboardData } from "@/lib/api";
import dynamic from "next/dynamic";

const GeoMap = dynamic(() => import("@/components/GeoMap"), { ssr: false });

const PERIOD_OPTIONS = [
  { label: "آخر 30 يوم", value: 30 },
  { label: "آخر 90 يوم", value: 90 },
  { label: "آخر 6 أشهر", value: 180 },
  { label: "آخر 12 شهر", value: 365 },
];

const REGIONS = ["", "Riyadh", "Jeddah", "Dammam", "Makkah", "Madinah"];
const REGION_LABELS: Record<string, string> = {
  "": "جميع المناطق",
  Riyadh: "الرياض",
  Jeddah: "جدة",
  Dammam: "الدمام",
  Makkah: "مكة",
  Madinah: "المدينة",
};

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [period, setPeriod] = useState(90);
  const [region, setRegion] = useState("");

  useEffect(() => {
    setLoading(true);
    setError(null);
    getDashboardData(period, region || undefined)
      .then(setData)
      .catch((err) => {
        setError("تعذّر الاتصال بالخادم. تأكد من تشغيل الباكند على المنفذ 8000.");
        console.error(err);
      })
      .finally(() => setLoading(false));
  }, [period, region]);

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6">
        {/* Header + Filters */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-800">لوحة تحليل اقتصاد المنصات</h1>
            <p className="text-sm text-slate-500 mt-1">
              مؤشرات النشاط الرقمي للوظائف الحرة والمنصات في المملكة العربية السعودية
            </p>
          </div>
          <div className="flex gap-2 flex-wrap">
            {/* Period filter */}
            <div className="flex bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
              {PERIOD_OPTIONS.map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => setPeriod(opt.value)}
                  className={`px-3 py-2 text-xs font-medium transition-colors ${
                    period === opt.value
                      ? "bg-sky-600 text-white"
                      : "text-slate-600 hover:bg-slate-50"
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
            {/* Region filter */}
            <select
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              className="bg-white border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-600 shadow-sm focus:outline-none focus:border-sky-400"
            >
              {REGIONS.map((r) => (
                <option key={r} value={r}>
                  {REGION_LABELS[r]}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Demo mode badge */}
        <div className="inline-flex items-center gap-2 bg-amber-50 border border-amber-200 rounded-full px-3 py-1.5 text-xs text-amber-700 mb-6">
          <span className="w-2 h-2 bg-amber-400 rounded-full animate-pulse" />
          وضع العرض التجريبي — البيانات من الذاكرة المؤقتة
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6 text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-4 border-sky-600 border-t-transparent rounded-full animate-spin" />
            <span className="mr-3 text-slate-500">جارٍ تحميل البيانات...</span>
          </div>
        )}

        {/* Content */}
        {data && !loading && (
          <>
            {/* KPI Cards */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <KPICard
                title="مؤشر نشاط المنصات"
                value={data.kpis.gig_activity_index.toFixed(1)}
                unit="/100"
                trend={data.kpis.growth_rate}
                icon="📊"
                color="blue"
                description="المؤشر المركب الكلي"
              />
              <KPICard
                title="معدل النمو"
                value={`${data.kpis.growth_rate > 0 ? "+" : ""}${data.kpis.growth_rate.toFixed(1)}`}
                unit="%"
                icon="📈"
                color="green"
                description="مقارنة بالفترة السابقة"
              />
              <KPICard
                title="موثوقية البيانات"
                value={data.kpis.data_reliability.toFixed(1)}
                unit="%"
                icon="✅"
                color="amber"
                description="الجودة الإجمالية للمصادر"
              />
              <KPICard
                title="الإشارات النشطة"
                value={data.kpis.active_signals}
                icon="📡"
                color="purple"
                description="مصادر البيانات المتاحة"
              />
            </div>

            {/* Time Series */}
            <div className="mb-6">
              <TimeSeriesChart
                data={data.time_series}
                title="اتجاه مؤشر نشاط المنصات عبر الزمن"
              />
            </div>

            {/* Row: Source + Regional */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              <SourceContributionChart
                data={data.source_contributions}
                title="مساهمة مصادر البيانات في المؤشر"
              />
              <RegionalComparisonChart
                data={data.regional_comparison}
                title="مقارنة النشاط بين المناطق"
              />
            </div>

            {/* Row: Map + Quality */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
              <div className="lg:col-span-2">
                <GeoMap
                  data={data.map_data}
                  title="الخريطة الجغرافية لنشاط المنصات"
                />
              </div>
              <DataQualityBadge quality={data.data_quality} />
            </div>
          </>
        )}
      </div>
    </div>
  );
}
