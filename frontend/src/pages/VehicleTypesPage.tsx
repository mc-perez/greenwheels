import { useCallback, useEffect, useState, type FormEvent } from "react";

import {
  createVehicleType,
  deleteVehicleType,
  listVehicleTypes,
  updateVehicleType,
  type VehicleType,
} from "../api/vehicleTypes";
import { ErrorBanner } from "../components/ErrorBanner";
import { errorMessage } from "../utils/errors";

export function VehicleTypesPage() {
  const [items, setItems] = useState<VehicleType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newName, setNewName] = useState("");
  const [newRate, setNewRate] = useState("");

  const reload = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setItems(await listVehicleTypes());
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
    const rate = Number(newRate);
    if (!newName.trim() || Number.isNaN(rate)) {
      setError("Name and rate are required");
      return;
    }
    try {
      await createVehicleType({ name: newName.trim(), current_rate: rate });
      setNewName("");
      setNewRate("");
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  async function onSave(item: VehicleType, name: string, rateStr: string) {
    setError(null);
    const rate = Number(rateStr);
    if (!name.trim() || Number.isNaN(rate)) {
      setError("Name and rate are required");
      return;
    }
    try {
      await updateVehicleType(item.id, { name: name.trim(), current_rate: rate });
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  async function onDelete(item: VehicleType) {
    if (!window.confirm(`Delete vehicle type "${item.name}"?`)) {
      return;
    }
    setError(null);
    try {
      await deleteVehicleType(item.id);
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  return (
    <main className="console-page">
      <h1>Vehicle types</h1>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />

      <form className="console-form" onSubmit={onCreate}>
        <h2>Add type</h2>
        <label>
          Name
          <input value={newName} onChange={(e) => setNewName(e.target.value)} required />
        </label>
        <label>
          Rate (per minute)
          <input
            type="number"
            min={0}
            step="any"
            value={newRate}
            onChange={(e) => setNewRate(e.target.value)}
            required
          />
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
              <th>Rate</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <VehicleTypeRow
                key={`${item.id}-${item.name}-${item.current_rate}`}
                item={item}
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

function VehicleTypeRow({
  item,
  onSave,
  onDelete,
}: {
  item: VehicleType;
  onSave: (item: VehicleType, name: string, rate: string) => void;
  onDelete: (item: VehicleType) => void;
}) {
  const [name, setName] = useState(item.name);
  const [rate, setRate] = useState(item.current_rate);

  return (
    <tr>
      <td>
        <input value={name} onChange={(e) => setName(e.target.value)} aria-label="Type name" />
      </td>
      <td>
        <input
          type="number"
          min={0}
          step="any"
          value={rate}
          onChange={(e) => setRate(e.target.value)}
          aria-label="Current rate"
        />
      </td>
      <td className="actions-cell">
        <button type="button" className="btn-secondary" onClick={() => onSave(item, name, rate)}>
          Save
        </button>
        <button type="button" className="btn-danger" onClick={() => onDelete(item)}>
          Delete
        </button>
      </td>
    </tr>
  );
}
