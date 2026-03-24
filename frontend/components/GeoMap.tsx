"use client";
import { useEffect, useRef } from "react";
import type { MapPoint } from "@/types";

interface Props {
  data: MapPoint[];
  title?: string;
}

function getColor(index: number): string {
  if (index >= 75) return "#10b981";
  if (index >= 60) return "#f59e0b";
  if (index >= 45) return "#0ea5e9";
  return "#ef4444";
}

const REGION_LABELS: Record<string, string> = {
  Riyadh: "الرياض",
  Jeddah: "جدة",
  Dammam: "الدمام",
  Makkah: "مكة",
  Madinah: "المدينة",
};

export default function GeoMap({ data, title }: Props) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);

  useEffect(() => {
    if (typeof window === "undefined" || !mapRef.current || mapInstanceRef.current) return;

    import("leaflet").then((L) => {
      // Fix default icon paths
      delete (L.Icon.Default.prototype as any)._getIconUrl;
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
        iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
        shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
      });

      const map = L.map(mapRef.current!, {
        center: [23.8859, 45.0792],
        zoom: 5,
        zoomControl: true,
        scrollWheelZoom: false,
      });
      mapInstanceRef.current = map;

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "© OpenStreetMap contributors",
        opacity: 0.7,
      }).addTo(map);

      data.forEach((point) => {
        const color = getColor(point.index);
        const radius = 20 + (point.index / 100) * 30;

        const circle = L.circleMarker([point.lat, point.lng], {
          radius,
          fillColor: color,
          color: "#fff",
          weight: 2,
          opacity: 1,
          fillOpacity: 0.8,
        }).addTo(map);

        circle.bindPopup(`
          <div style="font-family: Tajawal, sans-serif; direction: rtl; text-align: right; min-width: 160px;">
            <div style="font-size: 15px; font-weight: 700; color: #0c4a6e; margin-bottom: 6px;">
              ${REGION_LABELS[point.region] || point.region}
            </div>
            <div style="font-size: 13px; color: #475569;">
              مؤشر النشاط: <strong style="color: ${color}">${point.index.toFixed(1)}</strong>
            </div>
            <div style="font-size: 12px; color: #64748b; margin-top: 3px;">
              نمو: ${point.growth.toFixed(1)}%
            </div>
          </div>
        `);
      });
    });

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, [data]);

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
      {title && (
        <h3 className="text-base font-semibold text-slate-800 mb-4">{title}</h3>
      )}
      <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
      />
      <div
        ref={mapRef}
        style={{ height: "320px", width: "100%", borderRadius: "12px" }}
      />
      <div className="flex gap-4 mt-3 justify-center flex-wrap">
        {[
          { label: "نشاط مرتفع (75+)", color: "#10b981" },
          { label: "نشاط جيد (60-74)", color: "#f59e0b" },
          { label: "نشاط متوسط (45-59)", color: "#0ea5e9" },
          { label: "نشاط منخفض (<45)", color: "#ef4444" },
        ].map((item) => (
          <div key={item.label} className="flex items-center gap-1 text-xs text-slate-500">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
            {item.label}
          </div>
        ))}
      </div>
    </div>
  );
}
