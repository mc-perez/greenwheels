# Design

## Context

See `proposal.md`. APIs exist for types, stations, fleet, and rentals. Public checkout cannot backdate `started_at`. Seed runs only on an **empty** database (user decision). Urban bbox validation lives in `app/geo/tandil.py`.

## Goals / Non-Goals

**Goals:**

- `POST /api/v1/seed` → 201 + summary JSON on empty DB; **409** if any row exists in `station`, `vehicle`, `vehicle_type`, or `rental`.
- Versioned landmark catalog (five entries) with coordinates verified inside urban bbox.
- `SeedService` in one transaction: types (if needed) → stations → 50 vehicles → 5 internal open rentals.
- Deterministic RNG: `random.Random(42)` for type/station picks and which vehicles go out.
- Five open rentals: clear `parked_station_id`, insert `rental` with `started_at = utc_now() - timedelta(hours=rng.randint(1, 48))`, copy `rate_at_checkout` from type.

**Non-Goals:**

- Reset endpoint, CLI-only seed without API, configurable counts, map endpoints.

## Decisions

### Empty check

```text
is_empty = not (stations OR vehicles OR vehicle_types OR rentals)
```

Any existing operator data → `SeedDatabaseNotEmptyError` → HTTP 409.

**Alternatives:** stations-only check — rejected; partial data leaves inconsistent state.

### Landmark catalog (`app/seed/tandil_landmarks.py`)

| Name | Capacity | Latitude | Longitude |
|------|----------|----------|-----------|
| Plaza Independencia | 25 | -37.32140 | -59.13310 |
| Parque Independencia | 20 | -37.32500 | -59.12800 |
| Terminal de Ómnibus | 30 | -37.32850 | -59.14500 |
| Cerro El Divisorio | 15 | -37.31500 | -59.11800 |
| UNCPBA | 20 | -37.33900 | -59.10500 |

Unit test: every pair passes `is_inside_tandil_urban`.

### Demo vehicle types (only when type table empty)

| Name | Rate (per minute) |
|------|-------------------|
| Bici urbana | 150 |
| Monopatín | 220 |
| Bici eléctrica | 180 |
| Moto eléctrica | 300 |

### Vehicle and rental counts

- 50 vehicles total; RNG assigns type and station for all.
- After creating parked vehicles, pick **5 distinct vehicle indices** via `rng.sample(range(50), 5)` for open rentals.
- Remaining 45 stay parked (`available` true).

### Internal open rental

Method on `SeedService` (not public API):

- Read vehicle, type rate, `checkout_station_id = vehicle.parked_station_id`.
- Create `Rental` open row, set `vehicle.parked_station_id = None`.
- Does not call `RentalService.checkout` (no backdated `started_at` on public path).

### API

| Method | Path | Response |
|--------|------|----------|
| POST | `/seed` | 201 `SeedResult`: `stations`, `vehicle_types`, `vehicles`, `open_rentals` counts |

Register router under `/api/v1`.

### Testing

- `test_seed_tandil_landmarks.py` — bbox + exact coords.
- `test_seed_empty.py` — full seed assertions, deterministic first vehicle, 409 on non-empty.
- Use existing HTTP client + PostgreSQL session rollback pattern.

## Risks / Trade-offs

- **[Risk]** Landmark coords drift from "real" perception → **Mitigation**: documented places; coords fixed in catalog.
- **[Risk]** Empty check blocks seed after failed partial seed → **Mitigation**: transaction rollback on error.
- **[Risk]** SQLite tests lack partial rental index → **Mitigation**: seed logic enforces one open rental per vehicle.

## Migration Plan

- No schema change; application-only.

## Open Questions

- None blocking.
