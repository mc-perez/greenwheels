# rentals Specification

## Purpose
Records operator checkout and return for fleet vehicles, snapshots per-minute pricing at checkout, computes amount owed from time out, and records payment without a card gateway.

## Requirements

### Requirement: Operator can check out a parked vehicle

The system SHALL start an open rental when the vehicle is parked, has no other open rental, and SHALL copy the vehicle type's current rate as `rate_at_checkout` in price-per-minute units.

#### Scenario: Checkout copies rate and opens rental

- **WHEN** a vehicle type exists with name `"Bici urbana"` and current rate `150`
- **AND** a vehicle of that type is parked at a station named `"Centro"`
- **AND** the operator checks out that vehicle
- **THEN** the system stores a rental with `rate_at_checkout` `150`
- **AND** the rental has no end time
- **AND** the vehicle shows `available` false and no parked station

### Requirement: Checkout rejected when vehicle is not parked

The system SHALL reject checkout when the vehicle has no parked station.

#### Scenario: Reject checkout when vehicle already out

- **WHEN** a vehicle has no parked station
- **AND** the operator attempts checkout on that vehicle
- **THEN** the system rejects the request
- **AND** no new open rental is created

### Requirement: Checkout rejected when an open rental exists

The system SHALL reject checkout when the vehicle already has an open rental.

#### Scenario: Reject second checkout on same vehicle

- **WHEN** a vehicle has an open rental
- **AND** the operator attempts checkout on the same vehicle again
- **THEN** the system rejects the request
- **AND** exactly one open rental remains for that vehicle

### Requirement: Operator can return a vehicle to any station

The system SHALL close an open rental by parking the vehicle at an existing station and SHALL NOT reject return because station capacity would be exceeded.

#### Scenario: Return to a full station is allowed

- **WHEN** a vehicle is out on an open rental
- **AND** a station named `"Centro"` has stored capacity `1` and already has one parked vehicle
- **AND** the operator returns the rental to `"Centro"`
- **THEN** the rental is closed
- **AND** the returned vehicle is parked at `"Centro"`
- **AND** the vehicle shows `available` true

### Requirement: Return rejected when rental is not open

The system SHALL reject return when the rental is already closed or does not exist.

#### Scenario: Reject return on closed rental

- **WHEN** a rental is already closed
- **AND** the operator attempts return on that rental
- **THEN** the system rejects the request

### Requirement: Amount owed uses per-minute rate and ceiling minutes

The system SHALL set `amount_owed` to `rate_at_checkout` multiplied by the whole minutes between `started_at` and `ended_at`, counting any partial minute as one full minute.

#### Scenario: Ninety seconds out rounds up to two minutes

- **WHEN** a rental has `rate_at_checkout` `150`
- **AND** the rental `started_at` is `2026-06-01T12:00:00Z`
- **AND** the operator returns the vehicle with `ended_at` `2026-06-01T12:01:30Z`
- **THEN** the closed rental has `amount_owed` `300`

### Requirement: Type rate change does not alter open rental snapshot

The system SHALL keep an open rental's `rate_at_checkout` unchanged when the vehicle type's current rate is updated.

#### Scenario: Rate update after checkout leaves snapshot

- **WHEN** a vehicle type has current rate `150` and a vehicle is checked out with `rate_at_checkout` `150`
- **AND** the operator sets the type's current rate to `200`
- **THEN** the open rental still has `rate_at_checkout` `150`

### Requirement: Operator can list and get rentals

The system SHALL return rentals with identifiers, vehicle, stations, rate snapshot, start and end times, amount owed, and payment state.

#### Scenario: List includes open rental after checkout

- **WHEN** the operator checks out one vehicle
- **AND** the operator requests the rental list
- **THEN** the response includes one open rental for that vehicle

### Requirement: Operator can record payment

The system SHALL record that a closed rental was paid when the operator marks it paid.

#### Scenario: Record payment on closed rental

- **WHEN** a rental is closed with `amount_owed` `300` and not yet paid
- **AND** the operator records payment for that rental
- **THEN** the rental shows as paid
- **AND** `amount_owed` remains `300`

### Requirement: Payment rejected on open rental

The system SHALL reject recording payment while the rental is still open.

#### Scenario: Reject payment before return

- **WHEN** a rental is open
- **AND** the operator attempts to record payment
- **THEN** the system rejects the request
- **AND** the rental remains unpaid

### Requirement: Payment rejected when already paid

The system SHALL reject recording payment again when the rental is already paid.

#### Scenario: Reject duplicate payment

- **WHEN** a closed rental is already paid
- **AND** the operator attempts to record payment again
- **THEN** the system rejects the request
