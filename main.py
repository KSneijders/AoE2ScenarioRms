from __future__ import annotations

import random
import sys
from pathlib import Path
from typing import Tuple, Dict, List

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from util.prepare import clear_scenario
from util.resources.grouping_method import GroupingMethod
from util.resources.spawning import get_random_resource_spawn_locations
from util.spawn_grid import create_grid_map, mark_blocked_tiles
from util.xs import replace_xs_key, to_xs_bool

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

um.add_unit(1, 4, .5, mm.map_size - .5)
for set_ in scenario.new.area().select_entire_map().use_pattern_grid(block_size=3, gap_size=0).to_chunks():
    um.add_unit(1, OtherInfo.MAP_REVEALER_GIANT.ID, set_[0].x, set_[0].y)

resources = [
    {
        'name': 'gold',
        'unit_const': OtherInfo.GOLD_MINE.ID,
        'grouping_method': GroupingMethod.TOGETHER,
        'number_of_objects': [4, 5],
        'min_separation_distance_self': 24,
        'min_separation_distance_other': 5,
    },
    {
        'name': 'stone',
        'unit_const': OtherInfo.STONE_MINE.ID,
        'grouping_method': GroupingMethod.TOGETHER,
        'number_of_objects': [3, 4],
        'min_separation_distance_self': 27,
        'min_separation_distance_other': 5,
    },
    {
        'name': 'berries',
        'unit_const': OtherInfo.FORAGE_BUSH.ID,
        'grouping_method': GroupingMethod.TOGETHER,
        'number_of_objects': [5, 6],
        'min_separation_distance_self': 40,
        'min_separation_distance_other': 5,
    },
    {
        'name': 'deer',
        'unit_const': UnitInfo.DEER.ID,
        'grouping_method': GroupingMethod.SCATTERED,
        'spread_distance': 3,
        'number_of_objects': [3, 4],
        'min_separation_distance_self': 25,
        'min_separation_distance_other': 5,
    },
    {
        'name': 'boar',
        'unit_const': UnitInfo.WILD_BOAR.ID,
        'potential_spawn_count': 100,
        'number_of_objects': 1,
        'min_separation_distance_self': 40,
        'min_separation_distance_other': 3,
    },
    {
        'name': 'relic',
        'unit_const': OtherInfo.RELIC.ID,
        'potential_spawn_count': 100,
        'number_of_objects': 1,
        'min_separation_distance_self': 50,
        'min_separation_distance_other': 3,
        'number_of_groups': 10,
    },
    {
        'name': 'llama',
        'unit_const': UnitInfo.LLAMA.ID,
        'potential_spawn_count': 100,
        'number_of_objects': 1,
        'min_separation_distance_self': 10,
        'min_separation_distance_other': 0,
        'number_of_groups': 2,
        'scale_number_of_groups_to_player_count': True,
    },
]

default_resource_values = {
    # The name of this blob config, needs to be unique
    'name': None,
    # The unit to spawn in this blob
    'unit_const': None,
    # The spread method ('together' (like gold) or 'scattered' (like deer))
    'grouping_method': GroupingMethod.TOGETHER,
    # The distance between blobs when generating all possibilities
    'potential_spawn_separation_distance': 3,
    # The amount of possible blobs that should be generated (NOT THE SPAWN AMOUNT (currently not possible to define))
    'potential_spawn_count': 250,
    # The distance to other blobs of this type when choosing spawn positions
    'min_separation_distance_self': 20,
    # The distance to other blobs of other types when choosing spawn positions
    'min_separation_distance_other': 5,
    # The size of the resource blob (how many objects/units per blob)
    #   Accepts an int or a tuple[int, int] indicating a range ([1, 3] spawns 1, 2 or 3 of the resources in a blob)
    'number_of_objects': 1,
    # The distance at which resources should spawn from each other in the same blob
    #   Only used with: 'grouping_method': 'scattered'
    'spread_distance': 3,
    # The amount of groups to spawn (maximum). Ignored when 'number_of_groups_for_every_player' is set.
    # Remember that ALWAYS a single spawn will occur. Even if this is set to less than 1.
    'number_of_groups': 999_999_999,
    # If the amount of groups to spawn (maximum) should be relative to the amount of players.
    #   With this enabled and ... (Examples)
    #      ... 'number_of_groups' to 3 with 2 players will result in 6 spawns.
    #      ... 'number_of_groups' to 0.5 with 6 players will result in 3 spawns.
    #      ... 'number_of_groups' to 0.34 with 1, 2 or 3 player(s) will all result in a single spawn.
    'scale_number_of_groups_to_player_count': False,
}


def get_resource_value(resource_config: Dict, key: str) -> int | str | Tuple[int, int]:
    v = resource_config.get(key, default_resource_values.get(key))
    if v is None:
        raise ValueError(f"The '{key}' field is required")
    return v


xs_resource_variable_declaration = []
xs_resource_count_declaration = []
xs_resource_max_spawn_declaration = []
xs_resource_max_spawn_is_per_player_declaration = []
xs_resource_location_injection = []
xs_resource_config_declaration = []

for resource_index, res in enumerate(resources):
    # @formatter:off
    name: str                                       = get_resource_value(res, 'name')
    unit_const: int                                 = get_resource_value(res, 'unit_const')
    defined_grouping_method: str | GroupingMethod   = get_resource_value(res, 'grouping_method')
    potential_spawn_separation: int                 = get_resource_value(res, 'potential_spawn_separation_distance')
    potential_spawn_count: int                      = get_resource_value(res, 'potential_spawn_count')
    min_separation_distance_self: int               = get_resource_value(res, 'min_separation_distance_self')
    min_separation_distance_other: int              = get_resource_value(res, 'min_separation_distance_other')
    defined_size: int | List[int] | Tuple[int, int] = get_resource_value(res, 'number_of_objects')
    spread_distance: int                            = get_resource_value(res, 'spread_distance')
    number_of_groups: int                           = get_resource_value(res, 'number_of_groups')
    scale_number_of_groups_to_player_count: int     = get_resource_value(res, 'scale_number_of_groups_to_player_count')
    # @formatter:on

    if not isinstance(defined_grouping_method, GroupingMethod):
        defined_grouping_method = GroupingMethod[str(defined_grouping_method).upper()]
    grouping_method: GroupingMethod = defined_grouping_method

    if isinstance(defined_size, list):
        defined_size = tuple(defined_size)
    elif not isinstance(defined_size, int):
        raise TypeError(f"Size has to be either list or int, not: {type(defined_size)}")
    size: int | Tuple[int, int] = defined_size

    # ----------< XS Definitions >----------
    xs_resource_name: str = f"____{name.upper()}"
    xs_resource_variable_declaration.append(
        f"int {xs_resource_name} = {resource_index};")
    xs_resource_count_declaration.append(
        f"\txsArraySetInt(__RESOURCE_SPAWN_COUNTS, {xs_resource_name}, {potential_spawn_count});")
    xs_resource_max_spawn_declaration.append(
        f"\txsArraySetFloat(__RESOURCE_MAX_SPAWN_COUNTS, {xs_resource_name}, {number_of_groups});")
    xs_resource_max_spawn_is_per_player_declaration.append(
        f"\txsArraySetBool(__RESOURCE_MAX_SPAWN_COUNTS_IS_PER_PLAYER, {xs_resource_name}, "
        f"{to_xs_bool(scale_number_of_groups_to_player_count)});"
    )
    xs_resource_location_injection.append(
        f"\trArray = xsArrayGetInt(__ARRAY_RESOURCE_LOCATIONS, {xs_resource_name});")
    xs_resource_config_declaration.extend([
        f"\tcArray = xsArrayGetInt(__ARRAY_RESOURCE_CONFIGS, {xs_resource_name});",
        f"\txsArraySetInt(cArray, 0, {min_separation_distance_self});",
        f"\txsArraySetInt(cArray, 1, {min_separation_distance_other});",
    ])

    list_of_blobs = get_random_resource_spawn_locations(
        amount=potential_spawn_count,
        separation_distance=potential_spawn_separation,
        blob_spreading=grouping_method,
        blob_spread_distance=spread_distance,
        blob_size=size,
        grid_map=grid_map
    )

    for index, blob in enumerate(list_of_blobs):
        spawn_blob = tm.add_trigger(f"Spawn {name} blob {index}")
        spawn_blob.new_condition.script_call(
            xs_function=f"""
                bool __should_spawn_{name}_{index}() {{return (xsArrayGetBool(xsArrayGetInt(__ARRAY_RESOURCE_PLACED_INDICES, {xs_resource_name}), {index}));}}
            """.strip().replace('  ', '')
        )

        for tile in blob:
            spawn_blob.new_effect.create_object(
                source_player=PlayerId.GAIA if unit_const != UnitInfo.LLAMA.ID else PlayerId.ONE,
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
xs_script = replace_xs_key(
    xs_script, 'RESOURCE_MAX_SPAWN_IS_PER_PLAYER_DECLARATION',
    '\n'.join(xs_resource_max_spawn_is_per_player_declaration)
)
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
