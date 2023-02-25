from __future__ import annotations

import random
from typing import Tuple, List, TYPE_CHECKING

from AoE2ScenarioParser.helper.printers import warn
from AoE2ScenarioParser.objects.support.tile import Tile
from ordered_set import OrderedSet

from AoE2ScenarioRms.enums import GroupingMethod, TileLevel
from AoE2ScenarioRms.errors import LocationNotFoundError, SpawnFailureWarning

if TYPE_CHECKING:
    from AoE2ScenarioRms.rms import CreateObjectConfig
    from AoE2ScenarioRms.util.grid_map import GridMap


class Locator:
    """

    Utility class for locating tiles in a map based on the given criteria

    """

    def __init__(
            self,
            name: str,
            amount: int,
            grouping_method: GroupingMethod,
            group_size: int | Tuple[int, int],
            grid_map: 'GridMap',
            loose_grouping_distance: int = -1,
    ) -> None:
        self.name: str = name
        self.amount: int = amount
        self.grouping_method: GroupingMethod = grouping_method
        self.group_size: int | Tuple[int, int] = group_size
        self.grid_map: 'GridMap' = grid_map
        self.loose_grouping_distance: int = loose_grouping_distance

        self.map_size = grid_map.map_size

        self.available_tiles: List[Tile] = grid_map.available_tiles(shuffle=True)

    @classmethod
    def from_create_object_config(cls, create: 'CreateObjectConfig', grid_map: 'GridMap'):
        return cls(
            name=create.name,
            amount=create.max_potential_group_count,
            grouping_method=create.grouping,
            group_size=create.number_of_objects,
            grid_map=grid_map,
            loose_grouping_distance=create.loose_grouping_distance,
        )

    def get_valid_tiles(self, name: str = None, amount: int = None) -> List[List[Tile]]:
        tiles: List[List[Tile]] = []
        amount = amount or self.amount
        name = name or self.name

        if amount * 2 > len(self.available_tiles):
            warn(f"For group '{name}', the amount of groups requested is really high. "
                 f"({amount} groups compared to {len(self.available_tiles)} available tiles).\n"
                 f"Consider lowering the max amount of necessary groups for '{name}'.", SpawnFailureWarning)

        # starting_tiles = self.find_random_locations(amount)
        starting_tiles = self.available_tiles[:amount]

        failed_spawns = 0
        for starting_tile in starting_tiles:
            min_, size = self.get_random_size(self.group_size)

            group = [starting_tile]
            size -= 1

            failed_attempts = 0
            while size > 0 and failed_attempts < 50:
                nearby_tile = self.find_nearby_tile(group)

                if nearby_tile is not None:
                    group.append(nearby_tile)
                    size -= 1
                else:
                    failed_attempts += 1

            if len(group) >= min_:
                tiles.append(group)
            else:
                failed_spawns += 1

        if failed_spawns and failed_spawns / amount > .1:
            warn(f"When generating group '{name}', out of the {amount} groups, {failed_spawns} failed. "
                 f"Consider lowering the max amount of necessary groups for '{name}'.", SpawnFailureWarning)

        return tiles

    def find_nearby_tile(self, group: List[Tile]) -> Tile | None:
        if self.grouping_method == GroupingMethod.TIGHT:
            return self.find_random_adjacent_tile(random.choice(group), group)
        elif self.grouping_method == GroupingMethod.LOOSE:
            return self.find_random_tile_within_range(group[0], self.loose_grouping_distance, group)
        else:
            return None

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

    def find_random_locations(self, count: int) -> List[Tile]:
        """
        Find a list of random locations based on the grid map. Unused since shuffled list is now used.
        Might be removed in the future.
        """
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
        """
        Find a list of random locations based on the grid map. Unused since shuffled list is now used.
        Might be removed in the future.
        """
        counter = 1000
        while counter > 0:
            counter -= 1
            x = random.randrange(0, self.map_size)
            y = random.randrange(0, self.map_size)

            if self.grid_map.is_available(x, y):
                return Tile(x, y)

        raise LocationNotFoundError("Unable to find a valid location. "
                                    "Please verify that the map and settings allow enough room for all spawn attempts.")

    @staticmethod
    def get_random_size(size: int | Tuple[int, int]) -> Tuple[int, int]:
        if isinstance(size, tuple):
            return size[0], random.randint(size[0], size[1])
        else:
            return size, size
