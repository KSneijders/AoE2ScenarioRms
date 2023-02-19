from enum import IntFlag, auto


class ObjectClear(IntFlag):
    @staticmethod
    def resource_objects():
        return ObjectClear.GOLDS \
            | ObjectClear.STONES \
            | ObjectClear.BUSHES \
            | ObjectClear.STRAGGLERS \
            | ObjectClear.RELICS

    @staticmethod
    def animal_objects():
        return ObjectClear.BOARS \
            | ObjectClear.SHEEP \
            | ObjectClear.DEER \
            | ObjectClear.WOLFS

    @staticmethod
    def all():
        return ObjectClear.PLAYERS \
            | ObjectClear.CLIFFS \
            | ObjectClear.resource_objects() \
            | ObjectClear.animal_objects()

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
