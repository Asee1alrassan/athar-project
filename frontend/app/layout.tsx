import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "أثر - المرصد الرقمي لاقتصاد المنصات",
  description: "نظام رصد وتحليل نشاط اقتصاد المنصات الرقمية في المملكة العربية السعودية",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ar" dir="rtl">
      <body className="min-h-screen bg-slate-50 font-arabic">
        {children}
      </body>
    </html>
  );
}
