# Tasks

## 1. Landmark catalog

- [x] 1.1 Add `app/seed/tandil_landmarks.py` with five landmarks and demo vehicle types; unit-test all landmarks inside urban bbox.
- [x] 1.2 Document landmark names in design-aligned constants; verify tests pass.

## 2. Seed service core

- [x] 2.1 Write unit test for `database_is_empty` / `database_is_seedable`; verify fails before implementation.
- [x] 2.2 Implement empty-network guard and `SeedService.run()` transaction skeleton; verify guard tests pass.

## 3. Seed on empty database (RF-SE-4)

- [x] 3.1 Write API tests **Seed succeeds on empty database** and **Seed rejected when network is not empty**; verify fail before `POST /api/v1/seed`.
- [x] 3.2 Implement `POST /api/v1/seed` and wire router; verify empty/409 scenarios pass.

## 4. Stations and types (RF-SE-1)

- [x] 4.1 Write API test **Landmark stations are stored**; verify fails before seed creates stations.
- [x] 4.2 Seed creates five stations and four demo types when empty; verify landmark scenario passes.

## 5. Fifty vehicles (RF-SE-2)

- [x] 5.1 Write API test **Fifty vehicles after seed** including deterministic index-0 assignment on fresh DB; verify fails before vehicle loop.
- [x] 5.2 Implement RNG seed 42 vehicle creation; verify scenario passes.

## 6. Open rentals (RF-SE-3)

- [x] 6.1 Write API tests **Open rentals reduce availability** and **Open rental references a seeded station**; verify fail before internal open-rental path.
- [x] 6.2 Implement five internal open rentals with past `started_at`; verify scenarios pass.

## 7. Suite and docs

- [x] 7.1 Add `SeedResult` schema and conftest helper `seed_via_api` if useful.
- [x] 7.2 Run `docker compose build api` and `docker compose --profile test run --rm test`; verify full suite passes.
- [x] 7.3 Update README with seed endpoint and empty-database note.

## Workflow follow-up

- Archive with `openspec archive` after review when Docker pytest is green.
