from AoE2ScenarioRms.errors import InvalidCreateObjectError
from AoE2ScenarioRms.util import XsUtil


class RmsConfig:
    """Super class for all RMS config classes."""
    current_construction_area_name: str = None
    """The name of the area that is currently being constructed. Used to prefix object names within a group"""
    unique_names = set()

    index: int
    """The index for the specific config in this type. Implemented a different index counter per type"""

    def __init__(self, name: str) -> None:
        super().__init__()

        self.name = self._validate_name_unique(name)

        if self._is_type('CreateAreaConfig'):
            RmsConfig.current_construction_area_name = self.name

    def _validate_name_unique(self, name: str) -> str:
        # Prefix create object configs with the area config name
        area_name = RmsConfig.current_construction_area_name
        if self._is_type('CreateObjectConfig') and area_name is not None:
            name = f"{area_name}.{name}"

        xs_name = XsUtil.constant(name)

        if xs_name in RmsConfig.unique_names:
            raise InvalidCreateObjectError(
                f"[{name}]: group/area with name '{name}' ('{xs_name}') already exists. Make sure all names are unique and "
                f"aren't differentiated through just casing or spaces."
            )
        RmsConfig.unique_names.add(xs_name)

        return xs_name.lower()

    def _is_type(self, type_: str) -> bool:
        """
        Checks the type of self. Cannot use isinstance() as that requires an import of subclasses which will always
        result in a circular import. So... type() string comparison it is, there's better ways but inheritance doesn't
        go further down (as of now). So this suffices.

        Args:
            type_: The type as string to compare

        Returns:
            True if it is the correct type, False otherwise
        """
        return type(self).__name__ == type_

    @staticmethod
    def is_during_area_creation():
        return RmsConfig.current_construction_area_name is not None
