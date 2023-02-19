from __future__ import annotations

import random
import sys
from pathlib import Path
from typing import Tuple, List

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from classes.add_randomized_spawns import AddRandomizedSpawns
from classes.create_object import CreateObject
from enums.grouping_method import GroupingMethod
from flags.clear_options import ObjectClear
from util.resources.spawning import get_random_resource_spawn_locations
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

randomized = AddRandomizedSpawns(scenario, debug=True)
randomized.clear_scenario(ObjectClear.all())

randomized.mark_blocked_tiles()


create_objects: List[CreateObject] = [
    CreateObject(
        name='gold',
        object=OtherInfo.GOLD_MINE.ID,
        grouping=GroupingMethod.TIGHT,
        number_of_objects=(4, 5),
        temp_min_distance_group_placement=24,
        min_distance_group_placement=5,
    ),
    CreateObject(
        name='stone',
        object=OtherInfo.STONE_MINE.ID,
        grouping=GroupingMethod.TIGHT,
        number_of_objects=(3, 4),
        temp_min_distance_group_placement=27,
        min_distance_group_placement=5,
    ),
    CreateObject(
        name='berries',
        object=OtherInfo.FORAGE_BUSH.ID,
        grouping=GroupingMethod.TIGHT,
        number_of_objects=(5, 6),
        temp_min_distance_group_placement=40,
        min_distance_group_placement=5,
    ),
    CreateObject(
        name='deer',
        object=UnitInfo.DEER.ID,
        grouping=GroupingMethod.LOOSE,
        loose_grouping_distance=3,
        number_of_objects=(3, 4),
        temp_min_distance_group_placement=25,
        min_distance_group_placement=5,
    ),
    CreateObject(
        name='boar',
        object=UnitInfo.WILD_BOAR.ID,
        number_of_objects=1,
        temp_min_distance_group_placement=40,
        min_distance_group_placement=3,
        _max_potential_group_count=100,
    ),
    CreateObject(
        name='relic',
        object=OtherInfo.RELIC.ID,
        number_of_objects=1,
        temp_min_distance_group_placement=50,
        min_distance_group_placement=3,
        number_of_groups=10,
        _max_potential_group_count=100,
    ),
    CreateObject(
        name='llama',
        object=UnitInfo.LLAMA.ID,
        number_of_objects=1,
        temp_min_distance_group_placement=10,
        min_distance_group_placement=0,
        number_of_groups=2,
        scale_to_player_number=True,
        _max_potential_group_count=100,
    ),
]

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
    defined_grouping_method: str | GroupingMethod   = create_object.grouping
    min_distance_group_generation: int              = create_object.min_distance_group_generation
    max_potential_group_count: int                  = create_object.max_potential_group_count
    temp_min_distance_group_placement: int          = create_object.temp_min_distance_group_placement
    min_distance_group_placement: int               = create_object.min_distance_group_placement
    size: int | Tuple[int, int]                     = create_object.number_of_objects
    loose_grouping_distance: int                    = create_object.loose_grouping_distance
    number_of_groups: float                         = create_object.number_of_groups
    scale_to_player_number: int                     = create_object.scale_to_player_number
    # @formatter:on

    if not isinstance(defined_grouping_method, GroupingMethod):
        defined_grouping_method = GroupingMethod[str(defined_grouping_method).upper()]
    grouping_method: GroupingMethod = defined_grouping_method

    if not isinstance(size, int) and not isinstance(size, tuple):
        raise TypeError(f"Size has to be either tuple[int, int] or int, not: {type(size)}")

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

    groups = get_random_resource_spawn_locations(
        amount=max_potential_group_count,
        separation_distance=min_distance_group_generation,
        grouping_method=grouping_method,
        loose_grouping_distance=loose_grouping_distance,
        group_size=size,
        grid_map=randomized.grid_map
    )

    for index, group in enumerate(groups):
        spawn_group = tm.add_trigger(f"Spawn {name} blob {index}")
        spawn_group.new_condition.script_call(
            xs_function=f"bool __should_spawn_{name}_{index}() {{"
                        f"return (xsArrayGetBool(xsArrayGetInt(__ARRAY_RESOURCE_PLACED_INDICES, {xs_resource_name}), {index}));"
                        f"}}"
            .strip().replace('  ', '')
        )

        for tile in group:
            spawn_group.new_effect.create_object(
                source_player=PlayerId.GAIA if unit_type != UnitInfo.LLAMA.ID else PlayerId.ONE,
                object_list_unit_id=unit_type,
                location_x=tile.x,
                location_y=tile.y,
            )

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
# debug.mark_blocked_terrain_with_flags(scenario, grid_map)

scenario.write_to_file(f"{folder_de}!{filename}_written.aoe2scenario")
