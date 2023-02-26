from AoE2ScenarioParser.objects.support.tile import Tile

from AoE2ScenarioRms.util import TileUtil


def test_tile_util_adjacent():
    assert TileUtil.adjacent(Tile(3, 2)) == [Tile(3, 1), Tile(2, 2), Tile(4, 2), Tile(3, 3)]


def test_tile_util_coords():
    assert TileUtil.coords(3, 4) == (3, 4)
    assert TileUtil.coords(Tile(2, 5)) == (2, 5)
