from dataclasses import dataclass
from decimal import Decimal

from app.geo.tandil import is_inside_tandil_urban

DEMO_VEHICLE_TYPE_RATES: tuple[tuple[str, int], ...] = (
    ("Bici urbana", 150),
    ("Monopatín", 220),
    ("Bici eléctrica", 180),
    ("Moto eléctrica", 300),
)


@dataclass(frozen=True, slots=True)
class TandilLandmark:
    name: str
    capacity: int
    latitude: Decimal
    longitude: Decimal


TANDIL_LANDMARKS: tuple[TandilLandmark, ...] = (
    TandilLandmark(
        "Plaza Independencia",
        25,
        Decimal("-37.32140"),
        Decimal("-59.13310"),
    ),
    TandilLandmark(
        "Parque Independencia",
        20,
        Decimal("-37.32500"),
        Decimal("-59.12800"),
    ),
    TandilLandmark(
        "Terminal de Ómnibus",
        30,
        Decimal("-37.32850"),
        Decimal("-59.14500"),
    ),
    TandilLandmark(
        "Cerro El Divisorio",
        15,
        Decimal("-37.31500"),
        Decimal("-59.11800"),
    ),
    TandilLandmark(
        "UNCPBA",
        20,
        Decimal("-37.33900"),
        Decimal("-59.10500"),
    ),
)


def all_landmarks_inside_urban_bbox() -> bool:
    return all(
        is_inside_tandil_urban(landmark.latitude, landmark.longitude)
        for landmark in TANDIL_LANDMARKS
    )
