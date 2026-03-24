export interface KPIData {
  gig_activity_index: number;
  growth_rate: number;
  data_reliability: number;
  active_signals: number;
}

export interface TimeSeriesPoint {
  date: string;
  Riyadh?: number;
  Jeddah?: number;
  Dammam?: number;
  Makkah?: number;
  Madinah?: number;
  [key: string]: string | number | undefined;
}

export interface SourceContribution {
  source: string;
  weight: number;
  value: number;
  source_type: "real" | "estimated" | "synthetic";
  reliability_score: number;
}

export interface RegionalComparison {
  region: string;
  index: number;
  growth: number;
}

export interface MapPoint {
  region: string;
  lat: number;
  lng: number;
  index: number;
  growth: number;
}

export interface DataQuality {
  overall_reliability: number;
  real_percentage: number;
  estimated_percentage: number;
  synthetic_percentage: number;
  active_signals: number;
  total_records: number;
}

export interface DashboardData {
  kpis: KPIData;
  time_series: TimeSeriesPoint[];
  source_contributions: SourceContribution[];
  regional_comparison: RegionalComparison[];
  map_data: MapPoint[];
  data_quality: DataQuality;
  meta: {
    period_days: number;
    region_filter: string | null;
    demo_mode: boolean;
    generated_at: string;
  };
}
