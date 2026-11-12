# Design

## Context

See `proposal.md`. Fleet exposes `/api/v1/vehicles` with nullable `parked_station_id`. Vehicle types expose `current_rate`. No rental table yet. User decisions: rate **per minute**, integer minutes with **ceiling**, timestamps **UTC**.

## Goals / Non-Goals

**Goals:**

- Table `rental` with at most one open row per `vehicle_id`.
- Checkout, return, list, get, record payment via `/api/v1/rentals`.
- Coordinated updates to `vehicle.parked_station_id` and rental lifecycle in one transaction.
- `minutes_out = ceil(seconds_elapsed / 60)`; `amount_owed = rate_at_checkout * minutes_out` as `Decimal`.
- Fleet PATCH/DELETE guard when open rental exists (query rental repo or service).

**Non-Goals:**

- Seed/backdated `started_at` via public API.
- Payment gateway; currency metadata.
- Changing vehicle type on vehicle during open rental via fleet API.

## Decisions

### Data model

Table `rental`:

| Column | Notes |
|--------|--------|
| `id` | UUID PK |
| `vehicle_id` | FK, indexed |
| `checkout_station_id` | FK → station (where vehicle was parked at checkout) |
| `return_station_id` | FK nullable until return |
| `rate_at_checkout` | Numeric, per minute |
| `started_at` | timestamptz UTC |
| `ended_at` | timestamptz nullable |
| `amount_owed` | Numeric nullable until return |
| `paid_at` | timestamptz nullable |

**Open rental:** `ended_at IS NULL`.

**Uniqueness:** partial unique index one open rental per `vehicle_id` (PostgreSQL) or enforce in service + test.

Alembic `0004_rental`.

### Time and billing

- All rental timestamps stored and returned as timezone-aware UTC (ISO-8601 with `Z` or offset).
- Return sets `ended_at` to server UTC now unless design adds body override later (not in this slice).
- `minutes_out = math.ceil((ended_at - started_at).total_seconds() / 60)` minimum 1 when `ended_at > started_at`? For zero duration edge: if same instant, ceil(0)=0 — spec scenario needs positive elapsed; document 0-minute edge as 0 owed or reject; **use max(1, ceil(...)) only if spec demands** — spec says 90s → 2 min; 0s could be 0 minutes with ceil(0)=0. Keep pure ceil.

### API shape

| Method | Path | Behavior |
|--------|------|----------|
| POST | `/rentals/checkout` | Body: `vehicle_id` → 201 open rental + vehicle out |
| POST | `/rentals/{id}/return` | Body: `station_id` → 200 closed rental + vehicle parked |
| GET | `/rentals` | List |
| GET | `/rentals/{id}` | 200/404 |
| POST | `/rentals/{id}/record-payment` | 200; 409 if open or already paid |

**Alternatives:** Nested under vehicles — rejected; rentals are first-class for Seed/map later.

### Layering

- `RentalService` orchestrates rental + vehicle rows in one session transaction.
- `VehicleService` gains dependency on open-rental check for update/delete, or rental repository method `has_open_rental(vehicle_id)`.

### Fleet integration

- On checkout: `parked_station_id = None`.
- On return: `parked_station_id = return station_id`.
- `VehicleRead.available` unchanged logic (`parked_station_id is not None`).

### Testing

- Use `freezegun` or injectable clock only if needed; prefer explicit `started_at`/`ended_at` set in service tests, or return endpoint that uses known times via test-only hook — **prefer controlling time in integration tests** by patching `datetime.now(timezone.utc)` in service module for return scenario.
- One pytest module per requirement group.
- Regression: existing fleet delete integration still passes when no open rental.

## Risks / Trade-offs

- **[Risk]** Clock skew in Docker tests → **Mitigation**: freeze/patch UTC `now` in return test.
- **[Risk]** Partial unique index not portable to SQLite tests → **Mitigation**: service check + PostgreSQL migration test; SQLite relies on service rule.
- **[Risk]** Two services updating vehicle → **Mitigation**: single `RentalService` owns checkout/return mutations.

## Migration Plan

- `alembic upgrade head`; downgrade drops `rental`.

## Open Questions

- None blocking.
