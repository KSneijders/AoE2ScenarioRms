from __future__ import annotations

from typing import Tuple

from AoE2ScenarioParser.objects.support.tile import Tile


class TileUtil:
    _relative_adjacent = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    @staticmethod
    def adjacent(x: int | Tile, y: int | None = None):
        tx, ty = TileUtil.coords(x, y)
        return [Tile(tx + x, ty + y) for x, y in TileUtil._relative_adjacent]

    @staticmethod
    def coords(x: int | Tile, y: int | None = None) -> Tuple[int, int]:
        if isinstance(x, Tile):
            return x
        return x, y
