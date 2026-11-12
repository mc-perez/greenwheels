# Proposal

## Why

Capabilities 1–5 provide catalogs, rentals, and a demo seed, but the constitution's first screen—an OpenStreetMap of Tandil with station markers and availability by type—does not exist. The operator needs a dedicated map read model and a React UI that trusts system data instead of stitching CRUD list endpoints in the browser.

## What Changes

- Add `GET /api/v1/map/stations` returning every station with coordinates, stored capacity, and **available counts for every vehicle type in the catalog** (zero where none are parked at that station). Counts follow fleet availability (parked at the station).
- Add a React frontend (Vite on port `5173`) with Leaflet and OpenStreetMap tiles (no map API key).
- Load map data once on app open; station click opens a panel with station name, capacity, and per-type available counts (no refetch on click).
- Initial map view uses **fit bounds** to all station markers; when there are no stations, show the basemap and a clear empty message.
- Add a `frontend` Docker Compose service (Vite dev) alongside `db` and `api`; document the workflow in README.

## Capabilities

### New Capabilities

- `station-map`: Map read API and operator map UI (OpenStreetMap, station markers, availability by type on selection).

### Modified Capabilities

<!-- None: existing fleet/stations behavior unchanged; map consumes the same availability rules. -->

## Functional Requirements Addressed

From `requirements.md` **Capabilities → 6. Station map** and **Intent** (first screen is the map):

| RF | Requirement |
|----|-------------|
| RF-MP-1 | OpenStreetMap basemap with **no key and no account**. |
| RF-MP-2 | Map reads **stations from the system** and draws them at stored locations. |
| RF-MP-3 | Selecting a station shows **how many vehicles of each type are available** there (parked = available). |
| RF-MP-4 | Station location and counts come from the **system's data** via a map read endpoint, not ad-hoc client aggregation of CRUD lists. |

## Out of Scope

- `GET /vehicles?station_id=` and other fleet list filters (map endpoint is the read model).
- Per-station lazy endpoints or refetch-on-click in v1.
- Rental checkout/return, payments, or any operator CRUD screens beyond the map.
- Authentication, public client, Google Maps, GPS, dock hardware.
- Playwright or other frontend e2e in CI (API covered by pytest; UI verified manually).
- Nginx static production frontend image in Compose (Vite dev service only for this change).
- Occupancy gates using station capacity (capacity is displayed only as stored fact).

## Impact

- New map router, service, schemas, and pytest modules under `backend/`.
- New `frontend/` package (React, Leaflet), Compose service, README updates.
- No Alembic migration (read-only aggregate over existing tables).
