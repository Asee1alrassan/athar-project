import axios from "axios";
import type { DashboardData } from "@/types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({ baseURL: BASE_URL });

export async function getDashboardData(
  period: number = 90,
  region?: string
): Promise<DashboardData> {
  const params: Record<string, string> = { period: String(period) };
  if (region) params.region = region;
  const { data } = await api.get<DashboardData>("/dashboard-data", { params });
  return data;
}

export async function getRegions(): Promise<string[]> {
  const { data } = await api.get<{ regions: string[] }>("/regions");
  return data.regions;
}

export async function getSectors(): Promise<string[]> {
  const { data } = await api.get<{ sectors: string[] }>("/sectors");
  return data.sectors;
}

export async function triggerIngest(): Promise<void> {
  await api.post("/ingest");
}

export async function triggerProcess(): Promise<void> {
  await api.post("/process");
}

export async function calculateIndex(): Promise<void> {
  await api.post("/calculate-index");
}
