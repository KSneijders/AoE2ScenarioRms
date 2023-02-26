import random

import pytest
from AoE2ScenarioParser.objects.support.tile import Tile

from AoE2ScenarioRms.enums import GroupingMethod, TileLevel
from AoE2ScenarioRms.util import Locator, GridMap, TileUtil


@pytest.fixture
def locator():
    grid_map = GridMap(5)
    for i in range(5):
        grid_map.set(TileLevel.TERRAIN, i, 1)

    return Locator(
        name='TestLocator',
        amount=5,
        grouping_method=GroupingMethod.TIGHT,
        group_size=4,
        grid_map=grid_map,
        loose_grouping_distance=0,
    )


@pytest.fixture(autouse=True)
def set_seed():
    random.seed(14_14_14_14_14_14)


def test_locator_get_valid_tiles(locator: Locator):
    groups = locator.get_valid_tiles('test_name', 15)

    sum_ = sum([len(e) for e in groups])
    assert sum_ == 60  # 15 groups of 4

    for group in groups:
        for tile in group:
            assert tile.y != 1


def test_locator_find_random_adjacent_tile(locator: Locator):
    adjacent = set(TileUtil.adjacent(Tile(3, 3)))
    tiles = set()
    for _ in range(20):
        tiles.add(locator.find_random_adjacent_tile(Tile(3, 3), [Tile(3, 3)]))
    assert tiles == adjacent

    # Test if it cannot get tile that is already in group
    adjacent.remove(Tile(3, 2))
    tiles = set()
    for _ in range(20):
        tiles.add(locator.find_random_adjacent_tile(Tile(3, 3), [Tile(3, 2)]))
    assert tiles == adjacent

    # Test that it won't return tiles over map edge or on blocked terrain (x=*, y=1)
    adjacent = {Tile(3, 2), Tile(4, 3)}
    tiles = set()
    for _ in range(20):
        tiles.add(locator.find_random_adjacent_tile(Tile(4, 2), [Tile(4, 2)]))
    assert tiles == adjacent

    # Test that it returns None when it can't find any tile
    assert locator.find_random_adjacent_tile(Tile(0, 0), [Tile(0, 0), Tile(1, 0)]) is None


def test_locator_find_random_tile_within_range(locator: Locator):
    adjacent = {Tile(x, y) for x in range(2, 5) for y in range(2, 5) if x != 3 or y != 3}
    tiles = set()
    success = 0
    while success < 100:
        tile = locator.find_random_tile_within_range(Tile(3, 3), 1, [Tile(3, 3)])

        if tile is not None:
            success += 1
            tiles.add(tile)

    assert tiles == adjacent


def test_locator_get_random_size():
    assert Locator.randomize_group_size(2) == (2, 2)
    assert Locator.randomize_group_size((3, 4)) == (3, 3)
    assert Locator.randomize_group_size((2, 7)) == (2, 4)
