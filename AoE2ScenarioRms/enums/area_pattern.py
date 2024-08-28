from enum import Enum, auto


class AreaPattern(Enum):
    """Enum to differentiate all possible ways areas can be created"""
    FLOW = auto()
    """The area pattern is randomly created based on restrictions given in the config."""
    EXACT = auto()  # Todo: Implement
    """The area pattern should match an exact pattern. This pattern must be supplied to the area config"""
