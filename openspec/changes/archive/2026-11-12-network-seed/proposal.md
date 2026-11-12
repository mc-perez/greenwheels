# Proposal

## Why

The operator needs a realistic Tandil network in one action before the station map and demos. Capabilities 1–4 provide catalogs and rentals, but nothing loads the constitution's demo dataset (5 real stations, 50 vehicles, some vehicles out on open rentals).

## What Changes

- Add operator `POST /api/v1/seed` that populates the database **only when empty** (409 if any station, vehicle, vehicle type, or rental already exists).
- Create a fixed catalog of **five Tandil landmarks** with documented coordinates inside the urban bounding box.
- Create demo **vehicle types** when the type catalog is empty (four types with per-minute rates).
- Create **fifty vehicles** with pseudo-random type and parked station assignments using a **fixed RNG seed** (`42`) for reproducible tests.
- Place **five vehicles** on **open rentals** with `started_at` in the past via an internal seed path (not the public checkout API).
- Expose a seed summary in the HTTP response (counts of stations, vehicles, open rentals).

## Capabilities

### New Capabilities

- `seed`: Operator loads the demo Tandil network once on an empty database.

### Modified Capabilities

<!-- None -->

## Functional Requirements Addressed

From `requirements.md` **Capabilities → 5. Seed**:

| RF | Requirement |
|----|-------------|
| RF-SE-1 | Five stations at **real places in Tandil**, not invented coordinates. |
| RF-SE-2 | Fifty vehicles, each with a random type and random parked station (for vehicles not placed out). |
| RF-SE-3 | A few vehicles **out on open rentals** with past start times so availability is not the full fleet. |
| RF-SE-4 | Seed runs **only on an empty network**; no destructive reset in this change. |

## Out of Scope

- Station map UI, OpenStreetMap, and availability-by-type API (map capability).
- `POST /seed/reset` or any wipe of existing operator data.
- Custom operator-chosen RNG seed, vehicle counts, or landmark lists via API.
- Card payments, authentication, public client.
- Proving landmarks against live OpenStreetMap at runtime (coordinates are versioned in the repository).

## Impact

- New `SeedService`, landmark catalog module, `POST /api/v1/seed`, pytest with deterministic counts.
- README documents seed endpoint and empty-database requirement.
- Docker operators may use `docker compose down -v` before re-seeding.
