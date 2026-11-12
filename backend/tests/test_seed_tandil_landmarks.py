from decimal import Decimal

from app.geo.tandil import is_inside_tandil_urban
from app.seed.tandil_landmarks import (
    DEMO_VEHICLE_TYPE_RATES,
    TANDIL_LANDMARKS,
    all_landmarks_inside_urban_bbox,
)


def test_all_landmarks_inside_tandil_urban_bbox():
    assert all_landmarks_inside_urban_bbox()


def test_landmark_coordinates_match_catalog():
    expected = {
        "Plaza Independencia": (Decimal("-37.32140"), Decimal("-59.13310")),
        "Parque Independencia": (Decimal("-37.32500"), Decimal("-59.12800")),
        "Terminal de Ómnibus": (Decimal("-37.32850"), Decimal("-59.14500")),
        "Cerro El Divisorio": (Decimal("-37.31500"), Decimal("-59.11800")),
        "UNCPBA": (Decimal("-37.33900"), Decimal("-59.10500")),
    }
    for landmark in TANDIL_LANDMARKS:
        lat, lon = expected[landmark.name]
        assert landmark.latitude == lat
        assert landmark.longitude == lon
        assert is_inside_tandil_urban(landmark.latitude, landmark.longitude)


def test_demo_vehicle_type_catalog_has_four_entries():
    names = {name for name, _rate in DEMO_VEHICLE_TYPE_RATES}
    assert names == {
        "Bici urbana",
        "Monopatín",
        "Bici eléctrica",
        "Moto eléctrica",
    }
