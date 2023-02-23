from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms import AoE2ScenarioRms
from AoE2ScenarioRms.flags import ObjectClear, TerrainMark, ObjectMark, Debug
from examples.create_objects import create_objects_config

# Read scenario like usual
filename = "SCENARIO_NAME_WITHOUT_EXT"
folder_de = "FOLDER_PATH_WITH_TRAILING_SLASH"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")

# Give the scenario to the module and enable debug aspects.
# Debug options (and their use-cases) can be found in the Debug class (see import)
asr = AoE2ScenarioRms(scenario, debug=Debug.ALL_VISIBLE | Debug.XS_PRINT | Debug.NO_CLUTTER)

# Clear the scenario of all unwanted (some to be generated) objects (except for cliffs in this example)
asr.clear_scenario(ObjectClear.ALL & ~ObjectClear.CLIFFS)

# Mark terrain for placing the objects.
# A 'blocked' tile means resources cannot spawn there.
# In this example all water and beach terrains are blocked
# On top of that, all trees (forests) and cliffs are also blocked with a radius of 1 around them (default)
asr.mark_blocked_tiles(
    terrain_marks=TerrainMark.water_beach(),
    object_marks=ObjectMark.all(),
)

# Throw in the create_object_config (Can be found in the other example file)
asr.create_objects(create_objects_config)

# Write everything to a script and save it in the scenario (this will be changed in the future)
script = asr.write()
scenario.xs_manager.add_script(xs_string=script)

# Write the scenario like normal
scenario.write_to_file(f"{folder_de}!{filename}_written.aoe2scenario")
