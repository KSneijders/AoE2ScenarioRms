from __future__ import annotations

import math
import random
from typing import List, Optional, Tuple

from AoE2ScenarioParser.objects.support.tile import Tile

from enums.grouping_method import GroupingMethod
from util.spawn_grid import is_blocked, tile_is_valid
from enums.tile_level import TileLevel


def get_random_resource_spawn_locations(
        amount: int,
        separation_distance: int,
        grouping_method: GroupingMethod,
        group_size: int | Tuple[int, int],
        grid_map: List[List[int]],
        loose_grouping_distance: Optional[int] = -1,
) -> List[List[Tile]]:
    result_tiles: List[List[Tile]] = []
    starting_tiles = get_random_locations(amount, separation_distance, grid_map)

    for starting_tile in starting_tiles:
        if not isinstance(group_size, int):
            size = random.randint(group_size[0], group_size[1])
        else:
            size = group_size

        group_tiles = [starting_tile]
        size -= 1  # Remove the first tile from the list (deduct one from size)

        while size > 0:
            if grouping_method == GroupingMethod.TIGHT:
                tile = random.choice(group_tiles)
                adjacent_tile = get_random_adjacent_tile(tile, grid_map)
            elif grouping_method == GroupingMethod.LOOSE:
                adjacent_tile = get_random_tile_within_range(starting_tile, loose_grouping_distance, grid_map)
            else:
                raise ValueError(f"Unknown spreading method: {grouping_method}")

            if adjacent_tile is not None:
                grid_map[adjacent_tile.y][adjacent_tile.x] = TileLevel.RES
                group_tiles.append(adjacent_tile)
                size -= 1

        result_tiles.append(group_tiles)
    return result_tiles


def get_random_adjacent_tile(tile: Tile, grid_map: List[List[int]]) -> Optional[Tile]:
    rand_start = random.randrange(0, 4)

    coords = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    for i in range(4):
        x, y = coords[(rand_start + i) % 4]

        new_tile = Tile(tile.x + x, tile.y + y)
        if tile_is_valid(new_tile, TileLevel.RES, grid_map):
            return new_tile
    return None


def get_random_tile_within_range(tile: Tile, range_: int, grid_map: List[List[int]]) -> Optional[Tile]:
    x_offset = random.randrange(-range_, range_)
    y_offset = random.randrange(-range_, range_)

    new_x, new_y = tile.x + x_offset, tile.y + y_offset
    if tile_is_valid(Tile(new_x, new_y), TileLevel.RES, grid_map):
        return Tile(new_x, new_y)
    return None


def get_random_locations(n: int, separation_distance: int, grid_map: List[List[int]]) -> List[Tile]:
    locs = []

    tries, max_tries = 0, n * 100
    while n > 0:
        tries += 1
        new_loc = get_random_location(grid_map)

        if any(loc for loc in locs if get_distance(loc, new_loc) < separation_distance):
            continue

        locs.append(new_loc)
        # Will be overridden later
        grid_map[new_loc.y][new_loc.x] = TileLevel.TEMP
        n -= 1

        if tries > max_tries:
            break

    return locs


def get_random_location(grid_map: List[List[int]]) -> Tile:
    map_size = len(grid_map)

    counter = 1000
    while counter > 0:
        x = random.randrange(0, map_size)
        y = random.randrange(0, map_size)
        if not is_blocked(grid_map, x, y):
            return Tile(x, y)

        counter -= 1

    raise Exception("Unable to locate valid location")


def get_distance(tile1: Tile, tile2: Tile):
    return math.sqrt((tile1.x - tile2.x) ** 2 + (tile1.y - tile2.y) ** 2)
