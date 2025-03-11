from pathlib import Path
from typing import List

from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.enums import XsKey
from AoE2ScenarioRms.errors import InvalidAoE2ScenarioRmsState
from AoE2ScenarioRms.rms import CreateObjectConfig, CreateObjectFeature
from AoE2ScenarioRms.util import GridMap, XsContainer, XsUtil


class AoE2ScenarioRms:

    def __init__(self, scenario: AoE2DEScenario):
        """
        Core class of this AoE2ScenarioParser plugin (?). Manages the 'overarching' functionality of adding RMS features to
        the given scenario

        Args:
            scenario: The scenario to edit with this plugin (?)
        """
        self.scenario: AoE2DEScenario = scenario
        self.xs_container: XsContainer = XsContainer()

        # Staggered spawning configuration options (Can decrease lag spikes)
        self.staggered_resource_spawning = False
        """If resources should spawn staggered or all at once"""
        self.staggered_resource_offset = 0
        """The amount of time to start spawning resources (this number is added on top of the staggered delay)"""
        self.staggered_resource_delay = 0
        """The amount of delay between resource spawn cycles in in-game seconds"""
        self.staggered_resource_batch_size = 1
        """The amount of resources to spawn per cycle (i.e. set to 2 for spawning all gold and stone in the same cycle)"""

        # Internal
        self._debug_applied = False
        self.resources: dict[str, CreateObjectConfig] = {}
        """A map of the given configs by the given names"""

        scenario.xs_manager.initialise_xs_trigger()
        scenario.xs_manager.add_script(xs_file_path=str((Path(__file__).parent.parent / 'xs' / 'random.xs').resolve()))

        self._register_scenario_write_to_file_event()

    def create_objects(self, configs: List[CreateObjectConfig], grid_map: GridMap) -> None:
        """
        Add a set of <create object> configs to your scenario. This represents the ``create_object`` blocks in the
        ``<OBJECTS_GENERATION>`` section of an RMS script.

        Args:
            configs: The configs for this create object block
            grid_map: The grid map marking the area where this block should (not) be applied
        """
        self._verify_no_debug()

        # Store the configs for later use
        for config in configs:
            self.resources[config.name] = config

        create_objects = CreateObjectFeature(self.scenario)
        self.xs_container += create_objects.solve(configs, grid_map)

    def _verify_no_debug(self) -> None:
        """
        Verify if no debug classes have been applied to this scenario

        Raises:
            InvalidAoE2ScenarioRmsState: When debug functions have previously been applied to this scenario
        """
        if self._debug_applied:
            raise InvalidAoE2ScenarioRmsState(
                "Debug applied before RMS functionality is called. "
                "Please ONLY apply debug just before `scenario.write_to_file(...)`."
            )

    def _register_scenario_write_to_file_event(self) -> None:

        @self.scenario.on_write
        def func(scenario: AoE2DEScenario):
            delay = self.staggered_resource_offset
            for resource_id, (resource_name, resource_config) in enumerate(self.resources.items()):

                trigger: Trigger = scenario.trigger_manager.add_trigger(name=f'Spawn All of Resource {resource_name}')

                if self.staggered_resource_spawning:
                    trigger.new_condition.timer(timer=delay)

                trigger.new_effect.script_call(
                    message=f'void spawnAllShort_{resource_name}() {{ spawnAllOfResource__895621354({resource_id}); }}'
                )

                if resource_id % self.staggered_resource_batch_size == 0:
                    delay += self.staggered_resource_delay

            self.xs_container.append(XsKey.RESOURCE_VARIABLE_COUNT, str(len(self.resources)))

            xs_string = self.xs_container.resolve(XsUtil.file('main.xs'))
            scenario.xs_manager.add_script(xs_string=xs_string)
