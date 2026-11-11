# database-migrations Specification

## Purpose
Ensures the PostgreSQL schema is applied through versioned Alembic revisions so the database can evolve safely as new capabilities add tables and constraints.

## Requirements

### Requirement: Docker API starts only after migrations reach head

The system SHALL apply all pending Alembic revisions to the configured PostgreSQL database before the API serves HTTP traffic in the Docker `api` service.

#### Scenario: Fresh database gets vehicle_type table

- **WHEN** PostgreSQL is empty and the `api` container starts with `DATABASE_URL` pointing at that database
- **THEN** Alembic records revision at head
- **AND** the `vehicle_type` table exists with columns for identifier, name, and current rate

#### Scenario: API accepts writes after migrate

- **WHEN** the `api` container has finished startup against a migrated database
- **AND** the operator posts a vehicle type with name `"Bici urbana"` and rate `150`
- **THEN** the response is success and the row is stored in `vehicle_type`

### Requirement: Schema changes are delivered as Alembic revisions

The system SHALL introduce or alter PostgreSQL tables only by adding Alembic revision files under version control, not by calling `create_all` during API startup when `DATABASE_URL` is PostgreSQL.

#### Scenario: No create_all on PostgreSQL startup

- **WHEN** the API application lifespan runs with a PostgreSQL `DATABASE_URL`
- **THEN** the system does not call `SQLModel.metadata.create_all` against that database
