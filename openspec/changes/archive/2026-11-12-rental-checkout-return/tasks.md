# Tasks

## 1. Schema and migrations

- [x] 1.1 Extend migration test for `rental` table after `0004`; verify fails before revision exists.
- [x] 1.2 Add Alembic `0004_rental` with FKs and open-rental uniqueness guard (partial index on PostgreSQL); verify migration test passes.

## 2. Billing helper (RF-RT-4)

- [x] 2.1 Add unit tests for ceiling minutes and `amount_owed` (`150` rate, 90s elapsed → `300`); verify fail before helper exists.
- [x] 2.2 Implement `minutes_out_ceiling` and `compute_amount_owed`; verify unit tests pass.

## 3. Checkout (RF-RT-1, RF-RT-2, RF-VT rate unit)

- [x] 3.1 Write API tests **Checkout copies rate and opens rental**, **Reject checkout when vehicle already out**, **Reject second checkout**; verify fail before checkout route.
- [x] 3.2 Implement `Rental` model, repository, service checkout, `POST /api/v1/rentals/checkout`; verify scenarios pass.

## 4. Return (RF-RT-3, RF-RT-4)

- [x] 4.1 Write API tests **Return to a full station is allowed** and **Reject return on closed rental**; include ceiling amount scenario with patched UTC `now`; verify fail before return route.
- [x] 4.2 Implement `POST /api/v1/rentals/{id}/return`; verify scenarios pass.

## 5. Rate snapshot (RF-RT-7)

- [x] 5.1 Write API test **Rate update after checkout leaves snapshot**; verify fails before snapshot behavior exists.
- [x] 5.2 Ensure checkout reads type rate once; verify scenario passes.

## 6. List and get (RF-RT-6)

- [x] 6.1 Write API test **List includes open rental after checkout**; verify fail before list route.
- [x] 6.2 Implement `GET /api/v1/rentals` and `GET /api/v1/rentals/{id}`; verify scenarios pass.

## 7. Payment (RF-RT-5)

- [x] 7.1 Write API tests **Record payment on closed rental**, **Reject payment before return**, **Reject duplicate payment**; verify fail before payment route.
- [x] 7.2 Implement `POST /api/v1/rentals/{id}/record-payment`; verify scenarios pass.

## 8. Fleet guards (delta fleet)

- [x] 8.1 Write API tests **Patch refused while rental is open** and **Delete refused while rental is open**; verify fail before guards.
- [x] 8.2 Add open-rental checks to vehicle update/delete; verify scenarios pass and existing fleet tests still pass.

## 9. Suite and docs

- [x] 9.1 Register `Rental` in conftest metadata; add helpers to checkout/return in tests.
- [x] 9.2 Run `docker compose build api` and `docker compose --profile test run --rm test`; verify full suite passes.
- [x] 9.3 Update README with rental endpoints; verify against OpenAPI.

## Workflow follow-up

- Archive with `openspec archive` after review when Docker pytest is green.
