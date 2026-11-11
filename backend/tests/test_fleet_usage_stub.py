from uuid import uuid4

from app.ports.fleet_usage import StubFleetUsage


def test_stub_fleet_usage_reports_unused():
    stub = StubFleetUsage()
    assert stub.is_type_in_use(uuid4()) is False
