import { fetchJson } from "./client";

export type VehicleType = {
  id: string;
  name: string;
  current_rate: string;
};

export function listVehicleTypes(): Promise<VehicleType[]> {
  return fetchJson<VehicleType[]>("/api/v1/vehicle-types");
}

export function createVehicleType(body: { name: string; current_rate: number }): Promise<VehicleType> {
  return fetchJson<VehicleType>("/api/v1/vehicle-types", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function updateVehicleType(
  id: string,
  body: { name?: string; current_rate?: number },
): Promise<VehicleType> {
  return fetchJson<VehicleType>(`/api/v1/vehicle-types/${id}`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

export function deleteVehicleType(id: string): Promise<void> {
  return fetchJson<void>(`/api/v1/vehicle-types/${id}`, { method: "DELETE" });
}
