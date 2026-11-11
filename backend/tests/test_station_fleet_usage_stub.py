from uuid import uuid4

from app.ports.station_fleet_usage import StubStationFleetUsage


def test_stub_station_fleet_reports_no_vehicles():
    stub = StubStationFleetUsage()
    assert stub.has_vehicles_at_station(uuid4()) is False
