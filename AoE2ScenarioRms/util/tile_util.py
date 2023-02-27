from __future__ import annotations

from typing import Tuple

from AoE2ScenarioParser.objects.support.tile import Tile


class TileUtil:
    _relative_adjacent = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    @staticmethod
    def adjacent(x: int | Tile, y: int | None = None):
        """Return all tiles adjacent to the given coordinate. (non-diagonal)"""
        # Todo: Add a range param or extra function. Maybe use area for it?
        tx, ty = TileUtil.coords(x, y)
        return [Tile(tx + x, ty + y) for x, y in TileUtil._relative_adjacent]

    @staticmethod
    def coords(x: int | Tile, y: int | None = None) -> Tuple[int, int]:
        """Get the coords of a tile or xy params to make them consistent in functions."""
        if isinstance(x, Tile):
            return x
        return x, y
