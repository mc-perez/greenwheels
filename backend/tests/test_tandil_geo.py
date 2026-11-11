from app.geo.tandil import (
    TANDIL_URBAN_EAST,
    TANDIL_URBAN_NORTH,
    TANDIL_URBAN_SOUTH,
    TANDIL_URBAN_WEST,
    is_inside_tandil_urban,
)


def test_boundary_corners_are_inside():
    assert is_inside_tandil_urban(TANDIL_URBAN_SOUTH, TANDIL_URBAN_WEST)
    assert is_inside_tandil_urban(TANDIL_URBAN_NORTH, TANDIL_URBAN_EAST)
    assert is_inside_tandil_urban(-37.32167, -59.13316)


def test_latitude_south_of_box_is_outside():
    assert not is_inside_tandil_urban(-37.41000, -59.13316)


def test_longitude_west_of_box_is_outside():
    assert not is_inside_tandil_urban(-37.32167, -59.23000)
