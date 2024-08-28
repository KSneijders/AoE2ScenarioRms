from typing import Generator


class RmsUtil:
    @staticmethod
    def create_counter() -> Generator[int, None, None]:
        for i in range(999_999_999):
            yield i
