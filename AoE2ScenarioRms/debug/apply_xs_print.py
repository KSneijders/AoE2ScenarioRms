from AoE2ScenarioRms import AoE2ScenarioRms
from AoE2ScenarioRms.debug.apply_debug import ApplyDebug
from AoE2ScenarioRms.enums import XsKey
from AoE2ScenarioRms.util import XsUtil


class ApplyXsPrint(ApplyDebug):
    def __init__(self, rms: AoE2ScenarioRms) -> None:
        rms.container.extend(
            XsKey.AFTER_RESOURCE_SPAWN_EVENT,
            XsUtil.read('snippets/debug_print_info.xs').splitlines()
        )
