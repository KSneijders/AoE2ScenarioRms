from typing import Any


class XsUtil:
    @staticmethod
    def bool(val: Any):
        return 'true' if val else 'false'

