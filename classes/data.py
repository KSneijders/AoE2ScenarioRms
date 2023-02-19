from typing import List

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.units import UnitInfo

from flags.clear_options import ObjectClear
from flags.object_marks import ObjectMark
from flags.terrain_mark import TerrainMark


class Data:
    @staticmethod
    def trees() -> List[int]:
        return [o.ID for o in OtherInfo.trees()]

    @staticmethod
    def cliffs() -> List[int]:
        return [
            264, 265, 266, 267, 268, 269, 270, 271, 272,
            1339, 1340, 1341, 1342, 1344, 1346
        ]

    @staticmethod
    def get_terrain_ids_by_terrain_marks(marks: TerrainMark) -> List[TerrainId]:
        ids: List[int] = []

        if marks & TerrainMark.WATER:
            ids.extend(TerrainId.water_terrains())
        if marks & TerrainMark.BEACH:
            ids.extend(TerrainId.beach_terrains())
        if marks & TerrainMark.LAND:
            water_beach = TerrainId.water_terrains() + TerrainId.beach_terrains()
            ids.extend(terrain for terrain in TerrainId if terrain not in water_beach)

        return ids

    @staticmethod
    def get_object_consts_by_clear_options(clear: ObjectClear) -> List[int]:
        consts = []

        if clear & ObjectClear.BOARS:
            consts.extend([
                UnitInfo.JAVELINA.ID,
                UnitInfo.WILD_BOAR.ID,
                UnitInfo.ELEPHANT.ID,
                UnitInfo.RHINOCEROS.ID
            ])

        if clear & ObjectClear.SHEEP:
            consts.extend([
                UnitInfo.SHEEP.ID,
                UnitInfo.GOAT.ID,
                UnitInfo.TURKEY.ID,
                UnitInfo.GOOSE.ID,
                UnitInfo.PIG.ID,
                UnitInfo.COW_A.ID,
                UnitInfo.COW_B.ID,
                UnitInfo.COW_C.ID,
                UnitInfo.COW_D.ID,
                UnitInfo.LLAMA.ID
            ])

        if clear & ObjectClear.DEER:
            consts.extend([
                UnitInfo.DEER.ID,
                UnitInfo.IBEX.ID,
                UnitInfo.ZEBRA.ID
            ])

        if clear & ObjectClear.WOLFS:
            consts.extend([
                UnitInfo.WOLF.ID,
                UnitInfo.JAGUAR.ID,
                UnitInfo.LION.ID,
                UnitInfo.SNOW_LEOPARD.ID
            ])

        if clear & ObjectClear.RELICS:
            consts.append(OtherInfo.RELIC.ID)

        if clear & ObjectClear.GOLDS:
            consts.append(OtherInfo.GOLD_MINE.ID)

        if clear & ObjectClear.STONES:
            consts.append(OtherInfo.STONE_MINE.ID)

        if clear & ObjectClear.BUSHES:
            consts.extend([
                OtherInfo.FORAGE_BUSH.ID,
                OtherInfo.FRUIT_BUSH.ID
            ])

        if clear & ObjectClear.CLIFFS:
            consts.extend(Data.cliffs())

        return consts
