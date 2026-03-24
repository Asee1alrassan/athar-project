import Link from "next/link";
import Navbar from "@/components/Navbar";

export default function Home() {
  const features = [
    { icon: "📊", title: "مؤشر النشاط الرقمي", desc: "مؤشر مركب يجمع إشارات من 5 مصادر بيانات رقمية" },
    { icon: "🗺️", title: "خريطة تفاعلية", desc: "تصور جغرافي لمستوى نشاط اقتصاد المنصات في المدن السعودية" },
    { icon: "📈", title: "تحليل اتجاهات", desc: "سلاسل زمنية تعرض تطور المؤشر عبر الزمن" },
    { icon: "🔍", title: "مقارنة إقليمية", desc: "مقارنة بين الرياض وجدة والدمام ومكة والمدينة" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-950 via-sky-900 to-sky-800">
      <Navbar />

      {/* Hero */}
      <div className="max-w-5xl mx-auto px-6 py-20 text-center text-white">
        <div className="inline-flex items-center gap-2 bg-sky-800/50 border border-sky-600 rounded-full px-4 py-2 text-sm text-sky-200 mb-6">
          <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
          وضع العرض التجريبي مفعّل
        </div>

        <h1 className="text-5xl md:text-6xl font-extrabold mb-4 leading-tight">
          أثر
        </h1>
        <p className="text-xl text-sky-200 mb-3 font-medium">
          المرصد الرقمي لاقتصاد المنصات
        </p>
        <p className="text-sky-300 max-w-2xl mx-auto mb-10 text-base leading-relaxed">
          نظام متكامل لرصد وتحليل نشاط اقتصاد الوظائف الحرة والمنصات الرقمية في المملكة العربية السعودية،
          يعتمد على إشارات بيانات متعددة المصادر لحساب مؤشر نشاط موثوق ودقيق.
        </p>

        <div className="flex gap-4 justify-center flex-wrap">
          <Link
            href="/dashboard"
            className="bg-amber-400 hover:bg-amber-300 text-sky-900 font-bold px-8 py-3 rounded-xl text-base transition-colors shadow-lg"
          >
            استعرض لوحة التحليل →
          </Link>
          <Link
            href="/reports"
            className="bg-sky-700/50 hover:bg-sky-700 border border-sky-500 text-white px-8 py-3 rounded-xl text-base transition-colors"
          >
            التقارير
          </Link>
        </div>
      </div>

      {/* Features */}
      <div className="max-w-5xl mx-auto px-6 pb-20">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {features.map((f) => (
            <div
              key={f.title}
              className="bg-sky-800/40 border border-sky-700 rounded-2xl p-5 text-center text-white"
            >
              <div className="text-3xl mb-3">{f.icon}</div>
              <div className="font-semibold mb-2">{f.title}</div>
              <div className="text-sky-300 text-sm leading-relaxed">{f.desc}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Stats strip */}
      <div className="bg-sky-900/80 border-t border-sky-700 py-8">
        <div className="max-w-5xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center text-white">
            {[
              { value: "5", label: "مناطق مرصودة" },
              { value: "4", label: "قطاعات اقتصادية" },
              { value: "5", label: "مصادر بيانات" },
              { value: "42", label: "إشارة نشطة" },
            ].map((stat) => (
              <div key={stat.label}>
                <div className="text-3xl font-extrabold text-amber-400">{stat.value}</div>
                <div className="text-sky-300 text-sm mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
