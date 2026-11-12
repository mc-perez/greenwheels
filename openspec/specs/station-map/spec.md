# station-map Specification

## Purpose
Delivers the operator's first screen: an OpenStreetMap of Tandil with system station markers and per-type availability on selection, backed by a dedicated map read API.

## Requirements

### Requirement: Operator can load map stations

The system SHALL expose a read-only map payload listing every station with its identifier, name, stored capacity, latitude, longitude, and availability by vehicle type.

#### Scenario: Empty network returns no stations

- **WHEN** the database has no stations
- **AND** the operator requests the map station list
- **THEN** the response includes an empty station list

#### Scenario: Seeded network returns five landmarks

- **WHEN** the operator has seeded an empty database
- **AND** the operator requests the map station list
- **THEN** the response includes five stations named `"Plaza Independencia"`, `"Parque Independencia"`, `"Terminal de Ómnibus"`, `"Cerro El Divisorio"`, and `"UNCPBA"`
- **AND** each station's latitude and longitude match the stored station record

### Requirement: Available count follows fleet availability

The system SHALL count a vehicle toward a station's available count only when the vehicle is parked at that station (the same rule as fleet `available` true).

#### Scenario: Parked vehicles increase available count

- **WHEN** a station named `"Centro"` exists with identifier `S1`
- **AND** vehicle type `"Bici urbana"` exists with identifier `T1`
- **AND** two vehicles of type `T1` are parked at `S1`
- **AND** the operator requests the map station list
- **THEN** the entry for `S1` shows `available_count` `2` for type `T1`

#### Scenario: Vehicle out on open rental is excluded

- **WHEN** a station named `"Centro"` exists with identifier `S1`
- **AND** a vehicle of type `"Monopatín"` is parked at `S1`
- **AND** another vehicle of the same type is out on an open rental with no parked station
- **AND** the operator requests the map station list
- **THEN** the entry for `S1` shows `available_count` `1` for `"Monopatín"`

### Requirement: Map lists every vehicle type per station

The system SHALL include every vehicle type in the operator catalog in each station's availability list and SHALL report `available_count` `0` when no parked vehicle of that type exists at the station.

#### Scenario: Missing type appears with zero

- **WHEN** vehicle types `"Bici urbana"` and `"Monopatín"` exist
- **AND** a station named `"Centro"` has only `"Bici urbana"` vehicles parked
- **AND** the operator requests the map station list
- **THEN** the entry for `"Centro"` includes `"Monopatín"` with `available_count` `0`

### Requirement: Station capacity is not an occupancy gate on counts

The system SHALL compute availability from parked vehicles only and SHALL NOT cap or hide counts based on stored station capacity.

#### Scenario: Count exceeds stored capacity

- **WHEN** a station named `"Centro"` has stored capacity `1`
- **AND** two vehicles are parked at `"Centro"`
- **AND** the operator requests the map station list
- **THEN** the entry for `"Centro"` shows stored capacity `1`
- **AND** the summed `available_count` across types is `2`

### Requirement: Map client shows OpenStreetMap without credentials

The map client SHALL render an OpenStreetMap basemap using public tile access and SHALL NOT require a map provider API key or operator account.

#### Scenario: Basemap loads for operator

- **WHEN** the operator opens the map application with network access to public OpenStreetMap tiles
- **THEN** a map of Tandil is visible without entering credentials

### Requirement: Map client loads station data once on open

The map client SHALL request the map station list when the application opens and SHALL use that response for markers and selection panels without requesting the map station list again on each station selection.

#### Scenario: Single map request on startup

- **WHEN** the operator opens the map application
- **THEN** the client performs one request to the map station list endpoint before showing station markers

### Requirement: Map client places markers at system coordinates

The map client SHALL draw one marker per station returned by the map station list at that station's latitude and longitude.

#### Scenario: Marker matches API coordinates

- **WHEN** the map station list includes a station named `"Plaza Independencia"` at latitude `-37.32140` and longitude `-59.13310`
- **AND** the operator opens the map application
- **THEN** a marker is shown at `-37.32140`, `-59.13310`

### Requirement: Map client fits view to all stations

When at least one station is returned, the map client SHALL adjust the initial map view so every station marker is visible with padding.

#### Scenario: All seeded markers visible

- **WHEN** the operator opens the map application after seed
- **THEN** all five station markers are visible in the initial view

### Requirement: Map client handles an empty station list

When the map station list is empty, the map client SHALL still show the basemap and SHALL show a clear message that no stations exist.

#### Scenario: No stations message

- **WHEN** the map station list is empty
- **AND** the operator opens the map application
- **THEN** no station markers are shown
- **AND** the operator sees text indicating that no stations exist

### Requirement: Map client shows capacity and availability on selection

When the operator selects a station marker, the map client SHALL show the station name, stored capacity, and each vehicle type name with its `available_count` from the loaded map data.

#### Scenario: Selection panel content

- **WHEN** the operator selects a station named `"Centro"` with capacity `25`
- **AND** the loaded map data shows `"Bici urbana"` with `available_count` `3` and `"Monopatín"` with `available_count` `0` at that station
- **THEN** the panel shows name `"Centro"`, capacity `25`, `"Bici urbana"` `3`, and `"Monopatín"` `0`
