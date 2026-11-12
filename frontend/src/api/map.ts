const apiBase =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

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

export async function fetchMapStations(): Promise<MapStationsResponse> {
  const response = await fetch(`${apiBase}/api/v1/map/stations`);
  if (!response.ok) {
    throw new Error(`Map stations request failed: ${response.status}`);
  }
  return response.json() as Promise<MapStationsResponse>;
}
