import Navbar from "@/components/Navbar";
import Link from "next/link";

const REGIONS = [
  { name: "الرياض", index: 78.2, growth: 7.1, rank: 1 },
  { name: "جدة", index: 71.4, growth: 5.3, rank: 2 },
  { name: "الدمام", index: 64.7, growth: 4.2, rank: 3 },
  { name: "مكة", index: 58.9, growth: 3.8, rank: 4 },
  { name: "المدينة", index: 53.1, growth: 2.9, rank: 5 },
];

const SECTORS = [
  { name: "توصيل الطعام", activity: 82, trend: "↑ نمو قوي", desc: "قطاع التوصيل يشهد ارتفاعاً مستمراً في الطلب" },
  { name: "تنقل وركوب", activity: 75, trend: "↑ نمو مستقر", desc: "منصات النقل تحافظ على نشاط مرتفع في المدن الكبرى" },
  { name: "العمل الحر الرقمي", activity: 68, trend: "↑ نمو ملحوظ", desc: "تصاعد ملحوظ في الخدمات المستقلة عبر الإنترنت" },
  { name: "خدمات المنصات", activity: 61, trend: "→ مستقر", desc: "قطاع الخدمات العامة يسجل نمواً متوازناً" },
];

export default function ReportsPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-slate-800 mb-2">
            تقرير مؤشر نشاط اقتصاد المنصات
          </h1>
          <p className="text-slate-500 text-sm">
            المملكة العربية السعودية • يناير – ديسمبر 2024 • المرصد الرقمي أثر
          </p>
        </div>

        {/* Summary KPIs */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: "المؤشر الوطني الكلي", value: "72.4 / 100", color: "text-sky-700" },
            { label: "معدل النمو السنوي", value: "+5.8%", color: "text-emerald-600" },
            { label: "الموثوقية الإجمالية", value: "77%", color: "text-amber-600" },
            { label: "المناطق المرصودة", value: "5 مناطق", color: "text-purple-600" },
          ].map((item) => (
            <div key={item.label} className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm text-center">
              <div className={`text-2xl font-bold mb-1 ${item.color}`}>{item.value}</div>
              <div className="text-xs text-slate-500">{item.label}</div>
            </div>
          ))}
        </div>

        {/* Methodology */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm mb-6">
          <h2 className="text-lg font-bold text-slate-800 mb-4">المنهجية والمصادر</h2>
          <p className="text-slate-600 text-sm leading-relaxed mb-4">
            يعتمد مؤشر نشاط اقتصاد المنصات (ATHAR GIG INDEX) على منهجية هجينة تجمع بين الإشارات
            الرقمية المتعددة. يُحسب المؤشر من 0 إلى 100 بناءً على خمسة مصادر رئيسية بأوزان محددة:
          </p>
          <div className="space-y-3">
            {[
              { source: "اتجاهات البحث (Google Trends)", weight: "25%", type: "حقيقي", color: "bg-emerald-100 text-emerald-700" },
              { source: "إشارات تطبيقات المنصات", weight: "20%", type: "مقدّر", color: "bg-amber-100 text-amber-700" },
              { source: "نشاط منصات توصيل الطعام", weight: "20%", type: "مقدّر", color: "bg-amber-100 text-amber-700" },
              { source: "إشارات منصات العمل الحر", weight: "20%", type: "مقدّر", color: "bg-amber-100 text-amber-700" },
              { source: "مجموعات البيانات المرجعية", weight: "15%", type: "اصطناعي", color: "bg-purple-100 text-purple-700" },
            ].map((item) => (
              <div key={item.source} className="flex items-center justify-between p-3 bg-slate-50 rounded-xl">
                <div className="flex items-center gap-3">
                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${item.color}`}>{item.type}</span>
                  <span className="text-sm text-slate-700">{item.source}</span>
                </div>
                <span className="text-sm font-bold text-sky-700">{item.weight}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Regional Insights */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm mb-6">
          <h2 className="text-lg font-bold text-slate-800 mb-4">رؤى إقليمية</h2>
          <div className="space-y-3">
            {REGIONS.map((region) => (
              <div key={region.name} className="flex items-center gap-3">
                <span className="w-6 h-6 bg-sky-100 text-sky-700 rounded-full flex items-center justify-center text-xs font-bold">
                  {region.rank}
                </span>
                <span className="text-sm font-medium text-slate-700 w-20">{region.name}</span>
                <div className="flex-1 bg-slate-100 rounded-full h-3">
                  <div
                    className="bg-sky-500 h-3 rounded-full transition-all"
                    style={{ width: `${region.index}%` }}
                  />
                </div>
                <span className="text-sm font-bold text-slate-800 w-12 text-left">{region.index}</span>
                <span className="text-xs text-emerald-600 w-12">+{region.growth}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Sector Insights */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm mb-6">
          <h2 className="text-lg font-bold text-slate-800 mb-4">رؤى قطاعية</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {SECTORS.map((sector) => (
              <div key={sector.name} className="p-4 bg-slate-50 rounded-xl">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-slate-800">{sector.name}</span>
                  <span className="text-xs text-emerald-600 font-medium">{sector.trend}</span>
                </div>
                <div className="bg-slate-200 rounded-full h-2 mb-2">
                  <div
                    className="bg-sky-500 h-2 rounded-full"
                    style={{ width: `${sector.activity}%` }}
                  />
                </div>
                <p className="text-xs text-slate-500">{sector.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Call to action */}
        <div className="text-center">
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 bg-sky-600 hover:bg-sky-700 text-white px-6 py-3 rounded-xl font-medium transition-colors"
          >
            ← استعرض لوحة التحليل التفاعلية
          </Link>
        </div>
      </div>
    </div>
  );
}
