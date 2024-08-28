from abc import abstractmethod

from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.errors.exceptions import InvalidCreateFeatureStateError
from AoE2ScenarioRms.util import XsUtil
from AoE2ScenarioRms.util.xs_container import XsContainer
from AoE2ScenarioRms.util.grid_map import GridMap
from AoE2ScenarioRms.rms.rms_config import RmsConfig


class RmsFeature:
    """Super class for all RMS feature classes."""

    unique_names: set[str] = set()

    def __init__(self, scenario: AoE2DEScenario, xs_container: XsContainer) -> None:
        self.scenario: AoE2DEScenario = scenario
        self.xs_container: XsContainer = xs_container

    @abstractmethod
    def init(self, config: RmsConfig) -> None:
        ...

    @abstractmethod
    def build(self, config: RmsConfig, grid_map: GridMap) -> None:
        ...

    @abstractmethod
    def solve(self, config: RmsConfig, grid_map: GridMap):
        ...

    @staticmethod
    def _validate_name_unique(name: str) -> str:
        """
        Validate if the given name is unique compared to other names used

        Args:
            name: The name to validate

        Raises:
            InvalidCreateObjectError: If the given name has already been registered before in the scenario
        """
        name = RmsFeature._format_name(name)

        if name in RmsFeature.unique_names:
            raise InvalidCreateFeatureStateError(
                f"A Feature with the name '{name}' was already initialized. "
                f"Make sure the names are unique and are not accidentally registered more than once.\n"
                f"Also make sure that names aren't differentiated through just casing or spaces."
            )

        RmsFeature.unique_names.add(name)

        return name

    @staticmethod
    def _format_name(name: str) -> str:
        return f"____{XsUtil.constant(name)}"
