# Proposal

## Why

The operator can run the full network through REST and Swagger, and the map is the only v1 screen. Day-to-day work—catalog edits, fleet moves, checkout, return, and recording payment—still requires an API client. A browser **operator console** on the same React app makes capabilities 1–4 usable without leaving the stack.

## What Changes

- Add client-side routing and a lightweight **operator console** shell in `frontend/` (tabs or nav: **Map**, **Catalogs**, **Rentals**).
- **Catalogs** views that call existing CRUD endpoints:
  - Vehicle types (`/api/v1/vehicle-types`)
  - Stations (`/api/v1/stations`)
  - Vehicles / fleet (`/api/v1/vehicles`)
- **Rentals** views that call existing rental endpoints:
  - List rentals and highlight open vs closed
  - Checkout (pick a parked, available vehicle)
  - Return open rental to a chosen station
  - Record payment on closed, unpaid rentals
- Shared typed API client modules, loading/error states, and forms validated before submit.
- README section: console URL, manual UI checklist, no new Compose services (still port `5173`).
- **No backend behavior or schema changes** in this change; CORS and OpenAPI contracts stay as-is.

## Capabilities

### New Capabilities

- `operator-console`: Operator-facing React UI that performs catalog and rental workflows by calling the existing REST API, alongside the existing station map.

### Modified Capabilities

<!-- Backend requirements unchanged; map behavior unchanged. Console is an additional client. -->

## Functional Requirements Addressed

From `requirements.md` **Capabilities** (operator actions today exist only on the API; this change exposes them in the UI):

| Capability | RF (summary) |
|------------|----------------|
| 1. Vehicle types | Catalog add, list, rename, rate change, delete when unused |
| 2. Stations | Network add, list, update, delete when safe |
| 3. Fleet | Parked vehicles add, list, patch station/type, delete when safe |
| 4. Rental | Checkout, return to any station, amount owed, record payment |

**Constitution note:** `requirements.md` listed “any screen other than the map” as out of scope for the initial OpenSpec sequence. This change **extends** the product after v1 map delivery; it does not alter backend rules.

## Slice strategy

This change touches **four** product capabilities. Per project rules, implementation SHOULD follow `tasks.md` in **three phases** (catalogs → fleet → rentals) so each phase can be reviewed and manually tested before the next. If scope feels too large in review, split into follow-up changes `operator-console-catalogs` and `operator-console-rentals` without rewriting backend specs.

## Out of Scope

- Authentication, roles, or multi-user accounts.
- Public rider client, mobile layout polish, or i18n.
- New API endpoints, aggregation BFFs, or GraphQL.
- Seed trigger UI (`POST /api/v1/seed` remains manual or Swagger).
- Map feature changes (tiles, fit bounds, single fetch, panel content).
- Payment gateway, refunds, or currency formatting beyond displaying API numeric fields.
- Playwright/e2e CI, nginx production frontend image.
- Editing closed rental history or overriding `amount_owed` in the UI.

## Impact

- **Frontend:** `frontend/src/` — router, layout, catalog and rental pages, API clients, styles.
- **Backend:** None (reuse existing routes and error codes).
- **Docker:** Same `frontend` service; may add `react-router-dom` dependency.
- **Docs:** README operator console workflow and manual test plan.
