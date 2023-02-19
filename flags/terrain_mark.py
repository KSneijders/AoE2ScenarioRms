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
    LAND = auto()
