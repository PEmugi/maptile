# coding: utf-8

import itertools
import math
from typing import Tuple

from maptileindex.quadkey import quadkey2xy, xy2quadkey


class ZoomLevelNotMatch(Exception):
    pass


class Tile:
    def __init__(self, x: int, y: int, zoom: int) -> None:
        self.x: int = x
        self.y: int = y
        self.zoom: int = zoom
        self.quadkey = xy2quadkey(x, y, zoom)

    def index(self) -> Tuple[int, int, int]:
        """x, y, z index

        Returns:
            Tuple[int, int, int]: (x, y, zoom)
        """

        return (self.x, self.y, self.zoom)

    def to_wkt(self) -> str:
        """Returns Well Known Text(WKT) polygon string

        Returns:
            str: WKT Polygon
        """
        minx, maxy = xy2lonlat(self.x, self.y, self.zoom)
        maxx, miny = xy2lonlat(self.x + 1, self.y + 1, self.zoom)

        return f"POLYGON (({minx} {miny}, {minx} {maxy}, {maxx} {maxy}, {maxx} {miny}, {minx} {miny}))"

    def parent(self) -> "Tile":
        """Returns the parent tile

        Returns:
            Tile: Parent tile

        Examples:
        >>> t = Tile.from_quadkey("331")
        >>> t.parent().quadkey
        '33'
        """

        return self.from_quadkey(self.quadkey[:-1])

    def children(self, level: int = 1) -> list["Tile"]:
        """Returns child tiles of a given level.

        Args:
            level (int): Zoom level

        Returns:
            list["Tile"]: child tiles
        """
        current_level = self.zoom
        if current_level >= level:
            return []

        return [
            self.from_quadkey(self.quadkey + "".join(keys))
            for keys in itertools.product("0123", repeat=level - current_level)
        ]

    def difference(self, to_tile: "Tile") -> list["Tile"]:
        """Reterns all tiles between current tile and given one.

        Args:
            to_tile (Tile): Target tile

        Raises:
            ZoomLevelNotMatch: Zoom level mismatch exception

        Returns:
            list["Tile"]: All tiles between myself and to tile.
        """

        if self.zoom != to_tile.zoom:
            raise ZoomLevelNotMatch

        minx = min([self.x, to_tile.x])
        maxx = max([self.x, to_tile.x])
        miny = min([self.y, to_tile.y])
        maxy = max([self.y, to_tile.y])

        tiles: list["Tile"] = []
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                tiles.append(Tile(x, y, self.zoom))

        return tiles

    @classmethod
    def from_quadkey(cls, quadkey: str) -> "Tile":
        """Generate Tile object from quadkey

        Args:
            quadkey (str): QuadKey

        Returns:
            Tile: Tile object

        Example:
        >>> t1 = Tile.from_quadkey("211")
        >>> t1.index()
        (3, 4, 3)
        """

        return Tile(*quadkey2xy(quadkey))

    @classmethod
    def from_lonlat(cls, lon: float, lat: float, zoom: int) -> "Tile":
        """Generate Tile object from Lon. Lat.

        Args:
            lon (float): Longitude
            lat (float): Latitude
            zoom (int): Zoom Level

        Returns:
            Tile: Tile object
        """
        return Tile(*lonlat2xy(lon, lat, zoom))


def lonlat2xy(lon: float, lat: float, zoom: int) -> Tuple[int, int, int]:
    """Lon. Lat. to tile index

    https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python

    Args:
        lon (float): Longitude(degrees)
        lat (float): Latitude(degrees)
        zoom (int): Zoom level

    Returns:
        Tuple[int, int, int]: (x, y, zoom)

    Example:
    >>> lonlat2xy(139.75605009040905, 35.6761235534871, 15)
    (29104, 12903, 15)
    """

    lat_rad = math.radians(lat)
    n = 2.0**zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x, y, zoom


def xy2lonlat(x: int, y: int, zoom) -> Tuple[float, float]:
    """Tile index to Lon. Lat.

    This returns NW corner of Tile.
    https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python

    Args:
        x (int): Tile x
        y (int): Tile y
        zoom (int): Zoom level

    Returns:
        Tuple[float, float]: (Longitude, Latitude)

    Example:
    >>> xy2lonlat(29104, 12903, 15)
    (139.74609375, 35.68407153314097)
    """

    n = 2.0**zoom
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)

    return lon_deg, lat_deg
