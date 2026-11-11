# Spec Delta

## ADDED Requirements

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
