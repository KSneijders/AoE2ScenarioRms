"""
> THIS FILE WILL BE REMOVED IN THE FUTURE <
"""
from __future__ import annotations

import random
import sys

from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms import AoE2ScenarioRms
from AoE2ScenarioRms.debug import mark_blocked_terrain_as_black, remove_terrain_layers
from AoE2ScenarioRms.flags import ObjectClear, TerrainMark, ObjectMark
from AoE2ScenarioRms.local_config import folder_de
from examples.create_objects import create_objects_config

seed = random.randrange(sys.maxsize)
seed = 7647799647017082024
random.seed(seed)
print("Seed:", seed)

filename = "defense2"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")

asr = AoE2ScenarioRms(scenario, debug=True)

asr.clear_scenario(ObjectClear.ALL & ~ObjectClear.CLIFFS)
asr.mark_blocked_tiles(
    terrain_marks=TerrainMark.water_beach(),
    object_marks=ObjectMark.all(),
)
asr.create_objects(create_objects_config)

script = asr.write()
scenario.xs_manager.add_script(xs_string=script)

scenario.write_to_file(f"{folder_de}!{filename}_written.aoe2scenario")
