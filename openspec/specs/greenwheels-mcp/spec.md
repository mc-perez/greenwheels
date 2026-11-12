# greenwheels-mcp Specification

## Purpose
Provides a stdio MCP server so AI hosts (Cursor, OpenCode) can invoke GreenWheels operator REST endpoints through named tools without changing API business rules.

## Requirements

### Requirement: MCP server uses configurable API base URL

The system SHALL read `GREENWHEELS_API_URL` for HTTP requests and SHALL default to `http://localhost:8000` when unset.

#### Scenario: Default base URL

- **WHEN** the MCP server starts without `GREENWHEELS_API_URL`
- **AND** a tool calls `list_stations`
- **THEN** the client requests `GET http://localhost:8000/api/v1/stations`

### Requirement: MCP exposes read and rental tools in phase one

The system SHALL register MCP tools for health, map stations, listing vehicle types, stations, vehicles, and rentals, getting one rental by identifier, checkout, return, and record payment, each performing the corresponding REST call documented in the project README.

#### Scenario: List stations via tool

- **WHEN** the API returns two stations named `"Centro"` and `"Plaza Independencia"`
- **AND** an agent invokes `list_stations`
- **THEN** the tool response includes both station names

#### Scenario: Checkout via tool

- **WHEN** a vehicle with identifier `V1` is parked and has no open rental
- **AND** an agent invokes `checkout_rental` with `vehicle_id` `V1`
- **THEN** the tool calls `POST /api/v1/rentals/checkout` with body `{"vehicle_id": "V1"}`
- **AND** the response includes an open rental for vehicle `V1`

#### Scenario: Return via tool

- **WHEN** an open rental with identifier `R1` exists
- **AND** a station with identifier `S1` named `"Centro"` exists
- **AND** an agent invokes `return_rental` with `rental_id` `R1` and `station_id` `S1`
- **THEN** the tool calls `POST /api/v1/rentals/R1/return` with `station_id` `S1`
- **AND** the response shows the rental closed with return station at `S1`

#### Scenario: Record payment via tool

- **WHEN** a closed rental `R2` has `amount_owed` `300` and `paid` false
- **AND** an agent invokes `record_rental_payment` with `rental_id` `R2`
- **THEN** the tool calls `POST /api/v1/rentals/R2/record-payment`
- **AND** the response shows `paid` true

### Requirement: MCP exposes catalog mutation tools in phase two

The system SHALL register MCP tools to create, update, and delete vehicle types, stations, and vehicles, and to seed an empty network, each mapping to the existing REST routes.

#### Scenario: Create vehicle type via tool

- **WHEN** an agent invokes `create_vehicle_type` with name `"Bici urbana"` and `current_rate` `150`
- **THEN** the tool calls `POST /api/v1/vehicle-types` with those fields
- **AND** the response includes name `"Bici urbana"` and `current_rate` `150`

#### Scenario: Delete type in use surfaces API error

- **WHEN** a vehicle references type `"Monopatín"`
- **AND** an agent invokes `delete_vehicle_type` for that type's identifier
- **THEN** the tool reports the API rejection
- **AND** the type still exists on a subsequent `list_vehicle_types`

#### Scenario: Seed empty database via tool

- **WHEN** the database has no stations
- **AND** an agent invokes `seed_network`
- **THEN** the tool calls `POST /api/v1/seed` with success status
- **AND** `list_stations` returns five landmark stations

#### Scenario: Seed rejected when network exists

- **WHEN** at least one station already exists
- **AND** an agent invokes `seed_network`
- **THEN** the tool reports the API `409` response
- **AND** no duplicate seed data is implied in the tool message

### Requirement: MCP tools report API errors readably

The system SHALL surface FastAPI `detail` (or connection failures) as tool errors without dumping raw stack traces to the agent.

#### Scenario: Validation error from station create

- **WHEN** an agent invokes `create_station` with coordinates outside the Tandil urban rules
- **THEN** the tool error text includes the API validation message
- **AND** `list_stations` is unchanged

### Requirement: MCP is documented for Cursor and OpenCode stdio

The project SHALL document one local launch command and environment for Cursor MCP settings and for OpenCode `mcp.servers` with `type` `local`, using the same entrypoint.

#### Scenario: OpenCode local server configuration

- **WHEN** the operator copies the documented `opencode.jsonc` example with `GREENWHEELS_API_URL` `http://localhost:8000`
- **AND** runs `opencode mcp list`
- **THEN** the greenwheels server is shown as connected when the API is reachable
