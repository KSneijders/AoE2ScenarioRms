"""
> THIS FILE WILL BE REMOVED IN THE FUTURE <
"""
from __future__ import annotations

import random
import sys
from pathlib import Path
from typing import Tuple

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.classes import AoE2ScenarioRms, GroupsConfig
from AoE2ScenarioRms.enums.grouping_method import GroupingMethod
from AoE2ScenarioRms.flags import ObjectClear, TerrainMark, ObjectMark
from AoE2ScenarioRms.local_config import folder_de
from AoE2ScenarioRms.util.xs import replace_xs_key, to_xs_bool
from examples.create_objects import create_objects


seed = random.randrange(sys.maxsize)
seed = 7647799647017082024
random.seed(seed)
print("Seed:", seed)

filename = "defense2"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, um, mm, xm, pm, msm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
    scenario.player_manager, scenario.message_manager

asr = AoE2ScenarioRms(scenario, debug=True)

asr.clear_scenario(ObjectClear.ALL & ~ObjectClear.CLIFFS)
asr.mark_blocked_tiles(
    terrain_marks=TerrainMark.water_beach(),
    object_marks=ObjectMark.all(),
)

asr.resolve(create_objects)

xs_resource_variable_declaration = []
xs_resource_count_declaration = []
xs_resource_max_spawn_declaration = []
xs_resource_max_spawn_is_per_player_declaration = []
xs_resource_location_injection = []
xs_resource_config_declaration = []

for resource_index, create_object in enumerate(create_objects):
    # @formatter:off
    name: str                                       = create_object.name
    unit_type: int                                  = create_object.object
    grouping_method: GroupingMethod                 = create_object.grouping
    max_potential_group_count: int                  = create_object.max_potential_group_count
    temp_min_distance_group_placement: int          = create_object.temp_min_distance_group_placement
    min_distance_group_placement: int               = create_object.min_distance_group_placement
    base_group_size: int | Tuple[int, int]          = create_object.number_of_objects
    loose_grouping_distance: int                    = create_object.loose_grouping_distance
    number_of_groups: float                         = create_object.number_of_groups
    scale_to_player_number: int                     = create_object.scale_to_player_number
    # @formatter:on

    # ----------< XS Definitions >----------
    xs_resource_name: str = f"____{name.upper()}"

    xs_resource_variable_declaration.append(
        f"int {xs_resource_name} = {resource_index};"
    )
    xs_resource_count_declaration.append(
        f"\txsArraySetInt(__RESOURCE_SPAWN_COUNTS, {xs_resource_name}, {max_potential_group_count});"
    )
    xs_resource_max_spawn_declaration.append(
        f"\txsArraySetFloat(__RESOURCE_MAX_SPAWN_COUNTS, {xs_resource_name}, {number_of_groups});"
    )
    xs_resource_max_spawn_is_per_player_declaration.append(
        f"\txsArraySetBool(__RESOURCE_MAX_SPAWN_COUNTS_IS_PER_PLAYER, {xs_resource_name}, "
        f"{to_xs_bool(scale_to_player_number)});"
    )
    xs_resource_location_injection.append(
        f"\trArray = xsArrayGetInt(__ARRAY_RESOURCE_LOCATIONS, {xs_resource_name});"
    )
    xs_resource_config_declaration.extend([
        f"\tcArray = xsArrayGetInt(__ARRAY_RESOURCE_CONFIGS, {xs_resource_name});",
        f"\txsArraySetInt(cArray, 0, {temp_min_distance_group_placement});",
        f"\txsArraySetInt(cArray, 1, {min_distance_group_placement});",
    ])

    groups = GroupsConfig(
        name=name,
        amount=max_potential_group_count,
        grouping_method=grouping_method,
        group_size=base_group_size,
        grid_map=asr.grid_map,
        loose_grouping_distance=loose_grouping_distance,
    ).resolve()

    for index, group in enumerate(groups):
        spawn_group = tm.add_trigger(f"Spawn {name} group {index}")
        spawn_group.new_condition.script_call(
            xs_function=f"bool __should_spawn_{name}_{index}() {{"
                        f"return (xsArrayGetBool(xsArrayGetInt(__ARRAY_RESOURCE_PLACED_INDICES, {xs_resource_name}), {index}));"
                        f"}}"
            .strip().replace('  ', '')
        )

        for iindex, tile in enumerate(group):
            spawn_group.new_effect.create_object(
                source_player=PlayerId.GAIA if unit_type != UnitInfo.LLAMA.ID else PlayerId.ONE,
                object_list_unit_id=unit_type,
                location_x=tile.x,
                location_y=tile.y,
            )

            if create_object.debug_place_all:
                um.add_unit(player=PlayerId.GAIA, unit_const=unit_type, x=tile.x + .5, y=tile.y + .5)

                player = PlayerId.GAIA if iindex == 0 else PlayerId.ONE
                const = OtherInfo.FLAG_M.ID if iindex == 0 else OtherInfo.FLAG_C.ID

                um.add_unit(player=player, unit_const=const, x=tile.x + .5, y=tile.y + .5)

        xs_resource_location_injection.append(
            f"""\txsArraySetVector(rArray, {index}, vector({group[0].x}, {group[0].y}, -1));\t// {index}"""
        )
    xs_resource_location_injection.append(
        f"""\tShuffleVectorArray(rArray, xsArrayGetInt(__ARRAY_RESOURCE_INDICES, {xs_resource_name}));"""
    )

with (Path(__file__).parent / 'xs' / 'main.xs').open() as file:
    xs_script = file.read()

xs_script = replace_xs_key(xs_script, 'RESOURCE_VARIABLE_DECLARATION', '\n'.join(xs_resource_variable_declaration))
xs_script = replace_xs_key(xs_script, 'RESOURCE_VARIABLE_COUNT', str(len(create_objects)))
xs_script = replace_xs_key(xs_script, 'RESOURCE_COUNT_DECLARATION', '\n'.join(xs_resource_count_declaration))
xs_script = replace_xs_key(xs_script, 'RESOURCE_MAX_SPAWN_DECLARATION', '\n'.join(xs_resource_max_spawn_declaration))
xs_script = replace_xs_key(
    xs_script, 'RESOURCE_MAX_SPAWN_IS_PER_PLAYER_DECLARATION',
    '\n'.join(xs_resource_max_spawn_is_per_player_declaration)
)
xs_script = replace_xs_key(xs_script, 'RESOURCE_LOCATION_INJECTION', '\n'.join(xs_resource_location_injection))
xs_script = replace_xs_key(xs_script, 'CONFIG_DECLARATION', '\n'.join(xs_resource_config_declaration))

xm.add_script(xs_file_path=str((Path(__file__).parent / 'xs' / 'random.xs').resolve()))
xm.add_script(xs_string=xs_script)

# Debug statements
# debug.flatten_map(scenario)
# debug.remove_terrain_layers(scenario)
# debug.mark_blocked_terrain_as_black(scenario, grid_map)
# debug.mark_blocked_terrain_with_flags(scenario, asr.grid_map)

scenario.write_to_file(f"{folder_de}!{filename}_written.aoe2scenario")
