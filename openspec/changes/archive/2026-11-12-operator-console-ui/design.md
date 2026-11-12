# Design

## Context

See `proposal.md`. Backend capabilities for vehicle types, stations, fleet, and rentals are implemented and covered by pytest. The frontend today renders only `StationMap` at the app root. API base URL comes from `VITE_API_BASE_URL` (default `http://localhost:8000`). Error bodies follow FastAPI `detail` (string or validation list).

## Goals / Non-Goals

**Goals:**

- `react-router-dom` (or equivalent) with routes: `/` (map), `/catalogs/types`, `/catalogs/stations`, `/catalogs/vehicles`, `/rentals`.
- Thin typed clients in `frontend/src/api/` mirroring existing REST resources (`vehicleTypes.ts`, `stations.ts`, `vehicles.ts`, `rentals.ts`); reuse patterns from `api/map.ts`.
- `OperatorLayout`: top nav links, outlet for child routes, consistent loading and error banner component.
- Catalog pages: table list + inline or modal forms for create/edit; delete with confirm; refresh list after successful mutation.
- Rentals page: table of `GET /api/v1/rentals` with badges for open vs closed and paid; actions for checkout (modal), return (station select), record payment (disabled when not applicable).
- Checkout picker: `GET /api/v1/vehicles` filtered client-side to `available === true` (parked); join type and station names from parallel catalog lists cached in layout or React context.
- Keep `StationMap` behavior unchanged (single map fetch on mount, no new map endpoints).

**Non-Goals:**

- Backend changes, Alembic, new aggregation endpoints.
- Optimistic UI, websockets, or live map refresh after rental actions (operator may reload map tab manually).
- Seed button, auth, i18n, Playwright.
- Replacing Swagger as API reference.

## Decisions

### Routing and shell

- **Choice:** `BrowserRouter` with path-based routes; default `/` remains the map for parity with v1.
- **Alternative:** Hash router — rejected; paths are clearer for manual testing.
- **Alternative:** Single-page tabs without URL — rejected; deep links help debugging.

### Data loading

- **Choice:** Each catalog page loads its list on mount; rentals page loads rentals plus vehicles/types/stations for display labels.
- **Alternative:** Global React Query — rejected for v1; extra dependency and patterns not yet in repo.

### Forms and validation

- **Choice:** HTML forms with controlled inputs; block submit when required fields empty; numeric fields for rate and capacity; lat/lon as text inputs matching API validation.
- **Alternative:** Full schema library (Zod) — optional later; start minimal.

### Error handling

- **Choice:** `fetch` wrapper throws `{ status, detail }`; UI shows `detail` string or first validation message.
- Map HTTP codes: `409` for business conflicts (delete in use, checkout rejected), `404` for missing ids, `422` for body validation.

### Styling

- **Choice:** Extend existing `App.css` / `index.css` with simple layout (nav bar, tables, buttons); no new CSS framework.
- Accessible labels on form fields; keyboard-usable tables.

### Testing

- **Choice:** Manual UI checklist in README (mirrors spec scenarios); `npm run build` and `npm run lint` in tasks; **no new pytest** (API unchanged).
- Existing `docker compose --profile test` must stay green without modification unless a regression appears.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Large single PR | Follow phased tasks (catalogs → fleet → rentals). |
| Stale map after rental | Document that map tab does not auto-refresh; optional follow-up. |
| UUID-only tables confuse operator | Join ids to names from catalog fetches in rental and vehicle lists. |
| 409 errors opaque | Surface API `detail` verbatim in banner. |

## Migration Plan

- Ship behind same `frontend` Docker service; no compose changes required beyond possible router `basename` if ever needed (default `/`).
- Rollback: revert frontend bundle; API untouched.

## Open Questions

- Whether return flow should default station to checkout station (UX only; API accepts any station).
- Whether to add a lightweight shared `CatalogCache` context in phase 1 or refetch names per page (implementation detail; either satisfies spec).
