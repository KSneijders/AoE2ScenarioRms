from __future__ import annotations

from typing import List, Set

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.helper.helper import i_to_xy
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from enums.tile_level import TileLevel
from util import data
from util.unit import get_tiles_around_object


def create_grid_map(scenario: AoE2DEScenario) -> List[List[int]]:
    map_size = scenario.map_manager.map_size
    return [[TileLevel.NONE for _ in range(map_size)] for _ in range(map_size)]


def mark_blocked_tiles(scenario: AoE2DEScenario, grid_map: List[List[int]]) -> None:
    # map_size = scenario.map_manager.map_size
    mm, um = scenario.map_manager, scenario.unit_manager

    # # Mark all water & Beach spots
    # water_beach_terrains = TerrainId.water_terrains() + TerrainId.beach_terrains()
    # for index, t in enumerate(mm.terrain):
    #     if t.terrain_id in water_beach_terrains:
    #         x, y = i_to_xy(index, map_size)
    #         grid_map[y][x] = TileLevel.TERRAIN

    # marked_tiles: Set[Tile] = set()
    # # Find all trees and cliffs and mark everything around it
    # for obj in um.units[PlayerId.GAIA]:
    #     if obj.unit_const in data.tree_ids:
    #         marked_tiles.update(get_tiles_around_object(obj, 1))
    #     if obj.unit_const in data.cliff_ids:
    #         marked_tiles.update(get_tiles_around_object(obj, 2))
    #
    # for tile in marked_tiles:
    #     grid_map[tile.y][tile.x] = TileLevel.TERRAIN


def tile_is_valid(tile: Tile, level: TileLevel, grid_map: List[List[int]]) -> bool:
    """If a tile is within the map and also on a tile that is not blocked by another area"""
    map_size = len(grid_map)

    return (
            0 <= tile.x <= map_size - 1
            and 0 <= tile.y <= map_size - 1
            and not is_blocked_for_level(grid_map, tile.x, tile.y, level)
    )


def is_blocked(grid_map: List[List[int]], x: int, y: int):
    return grid_map[y][x] != TileLevel.NONE


def is_blocked_for_level(grid_map: List[List[int]], x: int, y: int, level: TileLevel):
    is_temp = grid_map[y][x] == TileLevel.TEMP
    return level <= grid_map[y][x] and not is_temp


