from AoE2ScenarioParser.objects.support.tile import Tile

from AoE2ScenarioRms.util import TileUtil


def test_tile_util_adjacent():
    assert TileUtil.adjacent(Tile(3, 2)) == [Tile(3, 1), Tile(2, 2), Tile(4, 2), Tile(3, 3)]


def test_tile_util_within_range():
    # @formatter:off
    assert TileUtil.within_range(5, 5, 1) == [
        Tile(4, 4), Tile(5, 4), Tile(6, 4),
        Tile(4, 5),             Tile(6, 5),
        Tile(4, 6), Tile(5, 6), Tile(6, 6),
    ]

    assert TileUtil.within_range(5, 5, 2) == [
        Tile(3, 3), Tile(4, 3), Tile(5, 3), Tile(6, 3), Tile(7, 3),
        Tile(3, 4), Tile(4, 4), Tile(5, 4), Tile(6, 4), Tile(7, 4),
        Tile(3, 5), Tile(4, 5),             Tile(6, 5), Tile(7, 5),
        Tile(3, 6), Tile(4, 6), Tile(5, 6), Tile(6, 6), Tile(7, 6),
        Tile(3, 7), Tile(4, 7), Tile(5, 7), Tile(6, 7), Tile(7, 7),
    ]
    # @formatter:on


def test_tile_util_coords():
    assert TileUtil.coords(3, 4) == (3, 4)
    assert TileUtil.coords(Tile(2, 5)) == (2, 5)
