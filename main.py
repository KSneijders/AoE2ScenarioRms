from __future__ import annotations

import random
import sys
from pathlib import Path
from typing import Tuple, Dict, Any, List

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

import debug
from util.prepare import clear_scenario
from util.resources.spawning import get_random_resource_spawn_locations, SpreadMethod, spawn_resource
from util.spawn_grid import create_grid_map, mark_blocked_tiles
from util.xs import replace_xs_key

seed = random.randrange(sys.maxsize)
seed = 7647799647017082024
random.seed(seed)
print("Seed:", seed)

filename = "defense"
folder_de = "C:/Users/Kerwin Sneijders/Games/Age of Empires 2 DE/76561198140740017/resources/_common/scenario/"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, um, mm, xm, pm, msm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
    scenario.player_manager, scenario.message_manager

# Make sure XS is at the top
xm.initialise_xs_trigger()

pm.active_players = 1

# Remove player related spawning
clear_scenario(scenario)

# Create and update grid map
grid_map = create_grid_map(scenario)
mark_blocked_tiles(scenario, grid_map)

# spawn_resource(scenario, OtherInfo.GOLD_MINE,   33, 26, (3, 5), SpreadMethod.TOGETHER,  4, grid_map)
# spawn_resource(scenario, OtherInfo.STONE_MINE,  25, 29, (2, 3), SpreadMethod.TOGETHER,  4, grid_map)
# spawn_resource(scenario, OtherInfo.FORAGE_BUSH, 15, 5,  (3, 5), SpreadMethod.TOGETHER,  3, grid_map)
# spawn_resource(scenario, UnitInfo.DEER,         20, 10, (3, 4), SpreadMethod.SCATTERED, 2, grid_map, 3)
# spawn_resource(scenario, UnitInfo.WILD_BOAR,      30, 10, 1, SpreadMethod.TOGETHER, 1, grid_map)

um.add_unit(1, 4, .5, mm.map_size - 1 + .5)
for set_ in scenario.new.area().select_entire_map().use_pattern_grid(block_size=3, gap_size=0).to_chunks():
    um.add_unit(1, OtherInfo.MAP_REVEALER_GIANT.ID, set_[0].x, set_[0].y)

resources = [
    {
        'name': 'gold',
        'unit_const': OtherInfo.GOLD_MINE.ID,
        'spread_method': 'together',
        'size': [4, 5],
        'spawn_separation_self': 24,
        'spawn_separation_other': 5,
    },
    {
        'name': 'stone',
        'unit_const': OtherInfo.STONE_MINE.ID,
        'spread_method': 'together',
        'size': [3, 4],
        'spawn_separation_self': 27,
        'spawn_separation_other': 5,
    },
    {
        'name': 'berries',
        'unit_const': OtherInfo.FORAGE_BUSH.ID,
        'spread_method': 'together',
        'size': [5, 6],
        'spawn_separation_self': 40,
        'spawn_separation_other': 5,
    },
    {
        'name': 'deer',
        'unit_const': UnitInfo.DEER.ID,
        'spread_method': 'scattered',
        'spread_distance': 3,
        'size': [3, 4],
        'spawn_separation_self': 25,
        'spawn_separation_other': 5,
    },
    {
        'name': 'boar',
        'unit_const': UnitInfo.WILD_BOAR.ID,
        'count': 100,
        'spawn_separation_self': 40,
        'spawn_separation_other': 3,
    },
    {
        'name': 'relic',
        'unit_const': OtherInfo.RELIC.ID,
        'count': 100,
        'spawn_separation_self': 50,
        'spawn_separation_other': 3,
        'max_spawns': 10,
    },
]

default_resource_values = {
    # The name of this blob config, needs to be unique
    'name': None,
    # The unit to spawn in this blob
    'unit_const': None,
    # The spread method ('together' (like gold) or 'scattered' (like deer))
    'spread_method': 'together',
    # The distance between blobs when generating all possibilities
    'separation': 3,
    # The amount of possible blobs that should be generated (NOT THE SPAWN AMOUNT (currently not possible to define))
    'count': 250,
    # The distance to other blobs of this type when choosing spawn positions
    'spawn_separation_self': 20,
    # The distance to other blobs of other types when choosing spawn positions
    'spawn_separation_other': 5,
    # The size of the resource blob (how many objects/units per blob)
    #   Accepts an int or a tuple[int, int] indicating a range ([1, 3] spawns 1, 2 or 3 of the resources in a blob)
    'size': 1,
    # The distance at which resources should spawn from each other in the same blob
    #   Only used with: 'spread_method': 'scattered'
    'spread_distance': 3,
    # The maximum of blobs to spawn for this resource
    'max_spawns': 999_999_999,
}

def get_resource_value(resource_config: Dict, key: str) -> int | str | Tuple[int, int]:
    v = resource_config.get(key, default_resource_values.get(key))
    if v is None:
        raise ValueError(f"The '{key}' field is required")
    return v


xs_resource_variable_declaration = []
xs_resource_count_declaration = []
xs_resource_max_spawn_declaration = []
xs_resource_location_injection = []
xs_resource_config_declaration = []

for resource_index, res in enumerate(resources):
    name: str = get_resource_value(res, 'name')
    unit_const: int = get_resource_value(res, 'unit_const')
    defined_spread_method: str = str(get_resource_value(res, 'spread_method')).upper()
    separation: int = get_resource_value(res, 'separation')
    count: int = get_resource_value(res, 'count')
    spawn_separation_self: int = get_resource_value(res, 'spawn_separation_self')
    spawn_separation_other: int = get_resource_value(res, 'spawn_separation_other')
    defined_size: int | List[int] | Tuple[int, int] = get_resource_value(res, 'size')
    spread_distance: int = get_resource_value(res, 'spread_distance')
    max_spawns: int = get_resource_value(res, 'max_spawns')

    spread_method: SpreadMethod = SpreadMethod[defined_spread_method]
    if isinstance(defined_size, list):
        defined_size = tuple(defined_size)
    elif not isinstance(defined_size, int):
        raise TypeError(f"Size has to be either list or int, not: {type(defined_size)}")
    size: int | Tuple[int, int] = defined_size

    # ----------< XS Definitions >----------
    xs_resource_name: str = f"____{name.upper()}"
    xs_resource_variable_declaration.append(f"int {xs_resource_name} = {resource_index};")
    xs_resource_count_declaration.append(f"\txsArraySetInt(__RESOURCE_SPAWN_COUNTS, {xs_resource_name}, {count});")
    xs_resource_max_spawn_declaration.append(f"\txsArraySetInt(__RESOURCE_MAX_SPAWN_COUNTS, {xs_resource_name}, {max_spawns});")
    xs_resource_location_injection.append(f"\trArray = xsArrayGetInt(__ARRAY_RESOURCE_LOCATIONS, {xs_resource_name});")
    xs_resource_config_declaration.extend([
        f"\tcArray = xsArrayGetInt(__ARRAY_RESOURCE_CONFIGS, {xs_resource_name});",
        f"\txsArraySetInt(cArray, 0, {spawn_separation_self});",
        f"\txsArraySetInt(cArray, 1, {spawn_separation_other});",
    ])

    list_of_blobs = get_random_resource_spawn_locations(
        amount=count,
        separation_distance=separation,
        blob_spreading=spread_method,
        blob_spread_distance=spread_distance,
        blob_size=size,
        grid_map=grid_map
    )

    for index, blob in enumerate(list_of_blobs):
        spawn_blob = tm.add_trigger(f"Spawn {name} blob {index}")
        spawn_blob.new_condition.script_call(
            xs_function=f"""bool __should_spawn_{name}_{index}() {{ 
                int hasBeenPlacedArray = xsArrayGetInt(__ARRAY_RESOURCE_PLACED_INDICES, {xs_resource_name});
                return (xsArrayGetBool(hasBeenPlacedArray, {index}));
            }}
            """
        )

        for tile in blob:
            spawn_blob.new_effect.create_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=unit_const,
                location_x=tile.x,
                location_y=tile.y,
            )

        xs_resource_location_injection.append(
            f"""\txsArraySetVector(rArray, {index}, vector({blob[0].x}, {blob[0].y}, -1));\t// {index}"""
        )
    xs_resource_location_injection.append(
        f"""\tShuffleVectorArray(rArray, xsArrayGetInt(__ARRAY_RESOURCE_INDICES, {xs_resource_name}));"""
    )

with (Path(__file__).parent / 'xs' / 'main.xs').open() as file:
    xs_script = file.read()

xs_script = replace_xs_key(xs_script, 'RESOURCE_VARIABLE_DECLARATION', '\n'.join(xs_resource_variable_declaration))
xs_script = replace_xs_key(xs_script, 'RESOURCE_VARIABLE_COUNT', str(len(resources)))
xs_script = replace_xs_key(xs_script, 'RESOURCE_COUNT_DECLARATION', '\n'.join(xs_resource_count_declaration))
xs_script = replace_xs_key(xs_script, 'RESOURCE_MAX_SPAWN_DECLARATION', '\n'.join(xs_resource_max_spawn_declaration))
xs_script = replace_xs_key(xs_script, 'RESOURCE_LOCATION_INJECTION', '\n'.join(xs_resource_location_injection))
xs_script = replace_xs_key(xs_script, 'CONFIG_DECLARATION', '\n'.join(xs_resource_config_declaration))

xm.add_script(xs_file_path=(Path(__file__).parent / 'xs' / 'random.xs').absolute())
xm.add_script(xs_string=xs_script)

# Debug
# debug.flatten_map(scenario)
# debug.remove_terrain_layers(scenario)
# debug.mark_blocked_terrain_as_black(scenario, grid_map)
# debug.mark_blocked_terrain_with_flags(scenario, grid_map)

scenario.write_to_file(f"{folder_de}!{filename}_written.aoe2scenario")
