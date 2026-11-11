from decimal import Decimal

TANDIL_URBAN_SOUTH = Decimal("-37.39785")
TANDIL_URBAN_NORTH = Decimal("-37.25939")
TANDIL_URBAN_WEST = Decimal("-59.22210")
TANDIL_URBAN_EAST = Decimal("-59.04832")


def _to_decimal(value: Decimal | float | str) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))


def is_inside_tandil_urban(latitude: Decimal | float | str, longitude: Decimal | float | str) -> bool:
    lat = _to_decimal(latitude)
    lon = _to_decimal(longitude)
    return (
        TANDIL_URBAN_SOUTH <= lat <= TANDIL_URBAN_NORTH
        and TANDIL_URBAN_WEST <= lon <= TANDIL_URBAN_EAST
    )
