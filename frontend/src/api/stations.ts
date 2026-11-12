import { fetchJson } from "./client";

export type Station = {
  id: string;
  name: string;
  capacity: number;
  latitude: string;
  longitude: string;
};

export type StationCreate = {
  name: string;
  capacity: number;
  latitude: number;
  longitude: number;
};

export type StationUpdate = {
  name?: string;
  capacity?: number;
  latitude?: number;
  longitude?: number;
};

export function listStations(): Promise<Station[]> {
  return fetchJson<Station[]>("/api/v1/stations");
}

export function createStation(body: StationCreate): Promise<Station> {
  return fetchJson<Station>("/api/v1/stations", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function updateStation(id: string, body: StationUpdate): Promise<Station> {
  return fetchJson<Station>(`/api/v1/stations/${id}`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

export function deleteStation(id: string): Promise<void> {
  return fetchJson<void>(`/api/v1/stations/${id}`, { method: "DELETE" });
}
