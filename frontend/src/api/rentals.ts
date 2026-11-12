import { fetchJson } from "./client";

export type Rental = {
  id: string;
  vehicle_id: string;
  checkout_station_id: string;
  return_station_id: string | null;
  rate_at_checkout: string;
  started_at: string;
  ended_at: string | null;
  amount_owed: string | null;
  paid: boolean;
};

export function listRentals(): Promise<Rental[]> {
  return fetchJson<Rental[]>("/api/v1/rentals");
}

export function checkoutRental(vehicleId: string): Promise<Rental> {
  return fetchJson<Rental>("/api/v1/rentals/checkout", {
    method: "POST",
    body: JSON.stringify({ vehicle_id: vehicleId }),
  });
}

export function returnRental(rentalId: string, stationId: string): Promise<Rental> {
  return fetchJson<Rental>(`/api/v1/rentals/${rentalId}/return`, {
    method: "POST",
    body: JSON.stringify({ station_id: stationId }),
  });
}

export function recordRentalPayment(rentalId: string): Promise<Rental> {
  return fetchJson<Rental>(`/api/v1/rentals/${rentalId}/record-payment`, {
    method: "POST",
  });
}
