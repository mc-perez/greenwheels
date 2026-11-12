import { useEffect, useMemo, useState } from "react";
import { MapContainer, Marker, TileLayer } from "react-leaflet";

import { fetchMapStations, type MapStation } from "../api/map";
import { FitBounds } from "./FitBounds";

const TANDIL_CENTER: [number, number] = [-37.32167, -59.13316];
const DEFAULT_ZOOM = 13;

export function StationMap() {
  const [stations, setStations] = useState<MapStation[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    fetchMapStations()
      .then((body) => {
        if (!cancelled) {
          setStations(body.stations);
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load stations");
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const positions = useMemo(
    () =>
      stations.map(
        (station) =>
          [Number(station.latitude), Number(station.longitude)] as [number, number],
      ),
    [stations],
  );

  const selected = stations.find((station) => station.id === selectedId) ?? null;

  return (
    <div className="app-layout">
      <header className="app-header">
        <h1>GreenWheels — Tandil</h1>
        {loading && <p className="status">Loading stations…</p>}
        {error && <p className="status error">{error}</p>}
        {!loading && !error && stations.length === 0 && (
          <p className="status empty">No stations exist.</p>
        )}
      </header>
      <h2 className="sr-only">Station map</h2>
      <div className="map-row">
        <div className="map-panel">
          <MapContainer center={TANDIL_CENTER} zoom={DEFAULT_ZOOM} className="map-container">
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <FitBounds positions={positions} />
            {stations.map((station) => (
              <Marker
                key={station.id}
                position={[Number(station.latitude), Number(station.longitude)]}
                eventHandlers={{
                  click: () => setSelectedId(station.id),
                }}
              />
            ))}
          </MapContainer>
        </div>
        <aside className="detail-panel" aria-live="polite">
          {selected ? (
            <>
              <h2>{selected.name}</h2>
              <p className="capacity">Capacity: {selected.capacity}</p>
              <ul className="availability-list">
                {selected.availability_by_type.map((row) => (
                  <li key={row.vehicle_type_id}>
                    <span>{row.vehicle_type_name}</span>
                    <span>{row.available_count}</span>
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <p className="hint">Select a station marker to see availability by type.</p>
          )}
        </aside>
      </div>
    </div>
  );
}
