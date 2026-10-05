from __future__ import annotations

from typing import TYPE_CHECKING, List

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.enums import XsKey
from AoE2ScenarioRms.errors import InvalidCreateObjectError
from AoE2ScenarioRms.rms.create_object.create_object_config import CreateObjectConfig
from AoE2ScenarioRms.rms.rms_feature import RmsFeature
from AoE2ScenarioRms.util import XsUtil, XsContainer, Locator

if TYPE_CHECKING:
    from AoE2ScenarioRms.util import GridMap


class CreateObjectFeature(RmsFeature):
    unique_names = set()

    def __init__(self, scenario: AoE2DEScenario) -> None:
        """
        Class that manages the functionality behind implementing the create_object clause

        Args:
            scenario: The scenario to apply the configs to
        """
        container = XsContainer()

        super().__init__(scenario, container)

    def init(self, config: CreateObjectConfig) -> None:
        """
        Initialize the 'create object' configurations. Setting XS initializers like variable and array definitions

        Args:
            config: The configs to be added
        """
        name = self._name(config)

        self._validate_name_unique(name)

        self.xs_container.append(
            XsKey.RESOURCE_VARIABLE_DECLARATION,
            f"int {name} = {config.index};"
        )

        self.xs_container.append(
            XsKey.RESOURCE_GROUP_NAMES_DECLARATION,
            f"xsArraySetString(__RESOURCE_GROUP_NAMES, {name}, \"{config.name}\");"
        )

        self.xs_container.append(
            XsKey.RESOURCE_MAX_SPAWN_DECLARATION,
            f"xsArraySetFloat(__RESOURCE_MAX_SPAWN_COUNTS, {name}, {config.number_of_groups}.0);"
        )

        bool_ = XsUtil.bool(config.scale_to_player_number)
        self.xs_container.append(
            XsKey.RESOURCE_MAX_SPAWN_IS_PER_PLAYER_DECLARATION,
            f"xsArraySetBool(__RESOURCE_MAX_SPAWN_COUNTS_IS_PER_PLAYER, {name}, {bool_});"
        )

        self.xs_container.extend(
            XsKey.RESOURCE_LOCATION_INJECTION,
            [
                f"rArray = xsArrayGetInt(__ARRAY_RESOURCE_LOCATIONS, {name});",
                f"spawnConstArray = xsArrayGetInt(__ARRAY_RESOURCE_SPAWN_CONSTS, {name});",
                f"spawnTileArray = xsArrayGetInt(__ARRAY_RESOURCE_SPAWN_TILES, {name});",
            ]
        )

        self.xs_container.extend(
            XsKey.CONFIG_DECLARATION,
            [
                f"cArray = xsArrayGetInt(__ARRAY_RESOURCE_CONFIGS, {name});",
                f"xsArraySetInt(cArray, 0, {config.temp_min_distance_group_placement});",
                f"xsArraySetInt(cArray, 1, {config.min_distance_group_placement});",
            ]
        )

    def build(self, config: CreateObjectConfig, grid_map: 'GridMap') -> None:
        """
        Inject the XS that places the objects of this config. All spawning happens inside XS (through
        ``xsCreateUnit``); no triggers are generated. For every generated group the object const and the tiles to
        spawn on are injected so the XS runtime can place them directly when the group is selected.

        Args:
            config: The config to implement
            grid_map: The GridMap to take into account when generating potential locations for groups
        """
        name = self._name(config)

        groups = Locator.create_groups(config, grid_map)

        # The amount of groups that is actually spawn-able (sizes the XS arrays and the spawn loop)
        self.xs_container.append(
            XsKey.RESOURCE_COUNT_DECLARATION,
            f"xsArraySetInt(__RESOURCE_SPAWN_COUNTS, {name}, {len(groups)});"
        )

        for index, group in enumerate(groups):
            group_const = config.get_random_const()

            # Anchor location (used for the distance checks) + the spawn data for this group
            self.xs_container.extend(
                XsKey.RESOURCE_LOCATION_INJECTION,
                [
                    f"xsArraySetVector(rArray, {index}, vector({group[0].x}, {group[0].y}, -1));\t// {index}",
                    f"xsArraySetInt(spawnConstArray, {index}, {group_const});",
                    f"groupTileArray = xsArrayCreateVector({len(group)}, vector(-1, -1, -1));",
                ]
            )
            self.xs_container.extend(
                XsKey.RESOURCE_LOCATION_INJECTION,
                [
                    f"xsArraySetVector(groupTileArray, {tile_index}, vector({tile.x + .5}, {tile.y + .5}, 0));"
                    for tile_index, tile in enumerate(group)
                ]
            )
            self.xs_container.append(
                XsKey.RESOURCE_LOCATION_INJECTION,
                f"xsArraySetInt(spawnTileArray, {index}, groupTileArray);"
            )

            if config.debug_place_all:
                um = self.scenario.unit_manager

                for iindex, tile in enumerate(group):
                    um.add_unit(PlayerId.GAIA, group_const, tile.x + .5, tile.y + .5)
                    player = PlayerId.GAIA if iindex == 0 else PlayerId.ONE
                    const = OtherInfo.FLAG_M.ID if iindex == 0 else OtherInfo.FLAG_C.ID
                    um.add_unit(player, const, tile.x + .5, tile.y + .5)

        self.xs_container.append(
            XsKey.RESOURCE_LOCATION_INJECTION,
            f"ShuffleVectorArray(rArray, xsArrayGetInt(__ARRAY_RESOURCE_INDICES, {name}));"
        )

    def solve(self, configs: List[CreateObjectConfig], grid_map: 'GridMap') -> XsContainer:
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

    @staticmethod
    def _validate_name_unique(name: str) -> None:
        """
        Validate if the given name is unique compared to other names used

        Args:
            name: The name to validate

        Raises:
            InvalidCreateObjectError: If the given name has already been registered before in the scenario
        """
        if name in CreateObjectConfig.unique_names:
            raise InvalidCreateObjectError(
                f"A CreateObjectFeature with the name '{name}' was already initialized. "
                f"Make sure the names are unique and are not accidentally registered more than once.\n"
                f"Also make sure that names aren't differentiated through just casing or spaces."
            )
        CreateObjectConfig.unique_names.add(name)

    @staticmethod
    def _name(create: CreateObjectConfig) -> str:
        return f"____{XsUtil.constant(create.name)}"
