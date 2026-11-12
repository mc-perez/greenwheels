import { fetchJson } from "./client";

export type Vehicle = {
  id: string;
  vehicle_type_id: string;
  station_id: string | null;
  available: boolean;
};

export function listVehicles(): Promise<Vehicle[]> {
  return fetchJson<Vehicle[]>("/api/v1/vehicles");
}

export function createVehicle(body: { vehicle_type_id: string; station_id: string }): Promise<Vehicle> {
  return fetchJson<Vehicle>("/api/v1/vehicles", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function updateVehicle(
  id: string,
  body: { vehicle_type_id?: string; station_id?: string },
): Promise<Vehicle> {
  return fetchJson<Vehicle>(`/api/v1/vehicles/${id}`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

export function deleteVehicle(id: string): Promise<void> {
  return fetchJson<void>(`/api/v1/vehicles/${id}`, { method: "DELETE" });
}
