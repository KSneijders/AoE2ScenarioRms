import pytest
from AoE2ScenarioParser.objects.support.tile import Tile

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
    grid_map.set(Tile(1, 1), False)
    assert grid_map.grid_map[0][0] is True
    assert grid_map.grid_map[1][1] is False
    assert grid_map.grid_map[1][2] is True

    grid_map.reset(Tile(1, 1))
    assert grid_map.grid_map[1][1] is True


def test_grid_map_set_all(grid_map: GridMap):
    grid_map.set_all(False)

    assert grid_map.grid_map[0][0] is False
    assert grid_map.grid_map[5][4] is False
    assert grid_map.grid_map[9][9] is False

    grid_map.set_all(True)

    assert grid_map.grid_map[0][0] is True
    assert grid_map.grid_map[5][4] is True
    assert grid_map.grid_map[9][9] is True


def test_grid_map_is_available(grid_map: GridMap):
    assert grid_map.is_available(Tile(4, 4))
    assert not grid_map.is_blocked(Tile(4, 4))

    grid_map.set(Tile(4, 4), False)

    assert not grid_map.is_available(Tile(4, 4))
    assert grid_map.is_blocked(Tile(4, 4))


def test_grid_map_invert(grid_map):
    grid_map.set(Tile(2, 2), False)

    assert grid_map.grid_map[0][0] is True
    assert grid_map.grid_map[2][2] is False

    grid_map.invert()

    assert grid_map.grid_map[0][0] is False
    assert grid_map.grid_map[2][2] is True
    assert grid_map.grid_map[4][5] is False
    assert grid_map.grid_map[9][9] is False


def test_grid_map_available_tiles():
    grid_map = GridMap(5, default_availability=False)

    grid_map.grid_map[0][0] = True
    grid_map.grid_map[1][1] = True
    grid_map.grid_map[2][2] = True
    grid_map.grid_map[3][3] = True

    assert grid_map.available_tiles() == [Tile(0, 0), Tile(1, 1), Tile(2, 2), Tile(3, 3)]


def test_grid_map_is_available_size():
    grid_map = GridMap(5, default_availability=True)

    # Overflow top, left, bottom, right of the grid (in that order)
    assert grid_map.is_available_size(size=2, tile=Tile(2, 0)) is False
    assert grid_map.is_available_size(size=2, tile=Tile(0, 2)) is False
    assert grid_map.is_available_size(size=3, tile=Tile(2, 4)) is False  # Size has to be 3 because of rounding
    assert grid_map.is_available_size(size=3, tile=Tile(4, 2)) is False  # Size has to be 3 because of rounding

    # . = available; # = blocked; X = Spawn Attempt; @ = Blocked Spawn Attempt
    # _____________
    # | X X X X X |
    # | X X X X X |
    # | X X X X X |
    # | X X X X X |
    # | X X X X X |
    assert grid_map.is_available_size(size=5, tile=Tile(2, 2)) is True
    assert grid_map.is_available_size(size=6, tile=Tile(2, 2)) is False  # Size overflows the map
    assert grid_map.is_available_size(size=7, tile=Tile(2, 2)) is False  # Size overflows the map

    grid_map.grid_map[0][0] = False

    # _____________
    # | @ X X X X |
    # | X X X X X |
    # | X X X X X |
    # | X X X X X |
    # | X X X X X |
    assert grid_map.is_available_size(size=5, tile=Tile(2, 2)) is False

    # _____________
    # | @ X X X . |
    # | X X X X . |
    # | X X X X . |
    # | X X X X . |
    # | . . . . . |
    assert grid_map.is_available_size(size=4, tile=Tile(2, 2)) is False

    grid_map.grid_map[1][1] = False
    grid_map.grid_map[2][2] = False
    grid_map.grid_map[3][3] = False

    # _____________
    # | # . X X . |
    # | . # X X . |
    # | . . # . . |
    # | . . . # . |
    # | . . . . . |
    assert grid_map.is_available_size(size=2, tile=Tile(3, 1))

    # _____________
    # | # . . . . |
    # | . # . . . |
    # | . . # . . |
    # | . X X # . |
    # | . X X . . |
    assert grid_map.is_available_size(size=2, tile=Tile(2, 4))

    # _____________
    # | # . . . . |
    # | . # . . . |
    # | . . # . . |
    # | . . . @ X |
    # | . . . X X |
    assert grid_map.is_available_size(size=2, tile=Tile(4, 4)) is False

    # _____________
    # | # . . . . |
    # | . # . . . |
    # | X X @ . . |
    # | X X X # . |
    # | X X X . . |
    assert grid_map.is_available_size(size=3, tile=Tile(1, 3)) is False

    # _____________
    # | # . . . . |
    # | . # . . . |
    # | X X X . . |
    # | X X X # . |
    # | X X X . . |
    grid_map.grid_map[2][2] = True
    assert grid_map.is_available_size(size=3, tile=Tile(1, 3))
