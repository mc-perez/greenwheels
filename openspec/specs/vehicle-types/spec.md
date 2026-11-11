# vehicle-types Specification

## Purpose
Maintains the operator's catalog of vehicle types, each with a display name and a current rate used when future rentals copy pricing at checkout.

## Requirements

### Requirement: Operator can add a vehicle type

The system SHALL create a vehicle type from a non-empty name and a non-negative rate.

#### Scenario: Add type with name and rate

- **WHEN** the operator adds a vehicle type with name `"Bici urbana"` and rate `150`
- **THEN** the system stores the type and exposes name `"Bici urbana"` and current rate `150`

### Requirement: Operator can list vehicle types

The system SHALL return every vehicle type with its identifier, name, and current rate.

#### Scenario: List after one add

- **WHEN** the operator adds a vehicle type with name `"Monopatín"` and rate `220`
- **AND** the operator requests the vehicle type list
- **THEN** the response includes one entry with name `"Monopatín"` and current rate `220`

### Requirement: Operator can rename a vehicle type

The system SHALL update only the name of an existing vehicle type when the operator renames it.

#### Scenario: Rename preserves rate

- **WHEN** a vehicle type exists with name `"Bici urbana"` and current rate `150`
- **AND** the operator renames it to `"Bici tradicional"`
- **THEN** the type has name `"Bici tradicional"` and current rate `150`

### Requirement: Operator can change a type's current rate

The system SHALL replace the stored current rate when the operator updates the rate.

#### Scenario: Rate update changes stored current rate

- **WHEN** a vehicle type exists with name `"Bici urbana"` and current rate `150`
- **AND** the operator sets the current rate to `180`
- **THEN** the type's current rate is `180`

### Requirement: Operator can delete an unused vehicle type

The system SHALL remove a vehicle type when no vehicle references it.

#### Scenario: Delete when fleet reports no usage

- **WHEN** a vehicle type exists with name `"Bici urbana"`
- **AND** the fleet reports zero vehicles referencing that type
- **AND** the operator deletes the type
- **THEN** the type no longer appears in the vehicle type list

### Requirement: Delete is refused while a vehicle uses the type

The system SHALL reject deletion when the fleet reports at least one vehicle referencing the type.

#### Scenario: Delete refused when fleet reports usage

- **WHEN** a vehicle type exists with name `"Bici urbana"`
- **AND** the fleet reports one or more vehicles referencing that type
- **AND** the operator attempts to delete the type
- **THEN** the system rejects the delete
- **AND** the type remains in the vehicle type list with unchanged name and current rate

### Requirement: Vehicle type names are unique

The system SHALL reject a create or name update that would duplicate another vehicle type's name.

#### Scenario: Reject add with duplicate type name

- **WHEN** a vehicle type exists with name `"Bici urbana"` and current rate `150`
- **AND** the operator adds a vehicle type with name `"Bici urbana"` and rate `200`
- **THEN** the system rejects the request
- **AND** exactly one vehicle type named `"Bici urbana"` appears in the vehicle type list with current rate `150`

#### Scenario: Reject rename to another type's name

- **WHEN** vehicle types exist with names `"Bici urbana"` and `"Monopatín"`
- **AND** the operator renames `"Monopatín"` to `"Bici urbana"`
- **THEN** the system rejects the rename
- **AND** the vehicle type list still includes one `"Bici urbana"` and one `"Monopatín"`
