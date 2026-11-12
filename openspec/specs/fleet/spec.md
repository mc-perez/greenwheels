# fleet Specification

## Purpose
Tracks the operator's fleet of rental vehicles, each assigned to exactly one vehicle type and parked at a station when managed through this API; exposes availability and backs delete guards for the vehicle-type and station catalogs.

## Requirements

### Requirement: Operator can add a parked vehicle

The system SHALL create a vehicle from an existing vehicle type identifier and an existing station identifier, and SHALL store the vehicle as parked at that station.

#### Scenario: Add vehicle with type and parked station

- **WHEN** a vehicle type exists with name `"Bici urbana"`
- **AND** a station exists with name `"Centro"`
- **AND** the operator adds a vehicle with that vehicle type identifier and that station identifier
- **THEN** the system stores the vehicle and exposes its identifier, vehicle type identifier, parked station identifier, and `available` true

### Requirement: Unknown vehicle type or station on add is rejected

The system SHALL reject adding a vehicle when the vehicle type identifier or station identifier does not exist.

#### Scenario: Reject add with unknown vehicle type

- **WHEN** a station exists with name `"Centro"`
- **AND** the operator adds a vehicle with an unknown vehicle type identifier and that station identifier
- **THEN** the system rejects the request
- **AND** the vehicle list remains empty

#### Scenario: Reject add with unknown station

- **WHEN** a vehicle type exists with name `"Bici urbana"`
- **AND** the operator adds a vehicle with that vehicle type identifier and an unknown station identifier
- **THEN** the system rejects the request
- **AND** the vehicle list remains empty

### Requirement: Operator can list vehicles

The system SHALL return every vehicle with its identifier, vehicle type identifier, parked station identifier, and availability.

#### Scenario: List after one add

- **WHEN** the operator adds one parked vehicle
- **AND** the operator requests the vehicle list
- **THEN** the response includes exactly one entry with the same vehicle type identifier, parked station identifier, and `available` true

### Requirement: Operator can get a vehicle by identifier

The system SHALL return one vehicle by identifier or report that it does not exist.

#### Scenario: Get existing vehicle

- **WHEN** a parked vehicle exists
- **AND** the operator requests it by its identifier
- **THEN** the response includes its vehicle type identifier, parked station identifier, and `available` true

### Requirement: Operator can update a parked vehicle

The system SHALL update an existing vehicle's vehicle type and/or parked station when the operator supplies at least one of those fields and both referenced entities exist.

#### Scenario: Update parked station preserves type

- **WHEN** a vehicle exists parked at a station named `"Centro"` with a type named `"Bici urbana"`
- **AND** another station exists with name `"Norte"`
- **AND** the operator sets the parked station to `"Norte"`
- **THEN** the vehicle keeps the same vehicle type identifier
- **AND** the parked station identifier matches `"Norte"`
- **AND** `available` remains true

#### Scenario: Update vehicle type preserves parked station

- **WHEN** a vehicle exists parked at `"Centro"` with type `"Bici urbana"`
- **AND** another type exists with name `"Monopatín"`
- **AND** the operator sets the vehicle type to `"Monopatín"`
- **THEN** the parked station identifier still matches `"Centro"`
- **AND** the vehicle type identifier matches `"Monopatín"`

### Requirement: Unknown vehicle type or station on update is rejected

The system SHALL reject a vehicle update when a supplied vehicle type identifier or station identifier does not exist.

#### Scenario: Reject update with unknown station

- **WHEN** a parked vehicle exists
- **AND** the operator sets the parked station to an unknown station identifier
- **THEN** the system rejects the request
- **AND** the vehicle's parked station and type are unchanged

### Requirement: Operator can delete a vehicle

The system SHALL remove a vehicle from the fleet when the operator deletes it.

#### Scenario: Delete existing vehicle

- **WHEN** a parked vehicle exists
- **AND** the operator deletes the vehicle
- **THEN** the vehicle no longer appears in the vehicle list

### Requirement: Available means parked for fleet reads

The system SHALL expose `available` as true when the vehicle is parked at a station and false when it is not parked.

#### Scenario: Parked vehicle is available

- **WHEN** the operator adds a parked vehicle through this capability
- **THEN** every read of that vehicle shows `available` true

### Requirement: Parking does not use station capacity as a gate

The system SHALL NOT reject adding or moving a vehicle because the parked count at a station would exceed the station's stored capacity.

#### Scenario: Park when stored capacity is already exceeded

- **WHEN** a station exists with name `"Centro"` and stored capacity `1`
- **AND** one vehicle is already parked at `"Centro"`
- **AND** the operator adds another vehicle parked at `"Centro"`
- **THEN** the system stores the second vehicle parked at `"Centro"`

### Requirement: Fleet backs vehicle type delete usage

The system SHALL report a vehicle type as in use when at least one vehicle references that vehicle type.

#### Scenario: Type delete refused when a vehicle uses the type

- **WHEN** a vehicle type exists with name `"Bici urbana"`
- **AND** a vehicle exists with that vehicle type
- **AND** the operator attempts to delete the vehicle type
- **THEN** the system rejects the delete
- **AND** the vehicle type remains in the vehicle type list

#### Scenario: Type delete succeeds when no vehicle uses the type

- **WHEN** a vehicle type exists with name `"Bici urbana"`
- **AND** no vehicle references that vehicle type
- **AND** the operator deletes the vehicle type
- **THEN** the vehicle type no longer appears in the vehicle type list

### Requirement: Fleet backs station delete usage

The system SHALL report a station as in use when at least one vehicle is parked at that station.

#### Scenario: Station delete refused when a vehicle is parked there

- **WHEN** a station exists with name `"Centro"`
- **AND** a vehicle is parked at `"Centro"`
- **AND** the operator attempts to delete the station
- **THEN** the system rejects the delete
- **AND** the station remains in the station list with unchanged name, capacity, and location

#### Scenario: Station delete succeeds when no vehicle is parked there

- **WHEN** a station exists with name `"Centro"`
- **AND** no vehicle is parked at `"Centro"`
- **AND** the operator deletes the station
- **THEN** the station no longer appears in the station list
