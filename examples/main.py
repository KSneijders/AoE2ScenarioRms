"""
# THIS IS A WORK IN PROGRESS

It is possible that not everything shown in thi example works already.
It might be a goal or experiment (it might be mentioned what is working and what is not, but it also might not...)

"""
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.classes import AoE2ScenarioRms
from AoE2ScenarioRms.flags import ObjectClear, TerrainMark, ObjectMark
from AoE2ScenarioRms.local_config import folder_de

filename = "defense2"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")

asr = AoE2ScenarioRms(scenario, debug=True)

asr.clear_scenario(ObjectClear.ALL & ~ObjectClear.CLIFFS)

asr.mark_blocked_tiles()
asr.resolve(...)

scenario.write_to_file(f"{folder_de}!{filename}_written.aoe2scenario")
