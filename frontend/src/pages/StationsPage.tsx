import { useCallback, useEffect, useState, type FormEvent } from "react";

import {
  createStation,
  deleteStation,
  listStations,
  updateStation,
  type Station,
} from "../api/stations";
import { ErrorBanner } from "../components/ErrorBanner";
import { errorMessage } from "../utils/errors";

export function StationsPage() {
  const [items, setItems] = useState<Station[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [capacity, setCapacity] = useState("20");
  const [lat, setLat] = useState("-37.32167");
  const [lon, setLon] = useState("-59.13316");

  const reload = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setItems(await listStations());
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  async function onCreate(e: FormEvent) {
    e.preventDefault();
    setError(null);
    const cap = Number(capacity);
    const latitude = Number(lat);
    const longitude = Number(lon);
    if (!name.trim() || Number.isNaN(cap) || Number.isNaN(latitude) || Number.isNaN(longitude)) {
      setError("Fill all fields with valid numbers");
      return;
    }
    try {
      await createStation({
        name: name.trim(),
        capacity: cap,
        latitude,
        longitude,
      });
      setName("");
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  async function onSave(
    station: Station,
    next: { name: string; capacity: string; lat: string; lon: string },
  ) {
    setError(null);
    const cap = Number(next.capacity);
    const latitude = Number(next.lat);
    const longitude = Number(next.lon);
    if (!next.name.trim() || Number.isNaN(cap) || Number.isNaN(latitude) || Number.isNaN(longitude)) {
      setError("Invalid station fields");
      return;
    }
    try {
      await updateStation(station.id, {
        name: next.name.trim(),
        capacity: cap,
        latitude,
        longitude,
      });
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  async function onDelete(station: Station) {
    if (!window.confirm(`Delete station "${station.name}"?`)) {
      return;
    }
    setError(null);
    try {
      await deleteStation(station.id);
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  return (
    <main className="console-page">
      <h1>Stations</h1>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />

      <form className="console-form" onSubmit={onCreate}>
        <h2>Add station</h2>
        <label>
          Name
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          Capacity
          <input
            type="number"
            min={1}
            value={capacity}
            onChange={(e) => setCapacity(e.target.value)}
            required
          />
        </label>
        <label>
          Latitude
          <input value={lat} onChange={(e) => setLat(e.target.value)} required />
        </label>
        <label>
          Longitude
          <input value={lon} onChange={(e) => setLon(e.target.value)} required />
        </label>
        <button type="submit" className="btn-primary">
          Add
        </button>
      </form>

      {loading ? (
        <p>Loading…</p>
      ) : (
        <table className="console-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Capacity</th>
              <th>Lat</th>
              <th>Lon</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map((station) => (
              <StationRow
                key={`${station.id}-${station.name}-${station.capacity}-${station.latitude}-${station.longitude}`}
                station={station}
                onSave={onSave}
                onDelete={onDelete}
              />
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}

function StationRow({
  station,
  onSave,
  onDelete,
}: {
  station: Station;
  onSave: (
    station: Station,
    next: { name: string; capacity: string; lat: string; lon: string },
  ) => void;
  onDelete: (station: Station) => void;
}) {
  const [name, setName] = useState(station.name);
  const [capacity, setCapacity] = useState(String(station.capacity));
  const [lat, setLat] = useState(station.latitude);
  const [lon, setLon] = useState(station.longitude);

  return (
    <tr>
      <td>
        <input value={name} onChange={(e) => setName(e.target.value)} aria-label="Station name" />
      </td>
      <td>
        <input
          type="number"
          min={1}
          value={capacity}
          onChange={(e) => setCapacity(e.target.value)}
          aria-label="Capacity"
        />
      </td>
      <td>
        <input value={lat} onChange={(e) => setLat(e.target.value)} aria-label="Latitude" />
      </td>
      <td>
        <input value={lon} onChange={(e) => setLon(e.target.value)} aria-label="Longitude" />
      </td>
      <td className="actions-cell">
        <button
          type="button"
          className="btn-secondary"
          onClick={() => onSave(station, { name, capacity, lat, lon })}
        >
          Save
        </button>
        <button type="button" className="btn-danger" onClick={() => onDelete(station)}>
          Delete
        </button>
      </td>
    </tr>
  );
}
