from typing import List, Dict, Set

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.helper.helper import i_to_xy
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.enums import TileLevel
from AoE2ScenarioRms.flags import TerrainMark, ObjectMark
from AoE2ScenarioRms.util.data import Data
from AoE2ScenarioRms.util.grid_map import GridMap
from AoE2ScenarioRms.util.unit_util import UnitUtil


class GridMapFactory:
    @staticmethod
    def default(
            scenario: 'AoE2DEScenario',
            terrain_marks: TerrainMark = None,
            object_marks: ObjectMark = None,
            terrain_ids: List[TerrainId] = None,
            object_consts: Dict[int, int] = None,
    ):
        mm, um = scenario.map_manager, scenario.unit_manager
        grid_map = GridMap(mm.map_size)

        terrain_marks = terrain_marks if terrain_marks is not None else TerrainMark.water_beach()
        object_marks = object_marks if object_marks is not None else ObjectMark.all()
        terrain_ids = terrain_ids if terrain_ids is not None else []
        object_consts = object_consts if object_consts is not None else {}

        # Mark all selected terrains
        terrain_ids = Data.get_terrain_ids_by_terrain_marks(terrain_marks) + terrain_ids
        marked_tiles: Set[Tile] = set()
        if len(terrain_ids):
            for index, t in enumerate(mm.terrain):
                if t.terrain_id in terrain_ids:
                    marked_tiles.add(Tile(*i_to_xy(index, mm.map_size)))

        # Mark everything around trees and cliffs and optionally given consts
        trees, cliffs = Data.trees(), Data.cliffs()

        mark_trees = object_marks & ObjectMark.TREES
        mark_cliffs = object_marks & ObjectMark.CLIFFS
        for obj in um.units[PlayerId.GAIA]:
            if mark_trees and obj.unit_const in trees:
                marked_tiles.update(UnitUtil.get_tiles_around_object(obj, 1))
            elif mark_cliffs and obj.unit_const in cliffs:
                marked_tiles.update(UnitUtil.get_tiles_around_object(obj, 2))

        units = um.filter_units_by_const(list(object_consts.keys()))
        for unit in units:
            marked_tiles.update(UnitUtil.get_tiles_around_object(unit, object_consts[unit.unit_const]))

        for tile in marked_tiles:
            grid_map.set(TileLevel.TERRAIN, tile)
