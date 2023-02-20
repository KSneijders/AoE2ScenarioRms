from __future__ import annotations

import random
from typing import Tuple, List

from AoE2ScenarioParser.helper.printers import warn
from AoE2ScenarioParser.objects.support.tile import Tile

from AoE2ScenarioRms.util.exceptions import LocationNotFoundError
from AoE2ScenarioRms.util.warnings import SpawnFailureWarning
from AoE2ScenarioRms.enums.grouping_method import GroupingMethod
from AoE2ScenarioRms.enums.tile_level import TileLevel
from AoE2ScenarioRms.util.grid_map import GridMap


class GroupsConfig:
    def __init__(
            self,
            name: str,
            amount: int,
            grouping_method: GroupingMethod,
            group_size: int | Tuple[int, int],
            grid_map: GridMap,
            loose_grouping_distance: int = -1,
    ) -> None:
        self.name: str = name
        self.amount: int = amount
        self.grouping_method: GroupingMethod = grouping_method
        self.group_size: int | Tuple[int, int] = group_size
        self.grid_map: GridMap = grid_map
        self.loose_grouping_distance: int = loose_grouping_distance

        self.map_size = grid_map.map_size

    def resolve(self):
        tiles: List[List[Tile]] = []
        starting_tiles = self.find_random_locations(self.amount)

        failed = 0
        for starting_tile in starting_tiles:
            min_, size = self.get_random_size(self.group_size)

            group = [starting_tile]
            size -= 1

            max_failed_attempts = 50
            while size > 0 and max_failed_attempts > 0:
                nearby_tile = self.find_nearby_tile(group)

                if nearby_tile is not None:
                    group.append(nearby_tile)
                    size -= 1
                else:
                    max_failed_attempts -= 1

            if len(group) >= min_:
                tiles.append(group)
            else:
                failed += 1

        if failed and failed / self.amount > .1:
            warn(f"When generating group '{self.name}', out of the {self.amount} groups, {failed} failed. "
                 f"Consider lowering '_max_potential_group_count' for '{self.name}'", SpawnFailureWarning)

        return tiles

    def find_nearby_tile(self, group: List[Tile]):
        if self.grouping_method == GroupingMethod.TIGHT:
            return self.find_random_adjacent_tile(random.choice(group), group)
        elif self.grouping_method == GroupingMethod.LOOSE:
            return self.find_random_tile_within_range(group[0], self.loose_grouping_distance, group)
        else:
            raise ValueError(f"Unknown grouping method '{self.grouping_method}' for group '{self.name}'.")

    def find_random_adjacent_tile(self, tile: Tile, group: List[Tile]) -> Tile | None:
        rand_start = random.randrange(0, 4)
        coords = [(0, -1), (-1, 0), (0, 1), (1, 0)]

        for i in range(4):
            x, y = coords[(rand_start + i) % 4]

            new_tile = Tile(tile.x + x, tile.y + y)
            if new_tile not in group and self.grid_map.is_valid(TileLevel.RES, new_tile):
                return new_tile
        return None

    def find_random_tile_within_range(self, tile: Tile, range_: int, group: List[Tile]) -> Tile | None:
        x_offset = random.randrange(-range_, range_)
        y_offset = random.randrange(-range_, range_)

        new_tile = Tile(tile.x + x_offset, tile.y + y_offset)
        if new_tile not in group and self.grid_map.is_valid(TileLevel.RES, new_tile):
            return new_tile
        return None

    @staticmethod
    def get_random_size(size: int | Tuple[int, int]) -> Tuple[int, int]:
        if isinstance(size, tuple):
            return size[0], random.randint(size[0], size[1])
        else:
            return size, size

    def find_random_locations(self, count: int) -> List[Tile]:
        tries = 0
        max_tries = count * 100
        spawns_left = count

        locs = []
        while spawns_left > 0:
            tries += 1
            loc = self.find_available_location()

            locs.append(loc)
            self.grid_map.temp(loc)
            spawns_left -= 1

            if tries > max_tries:
                break

        for loc in locs:
            self.grid_map.reset(loc)

        return locs

    def find_available_location(self) -> Tile:
        counter = 1000
        while counter > 0:
            counter -= 1
            x = random.randrange(0, self.map_size)
            y = random.randrange(0, self.map_size)

            if self.grid_map.is_available(x, y):
                return Tile(x, y)

        raise LocationNotFoundError("Unable to find a valid location. "
                                    "Please verify that the map and settings allow enough room for all spawn attempts.")
