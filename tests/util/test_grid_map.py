import pytest
from AoE2ScenarioParser.objects.support.tile import Tile

from AoE2ScenarioRms.enums import TileLevel
from AoE2ScenarioRms.util import GridMap


@pytest.fixture
def grid_map():
    return GridMap(11)


def test_grid_map_init(grid_map: GridMap):
    # found_value == expected_value
    assert grid_map.map_size == 11
    assert len(grid_map.grid_map) == 11
    assert len(grid_map.grid_map[0]) == 11


def test_grid_map_set(grid_map: GridMap):
    grid_map.set(TileLevel.TERRAIN, 1, 1)
    assert grid_map.grid_map[0][0] == TileLevel.NONE
    assert grid_map.grid_map[1][1] == TileLevel.TERRAIN
    assert grid_map.grid_map[1][2] == TileLevel.NONE

    grid_map.temp(1, 1)
    assert grid_map.grid_map[1][1] == TileLevel.TEMP

    grid_map.reset(1, 1)
    assert grid_map.grid_map[1][1] == TileLevel.NONE


def test_grid_map_set_all(grid_map: GridMap):
    grid_map.set_all(TileLevel.TERRAIN)

    assert grid_map.grid_map[0][0] == TileLevel.TERRAIN
    assert grid_map.grid_map[5][4] == TileLevel.TERRAIN
    assert grid_map.grid_map[9][9] == TileLevel.TERRAIN

    grid_map.set_all(TileLevel.NONE)

    assert grid_map.grid_map[0][0] == TileLevel.NONE
    assert grid_map.grid_map[5][4] == TileLevel.NONE
    assert grid_map.grid_map[9][9] == TileLevel.NONE


def test_grid_map_is_available(grid_map: GridMap):
    assert grid_map.is_available(4, 4)
    assert not grid_map.is_blocked(4, 4)

    grid_map.set(TileLevel.TERRAIN, 4, 4)

    assert not grid_map.is_available(4, 4)
    assert grid_map.is_blocked(4, 4)


def test_grid_map_level_is_available(grid_map: GridMap):
    assert grid_map.level_is_available(TileLevel.TERRAIN, 4, 4)
    assert not grid_map.level_is_blocked(TileLevel.TERRAIN, 4, 4)

    grid_map.set(TileLevel.TERRAIN, 4, 4)

    assert not grid_map.level_is_available(TileLevel.TERRAIN, 4, 4)
    assert grid_map.level_is_blocked(TileLevel.TERRAIN, 4, 4)

    grid_map.set(TileLevel.RES, 4, 4)

    assert grid_map.level_is_available(TileLevel.TERRAIN, 4, 4)
    assert not grid_map.level_is_blocked(TileLevel.TERRAIN, 4, 4)


def test_grid_map_invert(grid_map):
    grid_map.set(TileLevel.TERRAIN, 2, 2)

    assert grid_map.grid_map[0][0] == TileLevel.NONE
    assert grid_map.grid_map[2][2] == TileLevel.TERRAIN

    grid_map.invert()

    assert grid_map.grid_map[0][0] == TileLevel.TERRAIN
    assert grid_map.grid_map[2][2] == TileLevel.NONE
    assert grid_map.grid_map[4][5] == TileLevel.TERRAIN
    assert grid_map.grid_map[9][9] == TileLevel.TERRAIN


def test_grid_map_available_tiles():
    grid_map = GridMap(5, TileLevel.TERRAIN)

    grid_map.grid_map[0][0] = TileLevel.NONE
    grid_map.grid_map[1][1] = TileLevel.NONE
    grid_map.grid_map[2][2] = TileLevel.NONE
    grid_map.grid_map[3][3] = TileLevel.NONE

    assert grid_map.available_tiles() == [Tile(0, 0), Tile(1, 1), Tile(2, 2), Tile(3, 3)]
