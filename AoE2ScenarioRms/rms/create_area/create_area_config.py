from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from AoE2ScenarioParser.datasets.terrains import TerrainId

from AoE2ScenarioRms.enums.area_pattern import AreaPattern
from AoE2ScenarioRms.errors.exceptions import InvalidCreateAreaError
from AoE2ScenarioRms.rms.rms_config import RmsConfig
from AoE2ScenarioRms.util.rms_util import RmsUtil

if TYPE_CHECKING:
    from AoE2ScenarioRms.rms import CreateObjectConfig


# Todo: Add a way to expand base_size. How RMS does it: (land_percent OR number_of_tiles) + clump_factor (allows for circle-like behaviour)
class CreateAreaConfig(RmsConfig):
    def __init__(
            self,
            name: str,
            number_of_areas: int = 999_999_999,  # (As many as can fit) Cannot be math.inf as `str(...)` is used
            area_pattern: AreaPattern = AreaPattern.FLOW,
            base_size: int = 5,
            min_distance_area_placement: int = 5,
            temp_min_distance_area_placement: int = 20,
            block_resource_spawns: bool = True,

            scale_number_of_areas_by_player_number: bool = False,
            scale_number_of_areas_by_map_size: bool = False,
            scale_size_by_player_number: bool = False,
            scale_size_by_map_size: bool = False,

            create_objects: Callable[[], list[CreateObjectConfig]] = None,

            # ----- Debug & Parser -----
            _max_potential_area_count: int = 200,
            _debug_place_all: bool = False,
            _debug_mark_area_with_terrain: tuple[TerrainId, TerrainId] | TerrainId | None = None,
    ) -> None:
        super().__init__(name)

        if scale_number_of_areas_by_player_number and scale_number_of_areas_by_map_size:
            raise InvalidCreateAreaError(f"[{self.name}]: cannot use more than one scale_number_of_areas_by_x at the same time")

        if scale_size_by_player_number and scale_size_by_map_size:
            raise InvalidCreateAreaError(f"[{self.name}]: cannot use more than one scale_size_by_x at the same time")

        if (scale_number_of_areas_by_player_number or scale_number_of_areas_by_map_size) and number_of_areas > 100_000:
            raise InvalidCreateAreaError(f"[{self.name}]: cannot use scale_number_of_areas_by_x with player number when number of areas is above 100k")

        self.number_of_areas: int = number_of_areas
        self.area_pattern: AreaPattern = area_pattern
        self.base_size: int = base_size

        self.min_distance_area_placement: int = min_distance_area_placement
        self.temp_min_distance_area_placement: int = temp_min_distance_area_placement               # Todo:                [ ✖️ Implemented]
        self.block_resource_spawns: bool = block_resource_spawns                                    # Todo:                [ ✖️ Implement]

        self.scale_number_of_areas_to_player_number: bool = scale_number_of_areas_by_player_number  # Todo: [ ✖️ Declared] [ ✖️ Implement]
        self.scale_number_of_areas_to_map_size: bool = scale_number_of_areas_by_map_size            # Todo: [ ✖️ Declared] [ ✖️ Implement]
        self.scale_size_to_player_number: bool = scale_size_by_player_number                        # Todo: [ ✖️ Declared] [ ✖️ Implement]
        self.scale_size_to_map_size: bool = scale_size_by_map_size                                  # Todo: [ ✖️ Declared] [ ✖️ Implement]

        self.create_objects = create_objects() if create_objects is not None else []                # Todo: [ ✖️ Declared] [ ✖️ Implement]

        self.max_potential_area_count: int = _max_potential_area_count                              # Todo:                [ ✖️ Implement]
        self.debug_place_all: bool = _debug_place_all                                               # Todo:                [ ✖️ Implement]
        self.debug_mark_area_with_terrain: tuple[TerrainId, TerrainId] | TerrainId | None = _debug_mark_area_with_terrain

        self.index = next(RmsUtil.area_counter)

        RmsConfig.current_construction_area_name = None
