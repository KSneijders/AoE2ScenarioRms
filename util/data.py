from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

player_resources_ids = [
    # Boar like
    UnitInfo.JAVELINA.ID, UnitInfo.WILD_BOAR.ID, UnitInfo.ELEPHANT.ID, UnitInfo.RHINOCEROS.ID,
    # Sheep like
    UnitInfo.SHEEP.ID, UnitInfo.GOAT.ID, UnitInfo.TURKEY.ID, UnitInfo.GOOSE.ID, UnitInfo.PIG.ID,
    UnitInfo.COW_A.ID, UnitInfo.COW_B.ID, UnitInfo.COW_C.ID, UnitInfo.COW_D.ID, UnitInfo.LLAMA.ID,
    # Deer like
    UnitInfo.DEER.ID, UnitInfo.IBEX.ID, UnitInfo.ZEBRA.ID,
    # Wolf like
    UnitInfo.WOLF.ID, UnitInfo.JAGUAR.ID, UnitInfo.LION.ID, UnitInfo.SNOW_LEOPARD.ID,

    # Resources
    OtherInfo.STONE_MINE.ID, OtherInfo.GOLD_MINE.ID, OtherInfo.FORAGE_BUSH.ID, OtherInfo.FRUIT_BUSH.ID
]

tree_ids = [o.ID for o in OtherInfo.trees()]

cliff_ids = [
    264,
    265,
    266,
    267,
    268,
    269,
    270,
    271,
    272,
    1339,
    1340,
    1341,
    1342,
    1344,
    1346
]
