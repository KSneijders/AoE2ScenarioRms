from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms import AoE2ScenarioRms
from AoE2ScenarioRms.debug import ApplyAllVisible, ApplyNoClutter, ApplyXsPrint
from AoE2ScenarioRms.flags import ObjectClear, TerrainMark, ObjectMark
from AoE2ScenarioRms.util import ScenarioUtil, GridMapFactory
from examples.create_objects import create_objects_config

# Read scenario like usual
filename = "SCENARIO_NAME_WITHOUT_EXT"
folder_de = "FOLDER_PATH_WITH_TRAILING_SLASH"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")

# Give the scenario to the module
asr = AoE2ScenarioRms(scenario)

# Clear the scenario of all unwanted (some to be generated) objects (except for cliffs in this example)
ScenarioUtil.clear(scenario, ObjectClear.ALL & ~ObjectClear.CLIFFS)

# Mark terrain for placing the objects.
# A 'blocked' tile means resources cannot spawn there.
# In this example all water and beach terrains are blocked
# On top of that, all trees (forests) and cliffs are also blocked with a radius of 1 around them (default)
grid_map = GridMapFactory.default(
    scenario=scenario,
    terrain_marks=TerrainMark.water_beach(),
    object_marks=ObjectMark.all(),
)

# Throw in the create_object_config (Can be found in the other example file)
asr.create_objects(create_objects_config, grid_map)

# Apply debug options to the scenario.
# These can only be applied at the end of the script (before scenario.write_to_file)
# Please refer to the docstrings of these classes (and others) to see their use cases
ApplyAllVisible(asr)
ApplyNoClutter(asr)
ApplyXsPrint(asr)

# Write the scenario like normal
scenario.write_to_file(f"{folder_de}!{filename}_written.aoe2scenario")
