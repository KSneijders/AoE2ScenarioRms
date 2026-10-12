from __future__ import annotations

import random
from typing import List

from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile

from AoE2ScenarioRms.util.tile_util import TileUtil


class GridMap:
    def __init__(self, map_size: int, default_availability: bool = True) -> None:
        """
        Class that manages the state of a map. Used for marking tiles on a scenario for creation of potential group
        spawns.

        Args:
            map_size: The size of the map to manage
            default_availability: The starting state of all tiles
        """
        self.map_size: int = map_size
        self.grid_map: List[List[bool]] = []

        self._base_availability: bool = default_availability
        self._area: Area = Area(map_size=map_size)
        self.set_all(default_availability)

    def available_tiles(self, size: int = 1, shuffle: bool = False) -> List[Tile]:
        """
        Get all tiles available for resource spawning. Can be shuffled if necessary

        Args:
            size: The size of the object
            shuffle: If the resulting array should be returned shuffled or not

        Returns:
            A (shuffled) list of ``Tile`` objects that indicate which tiles are valid for spawn attempts for groups
        """
        tiles = []
        for y in range(self.map_size):
            for x in range(self.map_size):
                tile = Tile(x, y)
                if self.is_available_size(size, tile):
                    tiles.append(tile)
        if shuffle:
            random.shuffle(tiles)
        return tiles

    def is_available_size(self, size: int, tile: Tile) -> bool:
        """Check if a tile and tiles around it are available within a given size"""
        tile = TileUtil.coords(tile)
        if size == 1:
            return self.is_available(tile)

        area = self._area.select(*tile).size(size)
        if not area.is_within_bounds():
            return False

        tile: Tile
        for tile in area.to_coords():
            if self.is_blocked(tile):
                return False
        return True

    def invert(self) -> GridMap:
        """
        Invert the gridmap inline

        Returns:
            The current instance, so this it can be chained if necessary
        """
        for y in range(self.map_size):
            for x in range(self.map_size):
                tile = Tile(x, y)
                self.set(tile, not self.is_available(tile))
        return self

    def set(self, tile: Tile, availability: bool) -> None:
        """Set a coordinate's availability"""
        self.grid_map[tile.y][tile.x] = availability

    def reset(self, tile: Tile) -> None:
        """Reset a coordinate's availability to the base availability"""
        self.set(tile, self._base_availability)

    def set_all(self, availability: bool) -> None:
        """Set all coordinates to the same availability and override the base availability to that"""
        self._base_availability: bool = availability
        self.grid_map = [[availability] * self.map_size for _ in range(self.map_size)]

    def is_available(self, tile: Tile) -> bool:
        """If a given tile is available for group spawning"""
        is_within_map = 0 <= tile.x < self.map_size and 0 <= tile.y < self.map_size
        return is_within_map and self.grid_map[tile.y][tile.x]

    def is_blocked(self, tile: Tile) -> bool:
        """Inverse of ``is_available(...)``. If a given tile is NOT available for group spawning"""
        return not self.is_available(tile)
