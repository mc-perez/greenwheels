# Requirements

Constitution for GreenWheels capabilities. Capabilities **1–6** were the original OpenSpec sequence (one capability, one change, in that order). **7+** extend the product; their WHEN/THEN detail lives in each change's delta spec and in `openspec/specs/`, not here.

Local vehicle-rental system for one city. Learning project. The person running the app is the only user.

## Intent

- Outcome: one operator's data for Tandil — stations, vehicle types, vehicles, and rentals. The default screen is an OpenStreetMap of the city; the operator also uses a browser console for catalogs and rentals. No key, no account.
- User: the person running the app. A public rider on the web or a phone is a later client of the same rules, not a v1 user.
- Success: the system holds the network and a full rental. The seed is 5 stations on real places in Tandil and 50 vehicles. The map shows the stations, and a click shows how many vehicles of each type are available there.
- Constraint: one city, one local user, no login. The rules must still hold when a public client arrives.
- Constraint: The system builds and runs on Windows, Linux, and macOS.
- Constraint: The PostgreSQL schema is versioned and applied with Alembic migrations. Runtime does not create or alter production tables with ad-hoc `create_all` when serving the API in Docker.

## Out of scope

Authentication, a public client, card charging, GPS tracking, dock hardware, a capacity that blocks a return, and Google Maps.

Backend, database, and frontend are how a capability is built. They are not capabilities, and they are not decided here.

## Capabilities

1. **Vehicle types.** An operator catalog: add and rename. Delete is refused while a vehicle uses the type. Each type has a rate, and a rate change applies to future checkouts only.
2. **Stations.** A station has a name, a capacity, and a location on a real place in Tandil. Capacity is a fact, not a gate.
3. **Fleet.** A vehicle has one type. It is parked at a station, or out on a rental. Available means parked.
4. **Rental.** Checkout is legal when the vehicle is parked and has no open rental, and it copies the type's current rate. Return is to any station, including a full one. The amount owed is the copied rate times how long the vehicle was out. The operator records that it was paid. No card charge; business rules are enforced on the API whether the caller is Swagger or the operator console.
5. **Seed.** Five stations taken from real places in Tandil, not invented coordinates. Fifty vehicles, each with a random type and a random station. A few are out on an open rental, with a random station and start time, so the available count is not the whole fleet.
6. **Station map.** OpenStreetMap, no key and no account. It reads stations from the system and draws them. A click shows available counts by type. The station data is the system's.
7. **Operator console.** Same React app as the map; navigation to catalog views (vehicle types, stations, fleet) and rental actions (checkout, return, record payment) by calling the existing REST API. No new backend rules for v1 catalogs and rentals.
