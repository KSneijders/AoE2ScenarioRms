import math

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.helper.helper import xy_to_i
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from util import data
from util.data import tree_ids


def clear_scenario(scenario: AoE2DEScenario):
    um, mm = scenario.unit_manager, scenario.map_manager

    # Remove all player objects
    for i in PlayerId.all(exclude_gaia=True):
        um.units[i] = []

    remove_objects_ids = data.player_resources_ids.copy()
    remove_objects_ids.append(OtherInfo.RELIC.ID)

    # Clear all objects to be removed (deer, boar, sheep, gold, stone, etc.)
    objects_to_remove = set(obj for obj in um.units[0] if obj.unit_const in remove_objects_ids)

    # # Remove straggler trees
    for u in um.units[PlayerId.GAIA]:
        underlying_terrain = mm.terrain[xy_to_i(math.floor(u.x), math.floor(u.y), mm.map_size)].terrain_id
        if u.unit_const in tree_ids and underlying_terrain not in TerrainId.tree_terrains():
            objects_to_remove.add(u)

    for unit in objects_to_remove:
        um.remove_unit(unit=unit)
