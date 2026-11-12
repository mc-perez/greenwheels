# Spec Delta

## Purpose

Exposes operator catalog and rental workflows in the browser by calling the existing REST API, together with the station map, without changing backend business rules.

## ADDED Requirements

### Requirement: Operator can open the console beside the map

The system SHALL provide a single frontend application where the operator can navigate between the station map view and operator console views.

#### Scenario: Default route shows the map

- **WHEN** the operator opens the frontend root URL
- **THEN** the station map view is shown
- **AND** the operator can navigate to catalog and rental console views without a full page reload to another origin

### Requirement: Operator can manage vehicle types in the console

The system SHALL let the operator create, list, rename, update the current rate, and delete an unused vehicle type through the console by calling `POST`, `GET`, `PATCH`, and `DELETE` on `/api/v1/vehicle-types`.

#### Scenario: Add type from console

- **WHEN** the operator opens the vehicle types catalog view
- **AND** the operator submits name `"Bici urbana"` and current rate `150`
- **THEN** the console calls `POST /api/v1/vehicle-types` with that name and rate
- **AND** the list shows an entry with name `"Bici urbana"` and current rate `150`

#### Scenario: Delete refused type stays listed

- **WHEN** a vehicle references a type named `"Monopatín"`
- **AND** the operator attempts to delete that type in the console
- **THEN** the console shows the API error response
- **AND** `"Monopatín"` remains in the list

### Requirement: Operator can manage stations in the console

The system SHALL let the operator create, list, update, and delete a station when the API allows it, by calling `/api/v1/stations`.

#### Scenario: Add urban station from console

- **WHEN** the operator opens the stations catalog view
- **AND** the operator submits name `"Centro"`, capacity `20`, latitude `-37.32167`, and longitude `-59.13316`
- **THEN** the console calls `POST /api/v1/stations` with those fields
- **AND** the list shows `"Centro"` with capacity `20`

### Requirement: Operator can manage fleet vehicles in the console

The system SHALL let the operator create a parked vehicle, list vehicles with availability, update parked station or vehicle type when permitted, and delete when permitted, by calling `/api/v1/vehicles`.

#### Scenario: Add parked vehicle from console

- **WHEN** a vehicle type `"Bici urbana"` and a station `"Centro"` exist
- **AND** the operator adds a vehicle selecting that type and that parked station
- **THEN** the console calls `POST /api/v1/vehicles` with the selected identifiers
- **AND** the list shows the vehicle as available with the chosen type and station

#### Scenario: Checkout candidate list excludes vehicles out on rental

- **WHEN** one vehicle is parked at `"Centro"` and another vehicle of the same type has no parked station
- **AND** the operator opens the checkout vehicle picker
- **THEN** only the parked vehicle is offered for checkout

### Requirement: Operator can check out a vehicle from the console

The system SHALL start a rental by calling `POST /api/v1/rentals/checkout` with the selected vehicle identifier when the operator confirms checkout.

#### Scenario: Successful checkout from console

- **WHEN** a vehicle is parked at `"Centro"` and has no open rental
- **AND** the operator selects that vehicle and confirms checkout
- **THEN** the console calls `POST /api/v1/rentals/checkout` with that vehicle identifier
- **AND** the rentals view shows a new open rental for that vehicle

#### Scenario: Checkout conflict surfaced in console

- **WHEN** a vehicle is already out on an open rental
- **AND** the operator attempts checkout for that vehicle
- **THEN** the console shows the API rejection
- **AND** no duplicate open rental is shown in the list

### Requirement: Operator can return an open rental from the console

The system SHALL close an open rental by calling `POST /api/v1/rentals/{id}/return` with a chosen station identifier.

#### Scenario: Return to full station from console

- **WHEN** an open rental exists for a vehicle
- **AND** a station named `"Centro"` exists
- **AND** the operator returns the rental to `"Centro"`
- **THEN** the console calls `POST /api/v1/rentals/{id}/return` with that station identifier
- **AND** the rental is shown closed with return station `"Centro"` and an `amount_owed` value from the API

### Requirement: Operator can record payment from the console

The system SHALL record payment on a closed unpaid rental by calling `POST /api/v1/rentals/{id}/record-payment`.

#### Scenario: Record payment on closed rental

- **WHEN** a rental is closed with `amount_owed` `300` and `paid` false
- **AND** the operator records payment in the console
- **THEN** the console calls `POST /api/v1/rentals/{id}/record-payment`
- **AND** the rental is shown with `paid` true

### Requirement: Console shows API failures to the operator

The system SHALL display a human-readable error when the API responds with a client or server error status for a console action.

#### Scenario: Validation error on station create

- **WHEN** the operator submits a station outside the allowed coordinate rules
- **THEN** the console shows the API error detail
- **AND** the station list is unchanged
