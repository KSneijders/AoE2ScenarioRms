from enum import IntFlag, auto


class Debug(IntFlag):
    ALL_VISIBLE = auto()
    """Fill the entire map with map revealers and add a unit for p1 to see everything immediately when testing"""
    BLOCKED_AS_BLACK = auto()
    """Change all terrain tiles that are blocked (in the gridmap) to TerrainId.BLACK"""
    XS_PRINT = auto()
    """When testing, the amount of resources that were able to spawn is printed in the chat"""
    NO_CLUTTER = auto()
    """Set the entire map to have no elevation or layered terrain for extra clarity"""
