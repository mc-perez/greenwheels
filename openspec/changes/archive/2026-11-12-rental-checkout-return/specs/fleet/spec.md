# Spec Delta

## ADDED Requirements

### Requirement: Vehicle update refused while on open rental

The system SHALL reject updating a vehicle's type or parked station when that vehicle has an open rental.

#### Scenario: Patch refused while rental is open

- **WHEN** a vehicle is out on an open rental
- **AND** the operator attempts to update that vehicle's type or parked station through the fleet API
- **THEN** the system rejects the request
- **AND** the vehicle and open rental are unchanged

### Requirement: Vehicle delete refused while on open rental

The system SHALL reject deleting a vehicle when that vehicle has an open rental.

#### Scenario: Delete refused while rental is open

- **WHEN** a vehicle is out on an open rental
- **AND** the operator attempts to delete the vehicle
- **THEN** the system rejects the request
- **AND** the vehicle remains in the fleet
