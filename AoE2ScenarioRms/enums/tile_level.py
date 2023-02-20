from __future__ import annotations

from enum import IntEnum


class TileLevel(IntEnum):
    NONE = 0
    RES = 30
    TERRAIN = 50
    TEMP = 9998
    ALL = 9999
