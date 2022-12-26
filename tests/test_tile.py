# coding: utf-8


import pytest

from maptileindex.tile import Tile, xy2lonlat


class TestTile:
    def test_to_wkt(self):
        tile = Tile(0, 0, 1)
        assert (
            "POLYGON ((-180.0 0.0, -180.0 85.0511287798066, 0.0 85.0511287798066, 0.0 0.0, -180.0 0.0))"
            == tile.to_wkt()
        )

    def test_children(self):
        tile = Tile(0, 0, 1)

        expected_tiles = []
        for i in range(0, 4):
            for j in range(0, 4):
                expected_tiles.append(Tile(i, j, 3).quadkey)

        assert sorted(expected_tiles) == sorted([t.quadkey for t in tile.children(3)])

    def test_difference(self):
        tile = Tile.from_quadkey("012")
        expected_quadkey = []
        for y in range(1, 4):
            for x in range(2, 4):
                expected_quadkey.append(Tile(x, y, 3).quadkey)

        assert expected_quadkey == [t.quadkey for t in tile.difference(Tile.from_quadkey("033"))]


@pytest.mark.parametrize(
    "x, y, zoom, expected_lon, expected_lat", [(7, 7, 3, 135.0, -79.171334), (0, 0, 20, -180, 85.0511287798066)]
)
def test_xy2lonlat(x: int, y: int, zoom: int, expected_lon: float, expected_lat: float):
    assert pytest.approx((expected_lon, expected_lat), abs=1e-6) == xy2lonlat(x, y, zoom)
