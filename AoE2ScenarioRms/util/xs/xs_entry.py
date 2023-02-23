from typing import List

from AoE2ScenarioParser.helper.pretty_format import pretty_format_list


class XsEntry:
    lines: List[str]
    join_str: str

    def __init__(self, lines: List[str] = None, join: str = '\n') -> None:
        super().__init__()

        if lines is None:
            lines = []

        self.lines: List[str] = lines
        self.join_str: str = join

    def set(self, value: List[str]):
        self.lines = value

    def append(self, value: str):
        self.lines.append(value)

    def extend(self, value: List[str]):
        self.lines.extend(value)

    def __repr__(self) -> str:
        join = self.join_str.replace('\n', '\\n').replace('\t', '\\t')
        return f"""XsEntry({pretty_format_list(self.lines)}, '{join}')"""


