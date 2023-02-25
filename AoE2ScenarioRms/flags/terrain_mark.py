from __future__ import annotations

from enum import IntFlag, auto


class TerrainMark(IntFlag):
    @staticmethod
    def all() -> TerrainMark:
        return TerrainMark.water_beach() | TerrainMark.LAND

    @staticmethod
    def water_beach() -> TerrainMark:
        return TerrainMark.WATER | TerrainMark.BEACH

    WATER = auto()
    BEACH = auto()
    SHORE = auto()
    """A more specific type that points to shallow water directly next to beach tiles"""
    LAND = auto()
