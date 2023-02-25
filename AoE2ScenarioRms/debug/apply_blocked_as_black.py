from typing import TYPE_CHECKING

from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.helper.helper import xy_to_i

from AoE2ScenarioRms.debug.apply_debug import ApplyDebug
from AoE2ScenarioRms.util import GridMap

if TYPE_CHECKING:
    from AoE2ScenarioRms import AoE2ScenarioRms


class ApplyBlockedAsBlack(ApplyDebug):
    """

    Change all terrain tiles that are blocked (in the gridmap) to ``TerrainId.BLACK``

    """
    def __init__(self, rms: 'AoE2ScenarioRms', grid_map: 'GridMap') -> None:
        super().__init__(rms)

        mm = rms.scenario.map_manager
        map_size = mm.map_size

        for y in range(map_size):
            for x in range(map_size):
                if grid_map.is_blocked(x, y):
                    mm.terrain[xy_to_i(x, y, map_size)].terrain_id = TerrainId.BLACK
