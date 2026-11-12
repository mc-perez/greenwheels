from app.schemas.map import MapAvailabilityByType, MapStationRead, MapStationsResponse


def test_map_schema_imports():
    assert MapStationsResponse is not None
    assert MapStationRead is not None
    assert MapAvailabilityByType is not None
