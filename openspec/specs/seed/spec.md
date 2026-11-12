# seed Specification

## Purpose
Loads a one-shot demo network for Tandil—five landmark stations, vehicle types, fifty vehicles, and open rentals—so the map and operator can work against realistic data on an empty database.

## Requirements

### Requirement: Operator can seed an empty database

The system SHALL populate the demo network when no station, vehicle, vehicle type, or rental exists, and SHALL reject seed when any of those already exist.

#### Scenario: Seed succeeds on empty database

- **WHEN** the database has no stations, vehicles, vehicle types, or rentals
- **AND** the operator requests seed
- **THEN** the system creates the demo network
- **AND** the response reports five stations, four vehicle types, fifty vehicles, and five open rentals

#### Scenario: Seed rejected when network is not empty

- **WHEN** at least one station exists in the database
- **AND** the operator requests seed
- **THEN** the system rejects the request
- **AND** the station count remains unchanged

### Requirement: Seed creates five landmark stations in Tandil

The system SHALL create exactly five stations using the versioned landmark catalog with names and coordinates inside the Tandil urban bounding box.

#### Scenario: Landmark stations are stored

- **WHEN** the operator seeds an empty database
- **THEN** the station list includes `"Plaza Independencia"`, `"Parque Independencia"`, `"Terminal de Ómnibus"`, `"Cerro El Divisorio"`, and `"UNCPBA"`
- **AND** each station's latitude and longitude match the landmark catalog values

### Requirement: Seed creates demo vehicle types when missing

The system SHALL create four demo vehicle types with per-minute rates when the vehicle type catalog is empty as part of seed.

#### Scenario: Demo types appear after seed

- **WHEN** the vehicle type catalog is empty
- **AND** the operator seeds an empty database
- **THEN** the vehicle type list includes `"Bici urbana"`, `"Monopatín"`, `"Bici eléctrica"`, and `"Moto eléctrica"`

### Requirement: Seed creates fifty parked vehicles with pseudo-random assignment

The system SHALL create fifty vehicles, each assigned a vehicle type and parked station drawn from the seeded catalogs using the fixed internal RNG seed `42`.

#### Scenario: Fifty vehicles after seed

- **WHEN** the operator seeds an empty database
- **THEN** the vehicle list length is fifty
- **AND** forty-five vehicles show `available` true
- **AND** repeating seed on a fresh empty database with the same implementation version assigns the same type and station to the vehicle at index `0`

### Requirement: Seed places five vehicles on open rentals

The system SHALL leave exactly five vehicles out on open rentals with `started_at` in the past and `available` false.

#### Scenario: Open rentals reduce availability

- **WHEN** the operator seeds an empty database
- **THEN** exactly five rentals are open
- **AND** exactly five vehicles show `available` false
- **AND** each open rental has a `started_at` before the seed operation time

### Requirement: Open rental checkout stations come from seeded stations

The system SHALL set each open rental's checkout station to one of the five seeded stations.

#### Scenario: Open rental references a seeded station

- **WHEN** the operator seeds an empty database
- **AND** the operator requests the rental list
- **THEN** every open rental's checkout station identifier matches one of the five seeded stations
