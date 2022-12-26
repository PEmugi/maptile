# coding: utf-8

import pytest

from maptileindex.quadkey import InvalidQuadKey, quadkey2xy, xy2quadkey


@pytest.mark.parametrize(
    "quadkey, expected_x, expected_y, expected_zoom",
    [
        ("0", 0, 0, 1),
        ("31", 3, 2, 2),
        ("030", 2, 2, 3),
        ("201", 1, 4, 3),
        ("332", 6, 7, 3),
        ("1202102332221212", 35210, 21493, 16),
    ],
)
def test_quadkey_to_tileindex(quadkey: str, expected_x: int, expected_y: int, expected_zoom: int):
    x, y, zoom = quadkey2xy(quadkey)

    assert (x, y, zoom) == (expected_x, expected_y, expected_zoom)


def test_quadkey_to_tileindex_invalid_key():
    with pytest.raises(InvalidQuadKey):
        quadkey2xy("3205")


@pytest.mark.parametrize("x, y, zoom, expected_quadkey", [(0, 2, 3, "020"), (35210, 21493, 16, "1202102332221212")])
def test_tileindex_to_quadkey(x: int, y: int, zoom: int, expected_quadkey):
    quadkey = xy2quadkey(x, y, zoom)
    assert quadkey == expected_quadkey
