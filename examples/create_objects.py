from typing import List

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

from AoE2ScenarioRms.rms.create_object import CreateObject
from AoE2ScenarioRms.enums.grouping_method import GroupingMethod

create_objects: List[CreateObject] = [
    CreateObject(
        name='gold',
        object=OtherInfo.GOLD_MINE.ID,
        grouping=GroupingMethod.TIGHT,
        number_of_objects=(4, 5),
        temp_min_distance_group_placement=24,
        min_distance_group_placement=5,
        _debug_place_all=True,
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
