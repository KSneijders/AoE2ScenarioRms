from typing import Generator


def _create_counter() -> Generator[int, None, None]:
    for i in range(999_999_999):
        yield i


class RmsUtil:
    object_counter = _create_counter()
    area_counter = _create_counter()
