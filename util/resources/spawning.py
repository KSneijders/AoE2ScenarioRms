from __future__ import annotations

import math
import random
from typing import List, Optional, Tuple

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.support.info_dataset_base import InfoDatasetBase
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from util.resources.grouping_method import GroupingMethod
from util.spawn_grid import is_blocked_for_level, Level, is_blocked, tile_is_valid


def spawn_resource(scenario: AoE2DEScenario,
                   res: InfoDatasetBase,
                   amount: int,
                   separation_distance: int,
                   blob_size: int | Tuple[int, int],
                   blob_spreading: GroupingMethod,
                   block_area: int,
                   grid_map: List[List[int]],
                   blob_spread_distance: Optional[int] = -1):
    tiles = get_random_xy_locations(amount, separation_distance, grid_map)

    for tile in tiles:
        spawn_resource_blob(scenario, res, tile, blob_spreading, blob_spread_distance, blob_size, block_area, grid_map)


def get_random_resource_spawn_locations(
        amount: int,
        separation_distance: int,
        blob_spreading: GroupingMethod,
        blob_size: int | Tuple[int, int],
        grid_map: List[List[int]],
        blob_spread_distance: Optional[int] = -1,
) -> List[List[Tile]]:
    result_tiles: List[List[Tile]] = []
    starting_tiles = get_random_xy_locations(amount, separation_distance, grid_map)

    for starting_tile in starting_tiles:
        if not isinstance(blob_size, int):
            size = random.randint(blob_size[0], blob_size[1])
        else:
            size = blob_size

        blob_tiles = [starting_tile]
        size -= 1  # Remove the first tile from the list (deduct one from size)

        while size > 0:
            if blob_spreading == GroupingMethod.TOGETHER:
                tile = random.choice(blob_tiles)
                adjacent_tile = get_random_adjacent_tile(tile, grid_map)
            elif blob_spreading == GroupingMethod.SCATTERED:
                adjacent_tile = get_random_tile_within_range(starting_tile, blob_spread_distance, grid_map)
            else:
                raise ValueError(f"Unknown spreading method: {blob_spreading}")

            if adjacent_tile is not None:
                grid_map[adjacent_tile.y][adjacent_tile.x] = Level.RES
                blob_tiles.append(adjacent_tile)
                size -= 1

        result_tiles.append(blob_tiles)
    return result_tiles


def spawn_resource_blob(scenario: AoE2DEScenario,
                        res: InfoDatasetBase,
                        starting_tile: Tile,
                        blob_spreading: GroupingMethod,
                        blob_spread_distance: int,
                        size: int | Tuple[int, int],
                        block_area: int,
                        grid_map: List[List[int]]) -> None:
    um = scenario.unit_manager
    if not isinstance(size, int):
        size = random.randint(size[0], size[1])

    tiles = [starting_tile]
    grid_map[starting_tile.y][starting_tile.x] = Level.RES
    size -= 1

    tries, max_tries = 0, size * 100
    while size > 0:
        tries += 1

        if blob_spreading == GroupingMethod.TOGETHER:
            tile = random.choice(tiles)
            adjacent_tile = get_random_adjacent_tile(tile, grid_map)
        elif blob_spreading == GroupingMethod.SCATTERED:
            adjacent_tile = get_random_tile_within_range(starting_tile, blob_spread_distance, grid_map)
        else:
            raise ValueError(f"Unknown spreading method: {blob_spreading}")

        if adjacent_tile is not None:
            grid_map[adjacent_tile.y][adjacent_tile.x] = Level.RES
            tiles.append(adjacent_tile)
            size -= 1

        if tries > max_tries:
            return

    surrounding_tiles = set()
    for index, tile in enumerate(tiles):
        if index == 0:
            um.add_unit(PlayerId.THREE, OtherInfo.FLAG_J.ID, tile=tile)
        um.add_unit(PlayerId.GAIA, res.ID, tile=tile)
        surrounding_tiles.update(scenario.new.area().select(tile.x, tile.y).size(block_area * 2 + 1).to_coords())

    for tile in surrounding_tiles:
        if not is_blocked_for_level(grid_map, tile.x, tile.y, Level.RES_AREA):
            grid_map[tile.y][tile.x] = Level.RES_AREA


def get_random_adjacent_tile(tile: Tile, grid_map: List[List[int]]) -> Optional[Tile]:
    rand_start = random.randrange(0, 4)

    coords = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    for i in range(4):
        x, y = coords[(rand_start + i) % 4]

        new_x, new_y = tile.x + x, tile.y + y

        if tile_is_valid(Tile(new_x, new_y), Level.RES, grid_map):
            return Tile(new_x, new_y)
    return None


def get_random_tile_within_range(tile: Tile, range_: int, grid_map: List[List[int]]) -> Optional[Tile]:
    x_offset = random.randrange(-range_, range_)
    y_offset = random.randrange(-range_, range_)

    new_x, new_y = tile.x + x_offset, tile.y + y_offset
    if tile_is_valid(Tile(new_x, new_y), Level.RES, grid_map):
        return Tile(new_x, new_y)
    return None


def get_random_xy_locations(n: int, separation_distance: int, grid_map: List[List[int]]) -> List[Tile]:
    locs = []

    tries, max_tries = 0, n * 100
    while n > 0:
        tries += 1
        new_loc = get_random_location(grid_map)

        if any(loc for loc in locs if get_xy_distance(loc, new_loc) < separation_distance):
            continue

        locs.append(new_loc)
        # Will be overridden later
        grid_map[new_loc.y][new_loc.x] = Level.TEMP
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


def get_xy_distance(tile1: Tile, tile2: Tile):
    return math.sqrt((tile1.x - tile2.x) ** 2 + (tile1.y - tile2.y) ** 2)
