import { type FormEvent, type ReactNode, useCallback, useEffect, useMemo, useState } from "react";

import { listStations, type Station } from "../api/stations";
import {
  checkoutRental,
  listRentals,
  recordRentalPayment,
  returnRental,
  type Rental,
} from "../api/rentals";
import { listVehicles, type Vehicle } from "../api/vehicles";
import { ErrorBanner } from "../components/ErrorBanner";
import { errorMessage } from "../utils/errors";

export function RentalsPage() {
  const [rentals, setRentals] = useState<Rental[]>([]);
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [stations, setStations] = useState<Station[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [checkoutOpen, setCheckoutOpen] = useState(false);
  const [returnRentalId, setReturnRentalId] = useState<string | null>(null);
  const [checkoutVehicleId, setCheckoutVehicleId] = useState("");

  const stationName = useMemo(() => new Map(stations.map((s) => [s.id, s.name])), [stations]);

  const availableVehicles = useMemo(
    () => vehicles.filter((v) => v.available && v.station_id),
    [vehicles],
  );

  const reload = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [r, v, s] = await Promise.all([listRentals(), listVehicles(), listStations()]);
      setRentals(r);
      setVehicles(v);
      setStations(s);
      const available = availableVehiclesFromList(v);
      setCheckoutVehicleId((prev) => prev || available[0]?.id || "");
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  async function onCheckout(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await checkoutRental(checkoutVehicleId);
      setCheckoutOpen(false);
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  async function onReturn(rentalId: string, stationId: string) {
    setError(null);
    try {
      await returnRental(rentalId, stationId);
      setReturnRentalId(null);
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  async function onRecordPayment(rentalId: string) {
    setError(null);
    try {
      await recordRentalPayment(rentalId);
      await reload();
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  return (
    <main className="console-page">
      <h1>Rentals</h1>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />

      <Toolbar>
        <button type="button" className="btn-primary" onClick={() => setCheckoutOpen(true)}>
          Check out vehicle
        </button>
      </Toolbar>

      {loading ? (
        <p>Loading…</p>
      ) : (
        <table className="console-table">
          <thead>
            <tr>
              <th>Vehicle</th>
              <th>Status</th>
              <th>Checkout station</th>
              <th>Return station</th>
              <th>Amount owed</th>
              <th>Paid</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {rentals.map((rental) => {
              const open = rental.ended_at === null;
              return (
                <tr key={rental.id}>
                  <td className="mono">{rental.vehicle_id.slice(0, 8)}…</td>
                  <td>
                    <span className={open ? "badge open" : "badge closed"}>
                      {open ? "Open" : "Closed"}
                    </span>
                  </td>
                  <td>{stationName.get(rental.checkout_station_id) ?? rental.checkout_station_id}</td>
                  <td>
                    {rental.return_station_id
                      ? (stationName.get(rental.return_station_id) ?? rental.return_station_id)
                      : "—"}
                  </td>
                  <td>{rental.amount_owed ?? "—"}</td>
                  <td>{rental.paid ? "Yes" : "No"}</td>
                  <td className="actions-cell">
                    {open ? (
                      <button
                        type="button"
                        className="btn-secondary"
                        onClick={() => setReturnRentalId(rental.id)}
                      >
                        Return
                      </button>
                    ) : null}
                    {!open && !rental.paid && rental.amount_owed !== null ? (
                      <button
                        type="button"
                        className="btn-secondary"
                        onClick={() => void onRecordPayment(rental.id)}
                      >
                        Record payment
                      </button>
                    ) : null}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}

      {checkoutOpen ? (
        <div className="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="checkout-title">
          <div className="modal">
            <h2 id="checkout-title">Check out vehicle</h2>
            <form onSubmit={onCheckout}>
              <label>
                Parked vehicle
                <select
                  value={checkoutVehicleId}
                  onChange={(e) => setCheckoutVehicleId(e.target.value)}
                  required
                >
                  {availableVehicles.map((v) => (
                    <option key={v.id} value={v.id}>
                      {v.id.slice(0, 8)}… @{" "}
                      {v.station_id ? (stationName.get(v.station_id) ?? v.station_id) : "?"}
                    </option>
                  ))}
                </select>
              </label>
              {availableVehicles.length === 0 ? (
                <p className="hint">No parked vehicles available for checkout.</p>
              ) : null}
              <div className="modal-actions">
                <button type="button" className="btn-secondary" onClick={() => setCheckoutOpen(false)}>
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn-primary"
                  disabled={availableVehicles.length === 0}
                >
                  Confirm checkout
                </button>
              </div>
            </form>
          </div>
        </div>
      ) : null}

      {returnRentalId ? (
        <ReturnModal
          key={returnRentalId}
          stations={stations}
          onCancel={() => setReturnRentalId(null)}
          onConfirm={(stationId) => void onReturn(returnRentalId, stationId)}
        />
      ) : null}
    </main>
  );
}

function availableVehiclesFromList(vehicles: Vehicle[]): Vehicle[] {
  return vehicles.filter((v) => v.available && v.station_id);
}

function Toolbar({ children }: { children: ReactNode }) {
  return <div className="toolbar">{children}</div>;
}

function ReturnModal({
  stations,
  onCancel,
  onConfirm,
}: {
  stations: Station[];
  onCancel: () => void;
  onConfirm: (stationId: string) => void;
}) {
  const [stationId, setStationId] = useState(stations[0]?.id ?? "");

  return (
    <div className="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="return-title">
      <div className="modal">
        <h2 id="return-title">Return rental</h2>
        <label>
          Return to station
          <select value={stationId} onChange={(e) => setStationId(e.target.value)} required>
            {stations.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </label>
        <div className="modal-actions">
          <button type="button" className="btn-secondary" onClick={onCancel}>
            Cancel
          </button>
          <button
            type="button"
            className="btn-primary"
            disabled={!stationId}
            onClick={() => onConfirm(stationId)}
          >
            Confirm return
          </button>
        </div>
      </div>
    </div>
  );
}
