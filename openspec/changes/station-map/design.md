# Design

## Context

See `proposal.md`. Backend capabilities 1–5 are implemented; CORS allows `http://localhost:5173`. There is no frontend package yet. Fleet defines **available** as parked at a station (`parked_station_id` set). User decisions: server-side map read model (`GET /api/v1/map/stations`), all catalog types with zero counts, show capacity on selection, single fetch on app open, `fitBounds`, empty list UX, Vite dev in Compose, pytest for API only.

## Goals / Non-Goals

**Goals:**

- `GET /api/v1/map/stations` → 200 JSON with `stations[]` each carrying map fields + `availability_by_type[]` (`vehicle_type_id`, `vehicle_type_name`, `available_count`).
- Aggregate in one service query path: group parked vehicles by `(parked_station_id, vehicle_type_id)`, join types and stations, fill missing type rows with `0`.
- React + Vite + `react-leaflet` + OSM tile URL (standard `{s}.tile.openstreetmap.org` or project default).
- Docker Compose `frontend` service on `5173`, env `VITE_API_BASE_URL` (or equivalent) pointing at host-reachable API (`http://localhost:8000` from browser).

**Non-Goals:**

- Alembic changes, `GET /vehicles?station_id=`, per-station refetch endpoints, Playwright, nginx prod image, rental or CRUD UI.

## Decisions

### Map API shape

- **Router:** `app/api/map.py`, prefix `/map`, registered in `api_router`.
- **Route:** `GET /stations` → full path `/api/v1/map/stations`.
- **Response:** top-level `{ "stations": [...] }` to allow future map metadata without breaking clients.

**Alternatives:** Extend `GET /stations` — rejected; pollutes stations CRUD contract.

### Count algorithm

```text
FOR each station S:
  FOR each vehicle_type T in catalog (stable order by name):
    count = vehicles where parked_station_id = S.id AND vehicle_type_id = T.id
    emit { T, count }
```

Use SQL `GROUP BY` where possible; application layer fills zeros for `(S, T)` pairs with no rows. Open rentals already have `parked_station_id` null — no rental join needed.

### Frontend architecture

- Single `useEffect` on mount → fetch map stations → state drives `MapContainer`, `Marker`, side panel.
- Leaflet `fitBounds` on marker lat/lng array when `stations.length > 0`; when empty, default center near Tandil urban center (constants in frontend, not duplicated bbox logic).
- Selection: click marker → highlight + panel (not Leaflet popup required; panel acceptable if spec scenarios are met).

### Docker

- `frontend/Dockerfile`: Node image, `npm ci`, `CMD npm run dev -- --host 0.0.0.0`.
- Compose: `ports: "5173:5173"`, `depends_on: api`, volumes for hot reload optional for dev learning project.

### Testing

- Pytest modules mirroring map API scenarios (empty DB, explicit parks, open rental exclusion, all types with zero, capacity not cap).
- UI scenarios validated manually; document in README test plan.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Stale counts while app stays open | Accepted for v1; operator refreshes browser |
| OSM tile rate limits / offline | Dev message in README; no hard dependency in tests |
| Browser calls API on host vs Docker network | Document `localhost:8000` for Vite in Docker; API published on 8000 |

## Migration Plan

- Deploy order: pull → `docker compose build` (api + new frontend) → `up -d`.
- No DB migration. Rollback: stop frontend service; remove router if reverting API only.

## Open Questions

- None blocking; tile attribution string and default empty-map center are implementation choices.
