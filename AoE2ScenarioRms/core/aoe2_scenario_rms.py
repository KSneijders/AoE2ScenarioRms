from pathlib import Path
from typing import List

from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.enums import XsKey
from AoE2ScenarioRms.errors import InvalidAoE2ScenarioRmsState
from AoE2ScenarioRms.rms import CreateObjectConfig, CreateObjectFeature
from AoE2ScenarioRms.util import GridMap, XsContainer, XsUtil


class AoE2ScenarioRms:
    def __init__(self, scenario: AoE2DEScenario):
        self.scenario: AoE2DEScenario = scenario
        self.xs_container: XsContainer = XsContainer()
        self._debug_applied = False

        scenario.xs_manager.initialise_xs_trigger()
        scenario.xs_manager.add_script(xs_file_path=str((Path(__file__).parent.parent / 'xs' / 'random.xs').resolve()))

        self._register_scenario_write_to_file_event()

    def create_objects(self, configs: List[CreateObjectConfig], grid_map: GridMap) -> None:
        self._verify_no_debug()

        create_objects = CreateObjectFeature(self.scenario)
        self.xs_container += create_objects.solve(configs, grid_map)
        self.xs_container.append(XsKey.RESOURCE_VARIABLE_COUNT, str(len(configs)))
        
    def _verify_no_debug(self) -> None:
        if self._debug_applied:
            raise InvalidAoE2ScenarioRmsState(
                "Debug applied before RMS functionality is called. "
                "Please ONLY apply debug just before `scenario.write_to_file(...)`."
            )

    def _register_scenario_write_to_file_event(self) -> None:
        """
        Adds a unit to the bottom corner of the map.
        Adds map-revealers through the entire map.
        Disables other players, so they won't spawn units either.
        """
        original_write_to_file = self.scenario.write_to_file

        def write_to_file_wrapper(filename: str, skip_reconstruction: bool = False):
            xs_string = self.xs_container.resolve(XsUtil.read('main.xs'))
            self.scenario.xs_manager.add_script(xs_string=xs_string)

            original_write_to_file(filename, skip_reconstruction)

        self.scenario.write_to_file = write_to_file_wrapper
        self._debug_all_visible_enabled = True
