from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2ScenarioRms import AoE2ScenarioRms
from AoE2ScenarioRms.debug import ApplyAllVisible, ApplyNoClutter, ApplyXsPrint
from AoE2ScenarioRms.flags import ObjectClear, TerrainMark, ObjectMark
from AoE2ScenarioRms.util import ScenarioUtil, GridMapFactory
from examples.create_objects import create_objects_config, create_objects_config_shore_fish, \
    create_objects_config_deep_fish

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
grid_map = GridMapFactory.block(
    scenario=scenario,
    terrain_marks=TerrainMark.WATER_BEACH,
    object_marks=ObjectMark.ALL,
)
# Throw in the create_object_config (Can be found in the other example file) to start calculating spawn positions
# and add triggers and XS
asr.create_objects(create_objects_config, grid_map)

# In this example is only 'shore' terrain marked. This means only water tiles that are directly next to a beach tile.
# Notice the function `select(...)` is used because when using block(...), a gridmap marks it to not be spawn-able,
# but we want only the shore and nothing else, so we need to NOT block the mark tiles. So now it's the other way around.
# Everything will be blocked except for the tiles we mark
grid_map = GridMapFactory.select(
    scenario=scenario,
    terrain_marks=TerrainMark.SHORE,
)
asr.create_objects(create_objects_config_shore_fish, grid_map)

# Get only the water and place the deep fish in there.
# PLEASE NOTE: PLACING NON 1X1 OBJECTS IS CURRENTLY NOT TAKEN INTO ACCOUNT WHEN PLACING. (This is a known issue)
# So even though the selection does NOT include TerrainMark.SHORE, deep fish can sometimes still be reached by vills
grid_map = GridMapFactory.select(
    scenario=scenario,
    terrain_marks=TerrainMark.WATER,
)
asr.create_objects(create_objects_config_deep_fish, grid_map)

# Apply debug options to the scenario.
# These can only be applied at the end of the script (before scenario.write_to_file)
# Please refer to the docstrings of these classes (and others) to see their use cases
ApplyAllVisible(asr)
ApplyNoClutter(asr)
ApplyXsPrint(asr)

# Write the scenario like normal
scenario.write_to_file(f"{folder_de}!{filename}_written.aoe2scenario")
