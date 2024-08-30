from __future__ import annotations

from typing import TYPE_CHECKING

from AoE2ScenarioParser.helper.helper import xy_to_i
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.enums import XsKey
from AoE2ScenarioRms.rms.create_area.create_area_config import CreateAreaConfig
from AoE2ScenarioRms.rms.rms_feature import RmsFeature
from AoE2ScenarioRms.util import XsContainer, XsUtil, Locator

if TYPE_CHECKING:
    from AoE2ScenarioRms.util import GridMap


class CreateAreaFeature(RmsFeature):
    unique_names = set()

    def __init__(self, scenario: AoE2DEScenario) -> None:
        """
        Class that manages the functionality behind implementing the create_area clause

        Args:
            scenario: The scenario to apply the configs to
        """
        container = XsContainer()

        super().__init__(scenario, container)

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
                f"cArray = xsArrayGetInt(__ARRAY_AREA_CONFIGS, {name});",
                f"xsArraySetInt(cArray, 0, {config.temp_min_distance_area_placement}); // distance self: {config.temp_min_distance_area_placement}",
                f"xsArraySetInt(cArray, 1, {config.min_distance_area_placement}); // distance other: {config.min_distance_area_placement}",
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

        areas = Locator.create_areas(config, grid_map)

        for index, area in enumerate(areas):
            spawn_area = tm.add_trigger(f"Spawn {config.name} {index}/{len(areas)}")
            function = f"bool __should_spawn_area_{config.name}_{index}() {{" \
                       f"return (xsArrayGetBool(xsArrayGetInt(__ARRAY_AREA_PLACED_INDICES, {name}), {index}));" \
                       f"}}"

            spawn_area.new_condition.script_call(xs_function=function.strip().replace('  ', ''))

            # for iindex, tile in enumerate(group):
            #     spawn_group.new_effect.create_object(group_const, PlayerId.GAIA, tile.x, tile.y)
            #
            #     if config.debug_place_all:
            #         um.add_unit(PlayerId.GAIA, group_const, tile.x + .5, tile.y + .5)
            #         player = PlayerId.GAIA if iindex == 0 else PlayerId.ONE
            #         const = OtherInfo.FLAG_M.ID if iindex == 0 else OtherInfo.FLAG_C.ID
            #         um.add_unit(player, const, tile.x + .5, tile.y + .5)

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
