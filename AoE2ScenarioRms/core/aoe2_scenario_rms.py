from pathlib import Path
from typing import List

from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.debug import ApplyBlockedAsBlack, ApplyAllVisible, ApplyXsPrint, ApplyNoClutter
from AoE2ScenarioRms.enums import XsKey
from AoE2ScenarioRms.flags import Debug
from AoE2ScenarioRms.rms import CreateObjectConfig, CreateObjectFeature
from AoE2ScenarioRms.util import GridMap, XsContainer, XsUtil


class AoE2ScenarioRms:
    def __init__(self, scenario: AoE2DEScenario, debug: Debug = None):
        self.scenario: AoE2DEScenario = scenario
        self.grid_map: GridMap = GridMap(self.scenario.map_manager.map_size)
        self.container: XsContainer = XsContainer()
        self.debug: Debug = debug

        self._debug_all_visible_enabled = False

        scenario.xs_manager.initialise_xs_trigger()
        scenario.xs_manager.add_script(xs_file_path=str((Path(__file__).parent.parent / 'xs' / 'random.xs').resolve()))

        if debug & Debug.ALL_VISIBLE:
            self.enable_all_visible()

        if debug & Debug.BLOCKED_AS_BLACK:
            ApplyBlockedAsBlack(self)
        if debug & Debug.NO_CLUTTER:
            ApplyNoClutter(self)

    def create_objects(self, grid_map: GridMap, configs: List[CreateObjectConfig]) -> None:
        self.container += CreateObjectFeature(self.scenario) \
            .solve(configs, self.grid_map, create_object_count=len(configs))
        self.container.append(XsKey.RESOURCE_VARIABLE_COUNT, str(len(configs)))

    def write(self) -> str:
        if self.debug & Debug.XS_PRINT:
            ApplyXsPrint(self)
        return self.container.resolve(XsUtil.read('main.xs'))

    def enable_all_visible(self) -> None:
        """
        Adds a unit to the bottom corner of the map.
        Adds map-revealers through the entire map.
        Disables other players, so they won't spawn units either.
        """
        if self._debug_all_visible_enabled:
            return

        original_write_to_file = self.scenario.write_to_file

        def write_to_file_wrapper(filename: str, skip_reconstruction: bool = False):
            ApplyAllVisible(self)
            original_write_to_file(filename, skip_reconstruction)

        self.scenario.write_to_file = write_to_file_wrapper
        self._debug_all_visible_enabled = True
