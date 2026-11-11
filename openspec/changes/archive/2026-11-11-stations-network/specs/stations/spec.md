# Spec Delta

## Purpose

Maintains the operator's network of rental stations in urban Tandil, each with a unique name, a stored capacity, and a map location used by later fleet, seed, and map capabilities.

## ADDED Requirements

### Requirement: Operator can add a station

The system SHALL create a station from a non-empty unique name, an integer capacity of at least 1, and a latitude and longitude inside the Tandil urban bounding box.

#### Scenario: Add station with name, capacity, and urban coordinates

- **WHEN** the operator adds a station with name `"Centro"`, capacity `20`, latitude `-37.32167`, and longitude `-59.13316`
- **THEN** the system stores the station and exposes the same name, capacity `20`, latitude `-37.32167`, and longitude `-59.13316`

### Requirement: Operator can list stations

The system SHALL return every station with its identifier, name, capacity, latitude, and longitude.

#### Scenario: List after one add

- **WHEN** the operator adds a station with name `"Plaza Independencia"`, capacity `15`, latitude `-37.32120`, and longitude `-59.13250`
- **AND** the operator requests the station list
- **THEN** the response includes one entry with name `"Plaza Independencia"`, capacity `15`, latitude `-37.32120`, and longitude `-59.13250`

### Requirement: Operator can get a station by identifier

The system SHALL return one station by identifier or report that it does not exist.

#### Scenario: Get existing station

- **WHEN** a station exists with name `"Centro"` and the operator requests it by its identifier
- **THEN** the response includes name `"Centro"`, its capacity, latitude, and longitude

### Requirement: Operator can update a station

The system SHALL update an existing station's name, capacity, and/or location when the operator supplies at least one of those fields.

#### Scenario: Update capacity preserves name and location

- **WHEN** a station exists with name `"Centro"`, capacity `20`, latitude `-37.32167`, and longitude `-59.13316`
- **AND** the operator sets capacity to `25`
- **THEN** the station has name `"Centro"`, capacity `25`, latitude `-37.32167`, and longitude `-59.13316`

### Requirement: Station location outside the urban bounding box is rejected

The system SHALL reject a create or location update when latitude or longitude falls outside the Tandil urban bounding box.

#### Scenario: Reject latitude south of urban south edge

- **WHEN** the operator adds a station with name `"Sur inválido"`, capacity `10`, latitude `-37.41000`, and longitude `-59.13316`
- **THEN** the system rejects the request
- **AND** the station does not appear in the station list

#### Scenario: Reject longitude west of urban west edge

- **WHEN** the operator adds a station with name `"Oeste inválido"`, capacity `10`, latitude `-37.32167`, and longitude `-59.23000`
- **THEN** the system rejects the request
- **AND** the station does not appear in the station list

### Requirement: Station names are unique

The system SHALL reject a create or name update that would duplicate another station's name.

#### Scenario: Reject add with duplicate station name

- **WHEN** a station exists with name `"Centro"`
- **AND** the operator adds a station with name `"Centro"`, capacity `10`, latitude `-37.32000`, and longitude `-59.13000`
- **THEN** the system rejects the request
- **AND** exactly one station named `"Centro"` remains in the station list

#### Scenario: Reject rename to another station's name

- **WHEN** stations exist with names `"Centro"` and `"Norte"`
- **AND** the operator renames `"Norte"` to `"Centro"`
- **THEN** the system rejects the rename
- **AND** the station list still includes one `"Centro"` and one `"Norte"`

### Requirement: Capacity is stored and not used as an occupancy gate

The system SHALL store capacity as provided and SHALL NOT reject create or update based on how many vehicles would occupy the station.

#### Scenario: Update capacity below any future occupancy is allowed

- **WHEN** a station exists with name `"Centro"` and capacity `20`
- **AND** the operator sets capacity to `1`
- **THEN** the station's stored capacity is `1`

### Requirement: Operator can delete an unused station

The system SHALL remove a station when the fleet reports no vehicles at that station.

#### Scenario: Delete when fleet reports no vehicles at station

- **WHEN** a station exists with name `"Centro"`
- **AND** the fleet reports zero vehicles at that station
- **AND** the operator deletes the station
- **THEN** the station no longer appears in the station list

### Requirement: Delete is refused while the fleet reports vehicles at the station

The system SHALL reject station deletion when the fleet reports at least one vehicle at that station.

#### Scenario: Delete refused when fleet reports usage

- **WHEN** a station exists with name `"Centro"`
- **AND** the fleet reports one or more vehicles at that station
- **AND** the operator attempts to delete the station
- **THEN** the system rejects the delete
- **AND** the station remains in the station list with unchanged name, capacity, and location

## Out of Scope (this change)

- Fleet parked counts, rentals, seed landmarks, map UI, and authentication.
- Blocking returns or parks when stored capacity is exceeded (rental and fleet capabilities).
- Validating that coordinates match a named real-world landmark (seed capability).
