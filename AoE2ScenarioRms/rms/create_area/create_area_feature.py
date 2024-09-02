from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from AoE2ScenarioParser.helper.helper import xy_to_i
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.enums import XsKey
from AoE2ScenarioRms.rms.create_area.create_area_config import CreateAreaConfig
from AoE2ScenarioRms.rms.rms_feature import RmsFeature
from AoE2ScenarioRms.util import XsContainer, XsUtil, Locator, GridMapFactory
from AoE2ScenarioRms.util.rms_util import RmsUtil

if TYPE_CHECKING:
    from AoE2ScenarioRms.util import GridMap
    from AoE2ScenarioRms import AoE2ScenarioRms


class CreateAreaFeature(RmsFeature):
    unique_names = set()

    def __init__(self, scenario: AoE2DEScenario, scenario_rms: 'AoE2ScenarioRms') -> None:
        """
        Class that manages the functionality behind implementing the create_area clause

        Args:
            scenario: The scenario to apply the configs to
        """
        container = XsContainer()

        super().__init__(scenario, container)

        self.scenario_rms = scenario_rms

    def init(self, config: CreateAreaConfig) -> None:
        """
        Initialize the 'create area' configurations. Setting XS initializers like variable and array definitions

        Args:
            config: The configs to be added
        """
        name = self._validate_name_unique(config.name)

        self.xs_container.append(
            XsKey.AREA_VARIABLE_DECLARATION,
            f"int {name} = {config.index};"
        )

        self.xs_container.append(
            XsKey.AREA_GROUP_NAMES_DECLARATION,
            f"xsArraySetString(__AREA_GROUP_NAMES, {name}, \"{config.name}\");"
        )

        self.xs_container.append(
            XsKey.AREA_COUNT_DECLARATION,
            f"xsArraySetInt(__AREA_SPAWN_COUNTS, {name}, {config.max_potential_area_count});"
        )

        self.xs_container.append(
            XsKey.AREA_MAX_SPAWN_DECLARATION,
            f"xsArraySetFloat(__AREA_MAX_SPAWN_COUNTS, {name}, {config.number_of_areas});"
        )

        self.xs_container.append(
            XsKey.AREA_RESOURCE_COUNTS_DECLARATION,
            f"xsArraySetInt(__AREA_RESOURCE_COUNTS, {name}, {len(config.create_objects)});"
        )

        # Todo: Implement scaling to player number / map size

        block_resource_spawns = XsUtil.bool(config.block_resource_spawns)
        self.xs_container.append(
            XsKey.AREA_BLOCK_RESOURCE_SPAWNS_DECLARATION,
            f"xsArraySetBool(__AREA_BLOCK_RESOURCE_SPAWNS, {name}, {block_resource_spawns});"
        )

        self.xs_container.append(
            XsKey.AREA_LOCATION_INJECTION,
            f"rArray = xsArrayGetInt(__ARRAY_AREA_LOCATIONS, {name});"
        )

        self.xs_container.extend(
            XsKey.AREA_CONFIG_DECLARATION,
            [
                f"tempArray = xsArrayGetInt(__ARRAY_AREA_CONFIGS, {name});",
                f"xsArraySetInt(tempArray, 0, {config.temp_min_distance_area_placement}); // distance self: {config.temp_min_distance_area_placement}",
                f"xsArraySetInt(tempArray, 1, {config.min_distance_area_placement}); // distance other: {config.min_distance_area_placement}",
            ]
        )

    def build(self, config: CreateAreaConfig, grid_map: 'GridMap') -> None:
        """
        Write the functional logic (triggers) for placing the objects. Also write the functional and conditional logic
        for XS for the given configs.

        Args:
            config: The config to implement
            grid_map: The GridMap to take into account when generating potential locations for groups
        """
        tm, um, mm = self.scenario.trigger_manager, self.scenario.unit_manager, self.scenario.map_manager
        name = self._format_name(config.name)

        self.xs_container.append(
            XsKey.AREA_CONFIG_DECLARATION,
            f"tempArray = xsArrayGetInt(__ARRAY_AREA_RESOURCE_IDS, {name});"
        )

        areas = Locator.create_areas(config, grid_map)

        if config.debug_place_all:
            for object_config in config.create_objects:
                object_config.debug_place_all = True

        for index, area in enumerate(areas):
            spawn_area = tm.add_trigger(f"Spawn {config.name} {index}/{len(areas)}")
            function = f"bool __should_spawn_area_{config.name}_{index}() {{" \
                       f"return (xsArrayGetBool(xsArrayGetInt(__ARRAY_AREA_PLACED_INDICES, {name}), {index}));" \
                       f"}}"

            spawn_area.new_condition.script_call(xs_function=function.strip().replace('  ', ''))

            create_objects_config = copy.deepcopy(config.create_objects)

            self.xs_container.append(
                XsKey.AREA_CONFIG_DECLARATION,
                f"temp2Array = xsArrayGetInt(tempArray, {index});"
            )

            for object_index, object_config in enumerate(create_objects_config):
                object_name = object_config.name

                object_config.index = next(RmsUtil.object_counter)
                object_config.name = f"{object_name}_{index}"

                self.xs_container.append(
                    XsKey.AREA_CONFIG_DECLARATION,
                    f"xsArraySetInt(temp2Array, {object_index}, {object_config.index}); // {config.name}[{index}][{object_name}] = {object_config.index}"
                )

            grid_map = GridMapFactory.select(scenario=self.scenario, area=area)
            self.scenario_rms.create_objects(configs=create_objects_config, grid_map=grid_map)

            centre = area.get_center_int()
            self.xs_container.append(
                XsKey.AREA_LOCATION_INJECTION,
                f"xsArraySetVector(rArray, {index}, vector({centre[0]}, {centre[1]}, {config.base_size * 2}));\t// {index}"
            )
        self.xs_container.append(
            XsKey.AREA_LOCATION_INJECTION,
            f"ShuffleVectorArray(rArray, xsArrayGetInt(__ARRAY_AREA_INDICES, {name}));"
        )

        debug_mark_area_terrain = config.debug_mark_area_with_terrain
        if debug_mark_area_terrain is not None:

            if isinstance(debug_mark_area_terrain, tuple):
                terrain, centre = debug_mark_area_terrain
            else:
                terrain = centre = debug_mark_area_terrain

            for area in areas:
                tiles = area.to_coords()

                for tile in tiles:
                    mm.terrain[xy_to_i(*tile, mm.map_size)].terrain_id = terrain

                mm.terrain[xy_to_i(*area.get_center_int(), mm.map_size)].terrain_id = centre

    def solve(self, configs: list[CreateAreaConfig], grid_map: 'GridMap') -> XsContainer:
        """
        Execute the init and build steps in one go for each config given.

        Args:
            configs: The configs to implement
            grid_map: The GridMap to take into account when generating potential locations for groups of configs

        Returns:
            The XsContainer with all generated XS
        """
        for config_entry in configs:
            self.init(config_entry)
            self.build(config_entry, grid_map)
        return self.xs_container
