from __future__ import annotations

from enum import IntFlag, auto


class ObjectMark(IntFlag):
    @staticmethod
    def all() -> ObjectMark:
        return ObjectMark.TREES | ObjectMark.CLIFFS

    TREES = auto()
    CLIFFS = auto()
