# Spec Delta

## ADDED Requirements

### Requirement: Current rate is per minute for rental billing

The system SHALL treat `current_rate` as the price per minute of time out, copied at rental checkout into `rate_at_checkout`.

#### Scenario: Checkout uses type rate as per-minute price

- **WHEN** a vehicle type has current rate `150`
- **AND** the operator checks out a parked vehicle of that type
- **THEN** the open rental has `rate_at_checkout` `150`
