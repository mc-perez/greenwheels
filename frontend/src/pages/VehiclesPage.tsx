import { useCallback, useEffect, useMemo, useState, type FormEvent } from "react";

import { listStations, type Station } from "../api/stations";
import { listVehicleTypes, type VehicleType } from "../api/vehicleTypes";
import {
  createVehicle,
  deleteVehicle,
  listVehicles,
  updateVehicle,
  type Vehicle,
} from "../api/vehicles";
import { ErrorBanner } from "../components/ErrorBanner";
import { errorMessage } from "../utils/errors";

export function VehiclesPage() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [types, setTypes] = useState<VehicleType[]>([]);
  const [stations, setStations] = useState<Station[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [typeId, setTypeId] = useState("");
  const [stationId, setStationId] = useState("");

  const typeName = useMemo(() => new Map(types.map((t) => [t.id, t.name])), [types]);
  const stationName = useMemo(() => new Map(stations.map((s) => [s.id, s.name])), [stations]);

  const reload = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [v, t, s] = await Promise.all([listVehicles(), listVehicleTypes(), listStations()]);
      setVehicles(v);
      setTypes(t);
      setStations(s);
      setTypeId((prev) => prev || t[0]?.id || "");
      setStationId((prev) => prev || s[0]?.id || "");
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
    if (!typeId || !stationId) {
      setError("Select a type and station");
      return;
    }
    try {
      await createVehicle({ vehicle_type_id: typeId, station_id: stationId });
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  async function onPatch(vehicle: Vehicle, nextTypeId: string, nextStationId: string) {
    if (!vehicle.available) {
      setError("Cannot change a vehicle that is out on rental");
      return;
    }
    setError(null);
    try {
      await updateVehicle(vehicle.id, {
        vehicle_type_id: nextTypeId,
        station_id: nextStationId,
      });
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  async function onDelete(vehicle: Vehicle) {
    if (!window.confirm("Delete this vehicle?")) {
      return;
    }
    setError(null);
    try {
      await deleteVehicle(vehicle.id);
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  return (
    <main className="console-page">
      <h1>Fleet</h1>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />

      <form className="console-form" onSubmit={onCreate}>
        <h2>Add parked vehicle</h2>
        <label>
          Vehicle type
          <select value={typeId} onChange={(e) => setTypeId(e.target.value)} required>
            {types.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Parked at station
          <select value={stationId} onChange={(e) => setStationId(e.target.value)} required>
            {stations.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </label>
        <button type="submit" className="btn-primary" disabled={!types.length || !stations.length}>
          Add vehicle
        </button>
      </form>

      {loading ? (
        <p>Loading…</p>
      ) : (
        <table className="console-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Station</th>
              <th>Available</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {vehicles.map((vehicle) => (
              <VehicleRow
                key={`${vehicle.id}-${vehicle.vehicle_type_id}-${vehicle.station_id}-${vehicle.available}`}
                vehicle={vehicle}
                types={types}
                stations={stations}
                typeName={typeName.get(vehicle.vehicle_type_id) ?? vehicle.vehicle_type_id}
                stationLabel={
                  vehicle.station_id
                    ? (stationName.get(vehicle.station_id) ?? vehicle.station_id)
                    : "— (out)"
                }
                onPatch={onPatch}
                onDelete={onDelete}
              />
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}

function VehicleRow({
  vehicle,
  types,
  stations,
  typeName,
  stationLabel,
  onPatch,
  onDelete,
}: {
  vehicle: Vehicle;
  types: VehicleType[];
  stations: Station[];
  typeName: string;
  stationLabel: string;
  onPatch: (vehicle: Vehicle, typeId: string, stationId: string) => void;
  onDelete: (vehicle: Vehicle) => void;
}) {
  const [typeId, setTypeId] = useState(vehicle.vehicle_type_id);
  const [stationId, setStationId] = useState(vehicle.station_id ?? "");

  return (
    <tr>
      <td>
        {vehicle.available ? (
          <select value={typeId} onChange={(e) => setTypeId(e.target.value)} aria-label="Vehicle type">
            {types.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name}
              </option>
            ))}
          </select>
        ) : (
          typeName
        )}
      </td>
      <td>
        {vehicle.available ? (
          <select value={stationId} onChange={(e) => setStationId(e.target.value)} aria-label="Station">
            {stations.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        ) : (
          stationLabel
        )}
      </td>
      <td>{vehicle.available ? "Yes" : "No"}</td>
      <td className="actions-cell">
        {vehicle.available ? (
          <button
            type="button"
            className="btn-secondary"
            onClick={() => onPatch(vehicle, typeId, stationId)}
          >
            Save
          </button>
        ) : null}
        <button type="button" className="btn-danger" onClick={() => onDelete(vehicle)}>
          Delete
        </button>
      </td>
    </tr>
  );
}
