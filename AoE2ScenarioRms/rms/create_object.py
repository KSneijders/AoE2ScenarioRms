from __future__ import annotations

import math

from AoE2ScenarioParser.helper.printers import warn

from AoE2ScenarioRms.util.exceptions import ImproperCreateObjectError
from AoE2ScenarioRms.util.warnings import ImproperCreateObjectWarning
from AoE2ScenarioRms.enums.grouping_method import GroupingMethod


class CreateObject:
    """
    An object that holds the configuration of a single object group

    *An effort was made to make these keys to be somewhat the same to RMS `<create_object>` options.*

    ----

    Usual configuration.

    ----

    **name**:
        **[REQUIRED]** The name for this config, needs to be unique

    **object**:
        **[REQUIRED]** The unit to spawn

    **grouping**:
        The spread method. Use: ``GroupingMethod.TIGHT`` for spawning like gold, or: ``GroupingMethod.LOOSE`` for
        spawning like deer. Defaults to: ``GroupingMethod.TIGHT``

    **number_of_objects**:
        The size of a single group (Amount of objects per group).
        Accepts an ``int`` or a ``tuple[int, int]`` indicating a range ([1, 3] can spawn 1, 2 or 3 objects in a group).
        This value randomized per group so is useful for spawning equal resources. Defaults to 1

    **group_placement_radius**:
        **[NOT IMPLEMENTED]** The number of tiles out from the central tile that objects belonging to the same group
        may spawn. Defaults to 3

    **number_of_groups**:
        The maximum amount of groups to spawn. Can be a float when using `scale_to_player_number`. When left unchanged
        the maximum amount of spawns will be the maximum of groups that fits in the map. Defaults to infinity

    **loose_grouping_distance**:
        The distance at which resources should spawn from each other in the same group. Ignored when ``grouping`` is
        not set to ``GroupingMethod.LOOSE``. Defaults to 3

    **min_distance_group_placement**:
        The minimum distance in tiles to groups of OTHER create object config

    **temp_min_distance_group_placement**:
        The minimum distance in tiles to groups of THIS create object config

    **min_distance_to_map_edge**:
        **[NOT IMPLEMENTED]** The minimum distance in tiles that groups will stay away from the map edge

    **scale_to_player_number**:
        If the number of groups should be affected by the player number. When set to True, the number_of_groups value
        is multiplied with the number of players
        With this enabled and ... (Examples)::
           ... 'number_of_groups' to 3 with 2 players will result in 6 spawns
           ... 'number_of_groups' to 0.5 with 6 players will result in 3 spawns
           ... 'number_of_groups' to 0.4 with 1, 2 or 3 player(s) will all result in a single spawn

    ----

    Parser related configurations

    ----

    These configuration settings affect how the groups are generated **IN THE SCENARIO**. This means these settings will
    affect the triggers and XS generated. *Leave as-is if you don't know what they do*

    **_max_potential_group_count**:
        [PARSER GENERATION] The total amount of groups to **generate** on a map

    **_debug_place_all**:
        [DEBUG] Force all groups to be placed directly in the map. Not recommended with a high
        ``_max_potential_group_count``!
    """

    def __init__(
            self,
            name: str,
            object: int,
            grouping: GroupingMethod = GroupingMethod.TIGHT,
            number_of_objects: int | tuple[int, int] = 1,
            group_placement_radius: int = 3,
            number_of_groups: float = math.inf,  # Limited by `_max_potential_group_count`
            loose_grouping_distance: int = None,
            min_distance_group_placement: int = 4,
            temp_min_distance_group_placement: int = 20,
            min_distance_to_map_edge: int = 0,
            scale_to_player_number: bool = False,

            _max_potential_group_count: int = 250,
            _debug_place_all: bool = False
    ):
        if scale_to_player_number and number_of_groups == math.inf:
            raise ImproperCreateObjectError(f"[{name}]: cannot scale infinity with player numbers. "
                                            f"Please specify 'number_of_groups'")

        if not isinstance(number_of_objects, int) and not isinstance(number_of_objects, tuple):
            raise TypeError(f"[{name}]: number_of_objects has to be either int or tuple[int, int], "
                            f"not: {type(number_of_objects)}.")

        if grouping is not GroupingMethod.LOOSE and loose_grouping_distance is not None:
            warn(f"[{name}]: Setting 'loose_grouping_distance' without GroupingMethod.LOOSE has no effect",
                 ImproperCreateObjectWarning)

        if loose_grouping_distance is None:
            loose_grouping_distance = 3

        self.name: str = name
        self.object: int = object
        self.grouping: GroupingMethod = grouping
        self.number_of_objects: int | tuple[int, int] = number_of_objects
        self.group_placement_radius: int = group_placement_radius  # Todo: Implement
        self.number_of_groups: float = number_of_groups
        self.loose_grouping_distance: int = loose_grouping_distance
        self.min_distance_group_placement: int = min_distance_group_placement
        self.temp_min_distance_group_placement: int = temp_min_distance_group_placement
        self.min_distance_to_map_edge: int = min_distance_to_map_edge  # Todo: Implement
        self.scale_to_player_number: bool = scale_to_player_number

        self.max_potential_group_count: int = _max_potential_group_count
        self.debug_place_all: bool = _debug_place_all
