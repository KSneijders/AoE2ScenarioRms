from __future__ import annotations

import copy
from typing import Dict, List

from AoE2ScenarioRms.enums import XsKey
from AoE2ScenarioRms.util.xs.xs_entry import XsEntry


class XsContainer:
    def __init__(self, config: Dict[XsKey, XsEntry] = None) -> None:
        if config is None:
            config = {}

        self.entries: Dict[XsKey, XsEntry] = config

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
            if key in entries:
                entries.get(key).extend(val.lines)
            else:
                entries.setdefault(key, val)
        return entries

    def resolve(self, script: str) -> str:
        for key, value in self.entries.items():
            script = self.replace(script, key)
        return script

    def replace(self, script: str, key: XsKey, value: str = '') -> str:
        entry = self.entries[key]
        joined_lines = entry.join_str + entry.join_str.join(value or entry.lines)
        return script.replace(f"""/* REPLACE:{key.name} */""", joined_lines)

    def init(self, key: XsKey) -> None:
        self.set(key, [])

    def set(self, key: XsKey, value: List[str]) -> None:
        self.entries[key].set(value)

    def append(self, key: XsKey, value: str) -> None:
        self.entries[key].append(value)

    def extend(self, key: XsKey, value: List[str]) -> None:
        self.entries[key].extend(value)
