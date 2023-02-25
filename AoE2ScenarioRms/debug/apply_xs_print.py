from typing import TYPE_CHECKING

from AoE2ScenarioRms.debug.apply_debug import ApplyDebug
from AoE2ScenarioRms.enums import XsKey
from AoE2ScenarioRms.util import XsUtil

if TYPE_CHECKING:
    from AoE2ScenarioRms import AoE2ScenarioRms


class ApplyXsPrint(ApplyDebug):
    def __init__(self, rms: 'AoE2ScenarioRms') -> None:
        rms.container.extend(
            XsKey.AFTER_RESOURCE_SPAWN_EVENT,
            XsUtil.read('snippets/debug_print_info.xs').splitlines()
        )
