import random

import pytest
from AoE2ScenarioParser.objects.support.tile import Tile

from AoE2ScenarioRms.enums import GroupingMethod, TileLevel
from AoE2ScenarioRms.rms import CreateObjectConfig
from AoE2ScenarioRms.util import Locator, GridMap, TileUtil


@pytest.fixture
def grid_map():
    grid_map = GridMap(5)
    for i in range(5):
        grid_map.set(TileLevel.TERRAIN, i, 1)
    return grid_map


@pytest.fixture
def create_object_config():
    return CreateObjectConfig(
        name='Test Config',
        const=0,
        number_of_groups=5,
        number_of_objects=4,
        grouping=GroupingMethod.TIGHT,
    )


@pytest.fixture(autouse=True)
def set_seed():
    random.seed(14_14_14_14_14_14)


def test_locator_get_valid_tiles(create_object_config: CreateObjectConfig, grid_map: GridMap):
    create_object_config.max_potential_group_count = 15
    groups = Locator.create_groups(create_object_config, grid_map)

    sum_ = sum([len(e) for e in groups])
    assert sum_ == 60  # 15 groups of 4

    for group in groups:
        for tile in group:
            assert tile.y != 1


def test_locator_find_random_adjacent_tile(grid_map: GridMap):
    adjacent = set(TileUtil.adjacent(Tile(3, 3)))
    tiles = set()
    for _ in range(20):
        tiles.add(Locator.find_random_adjacent_tile(grid_map, Tile(3, 3), [Tile(3, 3)]))
    assert tiles == adjacent

    # Test if it cannot get tile that is already in group
    adjacent.remove(Tile(3, 2))
    tiles = set()
    for _ in range(20):
        tiles.add(Locator.find_random_adjacent_tile(grid_map, Tile(3, 3), [Tile(3, 2)]))
    assert tiles == adjacent

    # Test that it won't return tiles over map edge or on blocked terrain (x=*, y=1)
    adjacent = {Tile(3, 2), Tile(4, 3)}
    tiles = set()
    for _ in range(20):
        tiles.add(Locator.find_random_adjacent_tile(grid_map, Tile(4, 2), [Tile(4, 2)]))
    assert tiles == adjacent

    # Test that it returns None when it can't find any tile
    assert Locator.find_random_adjacent_tile(grid_map, Tile(0, 0), [Tile(0, 0), Tile(1, 0)]) is None


def test_locator_find_random_tile_within_range(grid_map: GridMap):
    adjacent = {Tile(x, y) for x in range(2, 5) for y in range(2, 5) if x != 3 or y != 3}
    tiles = set()
    success = 0
    while success < 100:
        tile = Locator.find_random_tile_within_range(grid_map, Tile(3, 3), 1, [Tile(3, 3)])

        if tile is not None:
            success += 1
            tiles.add(tile)

    assert tiles == adjacent


def test_locator_get_random_size():
    assert Locator.randomize_group_size(2) == (2, 2)
    assert Locator.randomize_group_size((3, 4)) == (3, 3)
    assert Locator.randomize_group_size((2, 7)) == (2, 4)
