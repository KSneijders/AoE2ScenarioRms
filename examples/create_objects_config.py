from typing import List

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

from AoE2ScenarioRms.enums import GroupingMethod
from AoE2ScenarioRms.enums.area_pattern import AreaPattern
from AoE2ScenarioRms.rms import CreateObjectConfig
from AoE2ScenarioRms.rms.create_group.create_area_config import CreateAreaConfig

bandit_camp_area_config: list[CreateAreaConfig] = [
    CreateAreaConfig(
        name='camps',
        area_pattern=AreaPattern.FLOW,
        area_spread_radius=5,
        min_distance_area_placement=8,  # Unused for now, no other areas
        temp_min_distance_area_placement=40,
        block_group_spawns=True,
        create_objects=[
            CreateObjectConfig(
                name='camp_mining_camp',
                const=BuildingInfo.MINING_CAMP.ID,
                number_of_objects=1,
                number_of_groups=1,
                min_distance_group_placement=0,
                _max_potential_group_count=3,
            ),
            CreateObjectConfig(
                name='camp_barracks',
                const=BuildingInfo.BARRACKS.ID,
                number_of_objects=1,
                number_of_groups=1,
                min_distance_group_placement=0,
                _max_potential_group_count=5,
            ),
            CreateObjectConfig(
                name='camp_gold',
                const=OtherInfo.GOLD_MINE.ID,
                grouping=GroupingMethod.TIGHT,
                number_of_objects=(1, 3),
                number_of_groups=8,
                temp_min_distance_group_placement=1,
                min_distance_group_placement=0,
                _max_potential_group_count=12,
            ),
            CreateObjectConfig(
                name='camp_archers',
                const=UnitInfo.ARCHER.ID,
                grouping=GroupingMethod.TIGHT,
                number_of_objects=1,
                number_of_groups=4,
                temp_min_distance_group_placement=1,
                min_distance_group_placement=0,
                min_distance_to_map_edge=2,
                _max_potential_group_count=12,
            ),
        ]
    )
]

create_objects_config: List[CreateObjectConfig] = [
    CreateObjectConfig(
        name='gold',
        const=OtherInfo.GOLD_MINE.ID,
        grouping=GroupingMethod.TIGHT,
        number_of_objects=(4, 5),
        temp_min_distance_group_placement=24,
        min_distance_group_placement=5,
    ),
    CreateObjectConfig(
        name='stone',
        const=OtherInfo.STONE_MINE.ID,
        grouping=GroupingMethod.TIGHT,
        number_of_objects=(3, 4),
        temp_min_distance_group_placement=27,
        min_distance_group_placement=5,
    ),
    CreateObjectConfig(
        name='berries',
        const=OtherInfo.FORAGE_BUSH.ID,
        grouping=GroupingMethod.TIGHT,
        number_of_objects=(5, 6),
        temp_min_distance_group_placement=40,
        min_distance_group_placement=5,
    ),
    CreateObjectConfig(
        name='deer',
        const=UnitInfo.DEER.ID,
        grouping=GroupingMethod.LOOSE,
        loose_grouping_distance=3,
        number_of_objects=(3, 4),
        temp_min_distance_group_placement=25,
        min_distance_group_placement=5,
    ),
    CreateObjectConfig(
        name='boar',
        const=UnitInfo.WILD_BOAR.ID,
        number_of_objects=1,
        temp_min_distance_group_placement=40,
        min_distance_group_placement=3,
        _max_potential_group_count=100,
    ),
    CreateObjectConfig(
        name='relic',
        const=OtherInfo.RELIC.ID,
        number_of_objects=1,
        temp_min_distance_group_placement=50,
        min_distance_group_placement=3,
        number_of_groups=10,
        _max_potential_group_count=100,
    ),
    CreateObjectConfig(
        name='llama',
        const=UnitInfo.LLAMA.ID,
        number_of_objects=1,
        temp_min_distance_group_placement=10,
        min_distance_group_placement=0,
        number_of_groups=2,
        scale_to_player_number=True,
        _max_potential_group_count=100,
    ),
]

create_objects_config_shore_fish: List[CreateObjectConfig] = [
    CreateObjectConfig(
        name='shore fish',
        const=OtherInfo.SHORE_FISH.ID,
        temp_min_distance_group_placement=8,
        min_distance_group_placement=0,
        _max_potential_group_count=50,
    )
]

create_objects_config_deep_fish: List[CreateObjectConfig] = [
    CreateObjectConfig(
        name='deep fish',
        object_size=2,
        const=[
            OtherInfo.FISH_TUNA.ID,
            OtherInfo.FISH_PERCH.ID,
            OtherInfo.FISH_DORADO.ID,
            OtherInfo.FISH_SALMON.ID,
            OtherInfo.FISH_SNAPPER.ID,
        ],
        temp_min_distance_group_placement=8,
        min_distance_group_placement=3,
    )
]
