from typing import List

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.helper.helper import xy_to_i
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from util.spawn_grid import is_blocked, Level


def flatten_map(scenario: AoE2DEScenario):
    mm = scenario.map_manager
    # Flatten Terrain
    for t in mm.terrain:
        t.elevation = 1


def remove_terrain_layers(scenario: AoE2DEScenario):
    mm = scenario.map_manager
    for tile in mm.terrain:
        tile.layer = -1


def entire_map_black(scenario: AoE2DEScenario):
    mm = scenario.map_manager
    for tile in mm.terrain:
        tile.terrain_id = TerrainId.BLACK


def mark_blocked_terrain_as_black(scenario: AoE2DEScenario, grid_map: List[List[int]]):
    mm = scenario.map_manager
    map_size = mm.map_size

    # Debug write blocked terrain to file
    for y, col in enumerate(grid_map):
        for x, tile_open in enumerate(col):
            if is_blocked(grid_map, x, y):
                mm.terrain[xy_to_i(x, y, map_size)].terrain_id = TerrainId.BLACK


def mark_blocked_terrain_with_flags(scenario: AoE2DEScenario, grid_map: List[List[int]]):
    mm, um = scenario.map_manager, scenario.unit_manager

    # Debug write blocked terrain to file
    for y, col in enumerate(grid_map):
        for x, tile_open in enumerate(col):
            e, unit_player = grid_map[y][x], (None, 0)
            if e == Level.NONE:
                pass
            elif e == Level.TERRAIN:
                unit_player = OtherInfo.FLAG_C, 0
            elif e == Level.RES_AREA:
                unit_player = OtherInfo.FLAG_B, 2
            elif e == Level.RES:
                unit_player = OtherInfo.FLAG_C, 1
            else:
                unit_player = OtherInfo.FLAG_M, 0

            if unit_player[0] is not None:
                um.add_unit(unit_player[1], unit_player[0].ID, tile=Tile(x, y))
