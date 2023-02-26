from pathlib import Path
from typing import Any


class XsUtil:
    @staticmethod
    def bool(val: Any) -> str:
        return 'true' if val else 'false'

    @staticmethod
    def file(path: str) -> str:
        with (Path(__file__).parent.parent / 'xs' / path).open() as file:
            return file.read()

    @staticmethod
    def constant(name: str):
        xs_name = ' '.join(filter(lambda e: e, name.split(' ')))
        return xs_name.upper().replace(' ', '_')
