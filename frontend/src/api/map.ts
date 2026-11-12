import { fetchJson } from "./client";

export type MapAvailabilityByType = {
  vehicle_type_id: string;
  vehicle_type_name: string;
  available_count: number;
};

export type MapStation = {
  id: string;
  name: string;
  capacity: number;
  latitude: string;
  longitude: string;
  availability_by_type: MapAvailabilityByType[];
};

export type MapStationsResponse = {
  stations: MapStation[];
};

export function fetchMapStations(): Promise<MapStationsResponse> {
  return fetchJson<MapStationsResponse>("/api/v1/map/stations");
}
