from pathlib import Path
from typing import Any


class XsUtil:
    @staticmethod
    def bool(val: Any) -> str:
        return 'true' if val else 'false'

    @staticmethod
    def read(path: str) -> str:
        with (Path(__file__).parent.parent / 'xs' / path).open() as file:
            return file.read()

    @staticmethod
    def format_name(name: str):
        xs_name = ' '.join(filter(lambda e: e, name.split(' ')))
        return xs_name.upper().replace(' ', '_')
