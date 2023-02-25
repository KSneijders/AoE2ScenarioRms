from enum import IntFlag, auto


class ObjectClear(IntFlag):
    PLAYERS = auto()
    BOARS = auto()
    SHEEP = auto()
    DEER = auto()
    WOLFS = auto()
    GOLDS = auto()
    STONES = auto()
    BUSHES = auto()
    STRAGGLERS = auto()
    RELICS = auto()
    CLIFFS = auto()
    DEEP_FISH = auto()
    SHORE_FISH = auto()

    ANIMAL_OBJECTS = BOARS | SHEEP | DEER | WOLFS
    FISH_OBJECTS = DEEP_FISH | SHORE_FISH
    RESOURCE_OBJECTS = GOLDS | STONES | BUSHES | STRAGGLERS | RELICS
    ALL = ANIMAL_OBJECTS | FISH_OBJECTS | RESOURCE_OBJECTS | PLAYERS | CLIFFS
