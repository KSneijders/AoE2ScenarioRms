from __future__ import annotations

from enum import IntFlag, auto


class TerrainMark(IntFlag):
    """Flag used for marking specific object related aspects of the map"""

    WATER = auto()
    """Mark all water (excluding the shore line, first line of water next to the beach)"""
    BEACH = auto()
    """Mark all beach tiles"""
    SHORE = auto()
    """Mark the shore line (first line of water around the beach tiles)"""
    LAND = auto()
    """Mark everything that is not water or beach tiles."""

    WATER_BEACH = WATER | SHORE | BEACH
    """Mark the water, shore and beach tiles"""
    ALL = WATER_BEACH | LAND
    """
    Mark everything...... Nice and pointless... Why would you need this? 11
    
    Are you sure you don't need the opposite ``GridMapFactory`` function? Give the opposite a try:
     
    - ``GridMapFactory.block(...)`` or
    - ``GridMapFactory.select(...)``
    """
