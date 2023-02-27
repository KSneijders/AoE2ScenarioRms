from __future__ import annotations

import random
from typing import Tuple, List, TYPE_CHECKING

from AoE2ScenarioParser.helper.printers import warn
from AoE2ScenarioParser.objects.support.tile import Tile

from AoE2ScenarioRms.enums import GroupingMethod, TileLevel
from AoE2ScenarioRms.errors import LocationNotFoundError, SpawnFailureWarning
from AoE2ScenarioRms.util.tile_util import TileUtil

if TYPE_CHECKING:
    from AoE2ScenarioRms.rms import CreateObjectConfig
    from AoE2ScenarioRms.util.grid_map import GridMap


class Locator:
    """

    Utility class for locating tiles in a map based on the given criteria

    """

    @staticmethod
    def create_groups(config: 'CreateObjectConfig', grid_map: 'GridMap') -> List[List[Tile]]:
        """
        Create groups for the given create object config.

        Args:
            config: The config object to be used for the groups
            grid_map: The grid map to be taken into account when creating the groups

        Returns:
            A list of groups. Each group is also a list of tiles.
        """
        available_tiles = grid_map.available_tiles(shuffle=True)

        amount = config.max_potential_group_count
        name = config.name

        tiles: List[List[Tile]] = []
        if amount * 2 > len(available_tiles):
            warn(f"For group '{name}', the amount of groups requested is really high. "
                 f"({amount} groups compared to {len(available_tiles)} available tiles).\n"
                 f"Consider lowering the max amount of necessary groups for '{name}'.", SpawnFailureWarning)

        # starting_tiles = self.find_random_locations(amount)
        starting_tiles = available_tiles[:amount]

        failed_spawns = 0
        for starting_tile in starting_tiles:
            min_, size = Locator.randomize_group_size(config.number_of_objects)

            group = [starting_tile]
            size -= 1

            failed_attempts = 0
            while size > 0 and failed_attempts < 50:
                nearby_tile = Locator.find_nearby_tile(grid_map, config.grouping, group, config.loose_grouping_distance)

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

    @staticmethod
    def find_nearby_tile(
            grid_map: GridMap,
            method: GroupingMethod,
            group: List[Tile],
            loose_grouping_distance: int = -1
    ) -> Tile | None:
        """
        Find a nearby tile with the given GridMap based on the method given.

        Args:
            grid_map: The gridmap to respect
            method: The method to use for choosing a GroupingMethod
            group: The current tiles belonging to this group (to not return a tile twice)
            loose_grouping_distance: The distance loosely grouped units have to be apart (only used for LOOSE grouping)

        Returns:
            The tile found or ``None`` if no tile was found (doesn't mean that there is no tile at all)
        """
        if method == GroupingMethod.TIGHT:
            return Locator.find_random_adjacent_tile(grid_map, random.choice(group), group)
        elif method == GroupingMethod.LOOSE:
            return Locator.find_random_tile_within_range(grid_map, group[0], loose_grouping_distance, group)
        else:
            return None

    @staticmethod
    def find_random_adjacent_tile(
            grid_map: GridMap,
            tile: Tile,
            group: List[Tile]
    ) -> Tile | None:
        """
        Find a random adjacent tile (not diagonal) around the given tile

        Args:
            grid_map: The gridmap to respect
            tile: The tile to look around
            group: The current tiles belonging to this group (to not return a tile twice)

        Returns:
            A random tile around the given tile, or if all are invalid, returns ``None``
        """
        offset = random.randrange(0, 4)

        tiles = TileUtil.adjacent(tile)
        for i in range(4):
            new_tile = tiles[(i + offset) % 4]
            if new_tile not in group and grid_map.is_valid(TileLevel.RES, new_tile):
                return new_tile
        return None

    @staticmethod
    def find_random_tile_within_range(
            grid_map: GridMap,
            tile: Tile,
            range_: int,
            group: List[Tile],
            attempts: int = 10,
    ) -> Tile | None:
        """
        Find a random tile within a given range

        Args:
            grid_map: The gridmap to respect
            tile: The tile to look around
            range_: The range in which to search for tiles
            group: The current tiles belonging to this group (to not return a tile twice)
            attempts: The amount of attempts to find a tile around a given tile

        Returns:
            A random tile around the given tile within a range. If all searches resulted in invalid tiles, None is
            returned. This does not mean there's no tiles within the range.
        """
        # Todo: Change to random.choice() to make sure `None` means no tiles are valid
        for _ in range(attempts):
            x_offset = random.randint(-range_, range_)
            y_offset = random.randint(-range_, range_)

            new_tile = Tile(tile.x + x_offset, tile.y + y_offset)
            if new_tile not in group and grid_map.is_valid(TileLevel.RES, new_tile):
                return new_tile
        return None

    @staticmethod
    def randomize_group_size(size: int | Tuple[int, int]) -> Tuple[int, int]:
        """
        Args:
            size: The size of a group

        Returns:
            A tuple with the minimum valid size for a group as first value, and if the given size is a tuple the second
            value is a randomized value between the 2 numbers. If an int was given, the int is returned as second value.
        """
        if isinstance(size, tuple):
            return size[0], random.randint(size[0], size[1])
        else:
            return size, size
