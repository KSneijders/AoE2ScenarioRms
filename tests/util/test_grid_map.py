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


def test_grid_map_is_available_size():
    grid_map = GridMap(5, TileLevel.NONE)

    # Overflow top, left, bottom, right of the grid (in that order)
    assert grid_map.is_available_size(size=2, x=2, y=0) is False
    assert grid_map.is_available_size(size=2, x=0, y=2) is False
    assert grid_map.is_available_size(size=3, x=2, y=4) is False  # Size has to be 3 because of rounding
    assert grid_map.is_available_size(size=3, x=4, y=2) is False  # Size has to be 3 because of rounding

    # . = available; # = blocked; X = Spawn Attempt; @ = Blocked Spawn Attempt
    # _____________
    # | X X X X X |
    # | X X X X X |
    # | X X X X X |
    # | X X X X X |
    # | X X X X X |
    assert grid_map.is_available_size(size=5, x=2, y=2)
    assert grid_map.is_available_size(size=6, x=2, y=2) is False  # Size overflows the map
    assert grid_map.is_available_size(size=7, x=2, y=2) is False  # Size overflows the map

    grid_map.grid_map[0][0] = TileLevel.TERRAIN

    # _____________
    # | @ X X X X |
    # | X X X X X |
    # | X X X X X |
    # | X X X X X |
    # | X X X X X |
    assert grid_map.is_available_size(size=5, x=2, y=2) is False

    # _____________
    # | @ X X X . |
    # | X X X X . |
    # | X X X X . |
    # | X X X X . |
    # | . . . . . |
    assert grid_map.is_available_size(size=4, x=2, y=2) is False

    grid_map.grid_map[1][1] = TileLevel.TERRAIN
    grid_map.grid_map[2][2] = TileLevel.TERRAIN
    grid_map.grid_map[3][3] = TileLevel.TERRAIN

    # _____________
    # | # . X X . |
    # | . # X X . |
    # | . . # . . |
    # | . . . # . |
    # | . . . . . |
    assert grid_map.is_available_size(size=2, x=3, y=1)

    # _____________
    # | # . . . . |
    # | . # . . . |
    # | . . # . . |
    # | . X X # . |
    # | . X X . . |
    assert grid_map.is_available_size(size=2, x=2, y=4)

    # _____________
    # | # . . . . |
    # | . # . . . |
    # | . . # . . |
    # | . . . @ X |
    # | . . . X X |
    assert grid_map.is_available_size(size=2, x=4, y=4) is False

    # _____________
    # | # . . . . |
    # | . # . . . |
    # | X X @ . . |
    # | X X X # . |
    # | X X X . . |
    assert grid_map.is_available_size(size=3, x=1, y=3) is False

    # _____________
    # | # . . . . |
    # | . # . . . |
    # | X X X . . |
    # | X X X # . |
    # | X X X . . |
    grid_map.grid_map[2][2] = TileLevel.NONE
    assert grid_map.is_available_size(size=3, x=1, y=3)
