from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms.core.aoe2_scenario_rms import AoE2ScenarioRms
from AoE2ScenarioRms.flags import ObjectClear, TerrainMark, ObjectMark
from examples.create_objects import create_objects_config

filename = "SCENARI_NAME_WITHOUT_EXT"
folder_de = "FOLDER_PATH_WITH_TRAILING_SLASH"
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
