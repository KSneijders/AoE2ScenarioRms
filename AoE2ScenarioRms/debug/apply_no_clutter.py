from AoE2ScenarioRms import AoE2ScenarioRms
from AoE2ScenarioRms.debug.apply_debug import ApplyDebug


class ApplyNoClutter(ApplyDebug):
    def __init__(self, rms: AoE2ScenarioRms) -> None:
        for tile in rms.scenario.map_manager.terrain:
            tile.layer = -1
            tile.elevation = 1
