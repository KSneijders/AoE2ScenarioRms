from typing import TYPE_CHECKING

from AoE2ScenarioRms.debug.apply_debug import ApplyDebug


if TYPE_CHECKING:
    from AoE2ScenarioRms import AoE2ScenarioRms


class ApplyNoClutter(ApplyDebug):
    def __init__(self, rms: 'AoE2ScenarioRms') -> None:
        for tile in rms.scenario.map_manager.terrain:
            tile.layer = -1
            tile.elevation = 1
