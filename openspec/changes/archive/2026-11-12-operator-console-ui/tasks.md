# Tasks

## 1. Shell and shared client

- [x] 1.1 Add `react-router-dom` to `frontend/package.json` and verify `npm ci` succeeds.
- [x] 1.2 Add `fetchJson` helper with `VITE_API_BASE_URL` and typed API error parsing; verify a smoke import from `App.tsx` builds.
- [x] 1.3 Wrap app in `BrowserRouter`, add `OperatorLayout` nav (Map, Catalogs, Rentals), mount existing `StationMap` at `/`; verify **Scenario: Default route shows the map** manually at `http://localhost:5173/`.
- [x] 1.4 Add `ErrorBanner` component; verify a forced bad request shows API `detail` text (**Scenario: Validation error on station create** can use this later).

## 2. Vehicle types catalog

- [x] 2.1 Document manual steps for **Scenario: Add type from console** and **Scenario: Delete refused type stays listed** in README draft section (before UI).
- [x] 2.2 Implement `api/vehicleTypes.ts` and types page (list + create form); verify add scenario with name `"Bici urbana"` rate `150`.
- [x] 2.3 Add rename, rate edit, and delete actions; verify delete-in-use shows error and list unchanged.

## 3. Stations catalog

- [x] 3.1 Document manual steps for **Scenario: Add urban station from console** in README.
- [x] 3.2 Implement `api/stations.ts` and stations page (list + create/edit); verify add `"Centro"` capacity `20` at urban coordinates.
- [x] 3.3 Wire delete with confirm; verify API rejections surface in `ErrorBanner`.

## 4. Fleet catalog

- [x] 4.1 Document manual steps for **Scenario: Add parked vehicle from console** and **Scenario: Checkout candidate list excludes vehicles out on rental**.
- [x] 4.2 Implement `api/vehicles.ts` and vehicles page (list with type/station names, add form); verify add parked vehicle.
- [x] 4.3 Add patch/delete when API allows; verify list refresh after mutations.

## 5. Rentals workflow

- [x] 5.1 Document manual steps for checkout, return, payment, and conflict scenarios from `specs/operator-console/spec.md`.
- [x] 5.2 Implement `api/rentals.ts` and rentals list page; verify open vs closed and `paid` badges against seeded data.
- [x] 5.3 Add checkout modal with available-vehicle picker only; verify **Scenario: Successful checkout from console** and **Scenario: Checkout conflict surfaced in console**.
- [x] 5.4 Add return action with station select; verify **Scenario: Return to full station from console**.
- [x] 5.5 Add record-payment action; verify **Scenario: Record payment on closed rental**.

## 6. Build, regression, documentation

- [x] 6.1 Run `npm run build` and `npm run lint` in `frontend/`; verify both exit 0.
- [x] 6.2 Run `docker compose --profile test run --rm test` from repo root; verify pytest suite still passes (no backend edits expected).
- [x] 6.3 Finish README operator console section (URLs, nav, manual checklist for all console scenarios); verify commands match compose ports.

## Workflow follow-up

- Review artifacts and manual UI checks, then run `openspec archive` for `operator-console-ui` when satisfied.
- Sync updates `openspec/specs/operator-console/spec.md` from the change delta.
