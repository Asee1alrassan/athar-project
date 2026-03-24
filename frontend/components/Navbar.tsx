"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";

const navItems = [
  { href: "/", label: "الرئيسية" },
  { href: "/dashboard", label: "لوحة التحليل" },
  { href: "/reports", label: "التقارير" },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="bg-gradient-to-l from-sky-900 to-sky-800 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-amber-400 rounded-full flex items-center justify-center font-bold text-sky-900 text-sm">
              أ
            </div>
            <span className="text-xl font-bold tracking-wide">أثر</span>
            <span className="text-sky-300 text-sm hidden md:inline">
              المرصد الرقمي لاقتصاد المنصات
            </span>
          </div>
          <div className="flex gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={clsx(
                  "px-4 py-2 rounded-lg text-sm font-medium transition-colors",
                  pathname === item.href
                    ? "bg-sky-700 text-white"
                    : "text-sky-200 hover:bg-sky-700 hover:text-white"
                )}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}
