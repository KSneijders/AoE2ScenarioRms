from AoE2ScenarioRms.errors import InvalidCreateObjectError
from AoE2ScenarioRms.util import XsUtil


class RmsConfig:
    """Super class for all RMS config classes."""
    unique_names = set()

    index: int
    """The index for the specific config in this type. Implemented a different index counter per type"""

    def __init__(self, name: str) -> None:
        super().__init__()

        self.name = self._validate_name_unique(name)

    @staticmethod
    def _validate_name_unique(name: str) -> str:
        xs_name = XsUtil.constant(name)

        if xs_name in RmsConfig.unique_names:
            raise InvalidCreateObjectError(
                f"[{name}]: group/area with name '{name}' ('{xs_name}') already exists. Make sure all names are unique and "
                f"aren't differentiated through just casing or spaces."
            )
        RmsConfig.unique_names.add(xs_name)

        return xs_name.lower()
