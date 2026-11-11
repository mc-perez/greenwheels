# Proposal

## Why

GreenWheels needs an operator-managed catalog of vehicle types before stations, fleet, rentals, or the map can reason about availability and pricing. Vehicle types are the first capability in the constitution order and underpin every later checkout that copies a type's current rate.

## What Changes

- Introduce persistence and API for operator vehicle types: name and current rate.
- Support add, rename, update current rate, list, and delete when no vehicle references the type.
- Expose a fleet-usage guard for delete (stub returns "unused" until the fleet capability exists).
- Bootstrap the backend project layout, database, Docker, and pytest harness required for this slice.

## Capabilities

### New Capabilities

- `vehicle-types`: Operator catalog — add and rename types, hold a current rate per type, refuse delete while any vehicle uses the type, with rate updates affecting only the stored current rate (checkout copy behavior is owned by the rental capability).

### Modified Capabilities

<!-- None — no main specs exist yet. -->

## Functional Requirements Addressed

From `requirements.md` **Capabilities → 1. Vehicle types**:

| RF | Requirement |
|----|-------------|
| RF-VT-1 | Operator can add a vehicle type with a name and a rate. |
| RF-VT-2 | Operator can rename a vehicle type. |
| RF-VT-3 | Operator can change a type's rate; the catalog stores the new current rate only (future-checkout effect is verified under rental). |
| RF-VT-4 | Operator can delete a type when no vehicle uses it. |
| RF-VT-5 | Delete is refused while a vehicle uses the type (rule specified here; full integration test when fleet exists). |

## Out of Scope

- Authentication, public client, UI screens (including the station map).
- Stations, fleet, rentals, seed data, and payment recording.
- Proving that an open rental keeps its copied rate after a rate change (rental capability).
- Currency symbol, billing time unit, and time zone (pending explicit product decisions).
- Uniqueness or validation rules for type names beyond non-empty (unless added in design as an open question).

## Impact

- New FastAPI application module and REST endpoints under a local API (no auth).
- New PostgreSQL table(s) for vehicle types via SQLModel.
- Docker Compose services for API and database.
- Initial pytest suite and CI-friendly test layout.
