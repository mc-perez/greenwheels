# Proposal

## Why

Fleet persists parked vehicles and reserves `parked_station_id` for vehicles out on rental, but checkout, return, pricing, and payment recording do not exist yet. Rental is capability 4 in the constitution order and unblocks Seed and the station map (availability counts).

## What Changes

- Introduce the `rental` table and Alembic revision linking vehicles, stations, and copied pricing.
- Expose operator HTTP API for **checkout**, **return**, **list/get rentals**, and **record payment** (no card gateway).
- On checkout: require parked vehicle with no open rental; copy `current_rate` as rate per minute; clear `parked_station_id`.
- On return: accept any existing station (capacity not a gate); set `parked_station_id`; close rental; compute `amount_owed` as `rate_at_checkout × minutes_out` with **integer minutes** via **ceiling** on elapsed time.
- Store and expose timestamps in **UTC** (ISO-8601).
- Reject fleet update or delete while a vehicle has an open rental.
- Document that `vehicle_type.current_rate` is **per minute** for rental billing.

## Capabilities

### New Capabilities

- `rentals`: Operator checkout, return, rental reads, amount owed, and payment recording for the local fleet.

### Modified Capabilities

- `fleet`: Refuse vehicle update and delete while the vehicle has an open rental.
- `vehicle-types`: Clarify that `current_rate` is the price per minute copied at rental checkout.

## Functional Requirements Addressed

From `requirements.md` **Capabilities → 4. Rental**:

| RF | Requirement |
|----|-------------|
| RF-RT-1 | Checkout is legal when the vehicle is parked and has no open rental; copies the type's current rate (per minute). |
| RF-RT-2 | Checkout clears parked station; vehicle is not available while out. |
| RF-RT-3 | Return is to any station, including a full one; capacity is not a gate. |
| RF-RT-4 | `amount_owed` = copied rate × minutes out (integer minutes, ceiling). |
| RF-RT-5 | Operator records that the rental was paid (no card charge). |
| RF-RT-6 | List and get rentals including open and closed states. |
| RF-RT-7 | Rate changes on the type apply only to future checkouts (existing open rental keeps its snapshot). |

## Out of Scope

- Seed data, map UI, public client, authentication, GPS, hardware docks.
- Card charging and payment gateway integration (simulated payment record only).
- Operator UI for rentals.
- Checkout API accepting custom `started_at` for backdating (Seed uses internal/service paths in its own change).
- Refunds, partial payments, and currency symbols in API.

## Impact

- New router under `/api/v1/rentals`, models, repository, service, Pydantic schemas.
- Alembic `0004_*`; updates to `VehicleService` / rental service coordination.
- Tests with controlled UTC timestamps for ceiling minute scenarios.
- README API slice update after implementation.
