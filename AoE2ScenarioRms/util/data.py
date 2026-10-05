from typing import List

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.units import UnitInfo

from AoE2ScenarioRms.flags.object_clear import ObjectClear
from AoE2ScenarioRms.flags.terrain_mark import TerrainMark


class Data:
    """
    Static class that holds functions that return specific data, mainly IDs used for removal of objects or marking of a
    scenario.
    """
    @staticmethod
    def trees() -> List[int]:
        """
        Returns:
            A list of all tree object IDs
        """
        return [o.ID for o in OtherInfo.trees()]

    @staticmethod
    def cliffs() -> List[int]:
        """
        Returns:
            A list of all cliff IDs
        """
        return [
            264, 265, 266, 267, 268, 269, 270, 271, 272,
            1339, 1340, 1341, 1342, 1344, 1346
        ]

    @staticmethod
    def get_terrain_ids_by_terrain_marks(marks: TerrainMark) -> List[TerrainId]:
        """
        Args:
            marks: The marks to take into account

        Returns:
            A list of Terrain Ids based on the marks given
        """
        ids: List[TerrainId] = []

        if TerrainMark.WATER in marks:
            ids.extend(TerrainId.water_terrains())
        if TerrainMark.BEACH in marks:
            ids.extend(TerrainId.beach_terrains())
        if TerrainMark.LAND in marks:
            water_beach = TerrainId.water_terrains() + TerrainId.beach_terrains()
            ids.extend(terrain for terrain in TerrainId if terrain not in water_beach)

        return ids

    @staticmethod
    def get_object_consts_by_clear_options(clear: ObjectClear) -> List[int]:
        """
        Args:
            clear: The ``ObjectClear`` configuration used for removing objects from a scenario

        Returns:
            A list of IDs of object consts used for the removal of objects
        """
        consts: List[int] = []

        if ObjectClear.BOARS in clear:
            consts.extend([
                UnitInfo.WILD_BOAR.ID,
                UnitInfo.IRON_BOAR.ID,
                UnitInfo.JAVELINA.ID,
                UnitInfo.ELEPHANT.ID,
                UnitInfo.RHINOCEROS.ID,
                UnitInfo.TAPIR.ID,
                # Not yet in UnitInfo (AoE2ScenarioParser v0.9.4) -- raw object IDs
                2737,  # Elk
                1924,  # Walrus
            ])

        if ObjectClear.SHEEP in clear:
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
                UnitInfo.LLAMA_A.ID,
                UnitInfo.LLAMA_B.ID,
            ])

        if ObjectClear.CHICKENS in clear:
            consts.extend([
                UnitInfo.HARE_A.ID,
                UnitInfo.HARE_B.ID,
                UnitInfo.ARCTIC_HARE.ID,
                UnitInfo.WILD_CHICKEN_A.ID,
                UnitInfo.WILD_CHICKEN_B.ID,
                UnitInfo.WILD_CHICKEN_C.ID,
                UnitInfo.PEACOCK.ID,
                # Not yet in UnitInfo (AoE2ScenarioParser v0.9.4) -- raw object IDs
                2739,  # Pheasant
            ])

        if ObjectClear.FOXES in clear:
            consts.extend([
                UnitInfo.RED_FOX.ID,
                UnitInfo.ARCTIC_FOX.ID,
            ])

        if ObjectClear.DEER in clear:
            consts.extend([
                UnitInfo.DEER.ID,
                UnitInfo.IBEX.ID,
                UnitInfo.ZEBRA.ID,
                UnitInfo.GAZELLE.ID,
                UnitInfo.ARGALI.ID,
                UnitInfo.MOUFLON.ID,
                UnitInfo.GUANACO.ID,
                UnitInfo.OSTRICH.ID,
                UnitInfo.RHEA.ID,
                # Not yet in UnitInfo (AoE2ScenarioParser v0.9.4) -- raw object IDs
                2735,  # Seal
            ])

        if ObjectClear.WOLFS in clear:
            consts.extend([
                UnitInfo.GREY_WOLF.ID,
                UnitInfo.DIRE_WOLF.ID,
                UnitInfo.RABID_WOLF.ID,
                UnitInfo.ARABIAN_WOLF.ID,
                UnitInfo.ARCTIC_WOLF.ID,
                UnitInfo.JAGUAR.ID,
                UnitInfo.LION.ID,
                UnitInfo.SNOW_LEOPARD.ID,
                UnitInfo.CROCODILE.ID,
                UnitInfo.BROWN_BEAR.ID,
                UnitInfo.BLACK_BEAR.ID,
                UnitInfo.POLAR_BEAR.ID,
                # Not yet in UnitInfo (AoE2ScenarioParser v0.9.4) -- raw object IDs
                2736,  # Lynx
            ])

        if ObjectClear.RELICS in clear:
            consts.append(OtherInfo.RELIC.ID)

        if ObjectClear.GOLDS in clear:
            consts.append(OtherInfo.GOLD_MINE.ID)

        if ObjectClear.STONES in clear:
            consts.append(OtherInfo.STONE_MINE.ID)

        if ObjectClear.BUSHES in clear:
            consts.extend([
                OtherInfo.FORAGE_BUSH.ID,
                OtherInfo.FRUIT_BUSH.ID,
                OtherInfo.PAPAYA_TREE.ID,
            ])

        if ObjectClear.CLIFFS in clear:
            consts.extend(Data.cliffs())

        if ObjectClear.DEEP_FISH in clear:
            consts.extend([
                OtherInfo.FISH_TUNA.ID,
                OtherInfo.FISH_PERCH.ID,
                OtherInfo.FISH_DORADO.ID,
                OtherInfo.FISH_SALMON.ID,
                OtherInfo.FISH_SNAPPER.ID,
                OtherInfo.GREAT_FISH_MARLIN.ID,
                OtherInfo.DOLPHIN.ID,
            ])

        if ObjectClear.SHORE_FISH in clear:
            consts.extend([
                OtherInfo.SHORE_FISH.ID,
                OtherInfo.BOX_TURTLES.ID,
            ])

        return consts
