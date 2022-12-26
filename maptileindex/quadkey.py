# coding: utf-8

from typing import Tuple


class InvalidQuadKey(Exception):
    pass


def quadkey2xy(quadkey: str) -> Tuple[int, int, int]:
    """QuadKey to Tile x, y and zoom level

    Args:
        quadkey (str): QuadKey

    Raises:
        InvalidTileException: Invalid QuadKey digit sequence.

    Returns:
        Tuple[int, int, int]: (tile x, tile y, zoom level)
    """

    zoom = len(quadkey)
    x = y = 0
    for i in range(zoom, 0, -1):
        mask = 1 << (i - 1)
        target_key = quadkey[zoom - i]
        if target_key == "0":
            continue
        elif target_key == "1":
            x |= mask
        elif target_key == "2":
            y |= mask
        elif target_key == "3":
            x |= mask
            y |= mask
        else:
            raise InvalidQuadKey("Invalid QuadKey digit sequence.")

    return x, y, zoom


def xy2quadkey(x: int, y: int, zoom: int) -> str:
    """Tile x, y and zoom to QuadKey

    Args:
        x (int): Tile x
        y (int): Tile y
        zoom (int): Zoom level

    Returns:
        str: QuadKey
    """

    quadkey: list[str] = []
    for i in range(zoom, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if x & mask != 0:
            digit += 1
        if y & mask != 0:
            digit += 1
            digit += 1
        quadkey.append(str(digit))

    return "".join(quadkey)
