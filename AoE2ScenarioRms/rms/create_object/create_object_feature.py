from __future__ import annotations

from typing import TYPE_CHECKING, List

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.enums import XsKey
from AoE2ScenarioRms.rms.create_object.create_object_config import CreateObjectConfig
from AoE2ScenarioRms.rms.rms_feature import RmsFeature
from AoE2ScenarioRms.util import XsUtil, XsContainer, Locator

if TYPE_CHECKING:
    from AoE2ScenarioRms.util import GridMap


class CreateObjectFeature(RmsFeature):

    def __init__(self, scenario: AoE2DEScenario) -> None:
        container = XsContainer()

        super().__init__(scenario, container)

    def solve(self, configs: List[CreateObjectConfig], grid_map: 'GridMap', **kwargs) -> XsContainer:
        for config_entry in configs:
            self.init(config_entry)
            self.build(config_entry, grid_map)
        return self.container

    def init(self, config: CreateObjectConfig) -> None:
        name = self._name(config)

        self.container.append(
            XsKey.RESOURCE_VARIABLE_DECLARATION,
            f"int {name} = {config.index};"
        )

        self.container.append(
            XsKey.RESOURCE_GROUP_NAMES_DECLARATION,
            f"xsArraySetString(__RESOURCE_GROUP_NAMES, {name}, \"{config.name}\");"
        )

        self.container.append(
            XsKey.RESOURCE_COUNT_DECLARATION,
            f"xsArraySetInt(__RESOURCE_SPAWN_COUNTS, {name}, {config.max_potential_group_count});"
        )

        self.container.append(
            XsKey.RESOURCE_MAX_SPAWN_DECLARATION,
            f"xsArraySetFloat(__RESOURCE_MAX_SPAWN_COUNTS, {name}, {config.number_of_groups});"
        )

        bool_ = XsUtil.bool(config.scale_to_player_number)
        self.container.append(
            XsKey.RESOURCE_MAX_SPAWN_IS_PER_PLAYER_DECLARATION,
            f"xsArraySetBool(__RESOURCE_MAX_SPAWN_COUNTS_IS_PER_PLAYER, {name}, {bool_});"
        )

        self.container.append(
            XsKey.RESOURCE_LOCATION_INJECTION,
            f"rArray = xsArrayGetInt(__ARRAY_RESOURCE_LOCATIONS, {name});"
        )

        self.container.extend(
            XsKey.CONFIG_DECLARATION,
            [
                f"cArray = xsArrayGetInt(__ARRAY_RESOURCE_CONFIGS, {name});",
                f"xsArraySetInt(cArray, 0, {config.temp_min_distance_group_placement});",
                f"xsArraySetInt(cArray, 1, {config.min_distance_group_placement});",
            ]
        )

    def build(self, config: CreateObjectConfig, grid_map: 'GridMap') -> None:
        tm, um = self.scenario.trigger_manager, self.scenario.unit_manager
        name = self._name(config)

        groups = Locator.from_create_object_config(config, grid_map) \
            .get_valid_tiles()
        for index, group in enumerate(groups):
            spawn_group = tm.add_trigger(f"Spawn {config.name} {index}/{len(groups)}")

            function = f"bool __should_spawn_{config.name}_{index}() {{" \
                f"return (xsArrayGetBool(xsArrayGetInt(__ARRAY_RESOURCE_PLACED_INDICES, {name}), {index}));" \
                f"}}"
            spawn_group.new_condition.script_call(xs_function=function.strip().replace('  ', ''))

            for iindex, tile in enumerate(group):
                spawn_group.new_effect.create_object(config.const, PlayerId.GAIA, tile.x, tile.y)

                if config.debug_place_all:
                    um.add_unit(PlayerId.GAIA, config.const, tile.x + .5, tile.y + .5)
                    player = PlayerId.GAIA if iindex == 0 else PlayerId.ONE
                    const = OtherInfo.FLAG_M.ID if iindex == 0 else OtherInfo.FLAG_C.ID
                    um.add_unit(player, const, tile.x + .5, tile.y + .5)

            self.container.append(
                XsKey.RESOURCE_LOCATION_INJECTION,
                f"xsArraySetVector(rArray, {index}, vector({group[0].x}, {group[0].y}, -1));\t// {index}"
            )
        self.container.append(
            XsKey.RESOURCE_LOCATION_INJECTION,
            f"ShuffleVectorArray(rArray, xsArrayGetInt(__ARRAY_RESOURCE_INDICES, {name}));"
        )

    @staticmethod
    def _name(create: CreateObjectConfig) -> str:
        return f"____{create.name.upper()}"
