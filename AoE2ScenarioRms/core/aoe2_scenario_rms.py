import math
from pathlib import Path
from typing import List, Set, Dict

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.helper.helper import xy_to_i, i_to_xy
from AoE2ScenarioParser.objects.data_objects.unit import Unit
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.util.grid_map import GridMap
from AoE2ScenarioRms.util.xs.xs_container import XsContainer
from AoE2ScenarioRms.enums import TileLevel, XsKey
from AoE2ScenarioRms.flags import ObjectClear, ObjectMark, TerrainMark
from AoE2ScenarioRms.rms import CreateObjectConfig, CreateObjectFeature
from AoE2ScenarioRms.util import UnitUtil, Data


class AoE2ScenarioRms:
    def __init__(self, scenario: AoE2DEScenario, debug: bool = False):
        self.scenario: AoE2DEScenario = scenario
        self.grid_map: GridMap = GridMap(self.scenario.map_manager.map_size)
        self.container = XsContainer()

        scenario.xs_manager.initialise_xs_trigger()
        scenario.xs_manager.add_script(xs_file_path=str((Path(__file__).parent.parent / 'xs' / 'random.xs').resolve()))

        if debug:
            self.enable_debug_mode()

    def create_objects(self, configs: List[CreateObjectConfig]) -> None:
        self.container += CreateObjectFeature(self.scenario)\
            .solve(configs, self.grid_map, create_object_count=len(configs))
        self.container.append(XsKey.RESOURCE_VARIABLE_COUNT, str(len(configs)))

    def write(self) -> str:
        with (Path(__file__).parent.parent / 'xs' / 'main.xs').open() as file:
            script = self.container.resolve(file.read())
        return script

    def enable_debug_mode(self) -> None:
        """
        Adds a unit to the bottom corner of the map.
        Adds map-revealers through the entire map.
        Disables other players, so they won't spawn units either.
        """
        original_write_to_file = self.scenario.write_to_file

        def write_to_file_wrapper(filename: str, skip_reconstruction: bool = False):
            mm, um, pm = self.scenario.map_manager, self.scenario.unit_manager, self.scenario.player_manager
            pm.active_players = 1
            um.add_unit(1, UnitInfo.HORSE_A.ID, .5, mm.map_size - .5)
            for chunk in self.scenario.new.area().select_entire_map() \
                    .use_pattern_grid(block_size=3, gap_size=0).to_chunks():
                um.add_unit(1, OtherInfo.MAP_REVEALER_GIANT.ID, chunk[0].x, chunk[0].y)

            original_write_to_file(filename, skip_reconstruction)

        self.scenario.write_to_file = write_to_file_wrapper

    def mark_blocked_tiles(
            self,
            terrain_marks: TerrainMark = None,
            object_marks: ObjectMark = None,
            terrain_ids: List[TerrainId] = None,
            object_consts: Dict[int, int] = None,
            fresh: bool = False
    ):
        if fresh:
            self.grid_map.reset_all()

        mm, um = self.scenario.map_manager, self.scenario.unit_manager

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
            self.grid_map.set(TileLevel.TERRAIN, tile)

    def clear_scenario(
            self,
            clear: ObjectClear = None,
            consts: List[int] = None,
            units: List[Unit] = None
    ) -> None:
        um, mm = self.scenario.unit_manager, self.scenario.map_manager

        if clear is None:
            clear = ObjectClear.RESOURCE_OBJECTS + ObjectClear.ANIMAL_OBJECTS

        consts = consts if consts is not None else []
        units = units if units is not None else []

        # Clear all player related objects
        if clear & ObjectClear.PLAYERS:
            for i in PlayerId.all(exclude_gaia=True):
                um.units[i] = []

        # Mark resources
        resource_consts = Data.get_object_consts_by_clear_options(clear)
        objects_to_remove = set(obj for obj in um.units[PlayerId.GAIA] if obj.unit_const in resource_consts)

        # Mark straggler trees
        if clear & ObjectClear.STRAGGLERS:
            tree_consts = Data.trees()
            for u in um.units[PlayerId.GAIA]:
                underlying_terrain = mm.terrain[xy_to_i(math.floor(u.x), math.floor(u.y), mm.map_size)].terrain_id
                if u.unit_const in tree_consts and underlying_terrain not in TerrainId.tree_terrains():
                    objects_to_remove.add(u)

        # Mark given consts
        if len(consts):
            objects_to_remove.update(set(um.filter_units_by_const(consts)))

        # Clear all marked objects
        for unit in objects_to_remove:
            um.remove_unit(unit=unit)

        # Clear all given objects
        for unit in units:
            um.remove_unit(unit=unit)
