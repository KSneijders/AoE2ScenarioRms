from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

from AoE2ScenarioRms import AoE2ScenarioRms
from AoE2ScenarioRms.debug.apply_debug import ApplyDebug


class ApplyAllVisible(ApplyDebug):
    def __init__(self, rms: AoE2ScenarioRms) -> None:
        mm, um, pm = rms.scenario.map_manager, rms.scenario.unit_manager, rms.scenario.player_manager
        pm.active_players = 1

        um.add_unit(1, UnitInfo.HORSE_A.ID, .5, mm.map_size - .5)

        grid_area = rms.scenario.new.area().select_entire_map().use_pattern_grid(block_size=3, gap_size=0)

        for chunk in grid_area.to_chunks():
            um.add_unit(1, OtherInfo.MAP_REVEALER_GIANT.ID, chunk[0].x, chunk[0].y)
