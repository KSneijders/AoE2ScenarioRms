from __future__ import annotations

import random
from typing import Tuple, List

from AoE2ScenarioParser.objects.support.tile import Tile

from AoE2ScenarioRms.enums import TileLevel


class GridMap:
    def __init__(self, map_size: int) -> None:
        self.map_size: int = map_size
        self.grid_map: List[List[TileLevel]] = []

        self.reset_all()

    def available_tiles(self, shuffle=False) -> List[Tile]:
        tiles = []
        for y in range(self.map_size):
            for x in range(self.map_size):
                if self.is_available(x, y):
                    tiles.append(Tile(x, y))
        if shuffle:
            random.shuffle(tiles)
        return tiles

    def set(self, level: TileLevel, x: int | Tile, y: int = None) -> None:
        x, y = self._coords(x, y)
        self.grid_map[y][x] = level

    def temp(self, x: int | Tile, y: int = None) -> None:
        self.set(TileLevel.TEMP, x, y)

    def reset(self, x: int | Tile, y: int = None) -> None:
        self.set(TileLevel.NONE, x, y)

    def reset_all(self) -> None:
        self.grid_map = [[TileLevel.NONE for _ in range(self.map_size)] for _ in range(self.map_size)]

    def is_available(self, x: int | Tile, y: int = None) -> bool:
        x, y = self._coords(x, y)
        return self.grid_map[y][x] == TileLevel.NONE

    def is_blocked(self, x: int | Tile, y: int = None) -> bool:
        return not self.is_available(x, y)

    def level_is_available(self, level: TileLevel, x: int | Tile, y: int = None) -> bool:
        x, y = self._coords(x, y)
        if self.grid_map[y][x] == TileLevel.TEMP:
            return True
        if level > self.grid_map[y][x]:
            return True
        return False

    def level_is_blocked(self, level: TileLevel, x: int | Tile, y: int = None) -> bool:
        return not self.level_is_available(level, x, y)

    def is_valid(self, level: TileLevel, x: int | Tile, y: int = None) -> bool:
        x, y = self._coords(x, y)
        is_within_map = 0 <= x <= self.map_size - 1 and 0 <= y <= self.map_size - 1
        return is_within_map and self.level_is_available(level, x, y)

    @staticmethod
    def _coords(x: int | Tile, y: int | None = None) -> Tuple[int, int]:
        if isinstance(x, Tile):
            return x
        return x, y
