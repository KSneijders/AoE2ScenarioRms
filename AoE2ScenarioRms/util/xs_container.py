from __future__ import annotations

import copy
from typing import Dict, List

from AoE2ScenarioRms.enums import XsKey


class XsContainer:
    def __init__(self, entries: Dict[XsKey, List[str]] = None) -> None:
        self.entries: Dict[XsKey, List[str]]

        self._set_entries(entries or {})

    def _set_entries(self, entries: Dict[XsKey, List[str]]):
        self.entries: Dict[XsKey, List[str]] = {key: entries.get(key, []) for key in XsKey}

    def __add__(self, other: XsContainer):
        return XsContainer(self._add(other, True))

    def __iadd__(self, other: XsContainer):
        self._add(other, False)
        return self

    def _add(self, other: XsContainer, deepcopy: bool):
        if not isinstance(other, XsContainer):
            raise TypeError(f"Cannot add XsContainer with {other.__class__}")

        entries = copy.deepcopy(self.entries) if deepcopy else self.entries
        for key, val in other.entries.items():
            entries.setdefault(key, []).extend(val)
        return entries

    def resolve(self, script: str) -> str:
        for key in self.entries.keys():
            script = self.replace(script, key)
        return script

    def replace(self, script: str, key: XsKey) -> str:
        join_string = XsKey.join_string(key)

        joined_lines = join_string + join_string.join(self.entries[key])
        return script.replace(f"""/* REPLACE:{key.name} */""", joined_lines)

    def init(self, key: XsKey) -> None:
        self.set(key, [])

    def set(self, key: XsKey, value: List[str]) -> None:
        self.entries[key] = value

    def append(self, key: XsKey, value: str) -> None:
        self.entries[key].append(value)

    def extend(self, key: XsKey, value: List[str]) -> None:
        self.entries[key].extend(value)
