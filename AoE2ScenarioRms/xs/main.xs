bool __AOE2_SCENARIO_RMS_DEBUG = true;
string __AOE2_SCENARIO_RMS_DEBUG_OUTPUT = "file";  /* Either "console" or "file" */

/* REPLACE:AREA_VARIABLE_DECLARATION */
/* REPLACE:RESOURCE_VARIABLE_DECLARATION */

int __AREA_COUNT = /* REPLACE:AREA_VARIABLE_COUNT */;
int __RESOURCE_COUNT = /* REPLACE:RESOURCE_VARIABLE_COUNT */;

// ---------< Other initialization stuff >--------- \\
/* REPLACE:XS_ON_INIT_FILE */

// ---------< Arrays where area ID is value (1D) >--------- \\
int __AREA_SPAWN_COUNTS = -1;
int __AREA_MAX_SPAWN_COUNTS = -1;
int __AREA_BLOCK_RESOURCE_SPAWNS = -1;
int __AREA_GROUP_NAMES = -1;
int __AREA_RESOURCE_COUNTS = -1;

// ---------< Arrays where area ID is reference to other Array (2D) >--------- \\
int __ARRAY_AREA_LOCATIONS = -1;
int __ARRAY_AREA_INDICES = -1;
int __ARRAY_AREA_PLACED = -1;
int __ARRAY_AREA_PLACED_INDICES = -1;
int __ARRAY_AREA_CONFIGS = -1;             // [i][0]: dist self, [i][1]: dist other
int __ARRAY_AREA_PROGRESS = -1;            // [i][0]: placed,    [i][1]: skipped

// ---------< Arrays where area ID is reference to other Array is reference to other Array (3D) >--------- \\
int __ARRAY_AREA_RESOURCE_IDS = -1;        // [areaId][areaIndex][resourceIndex]: resource IDs within area

// ---------< Arrays where resource ID is value (1D) >--------- \\
// Amount of potential spawns per resource
int __RESOURCE_SPAWN_COUNTS = -1;
int __RESOURCE_MAX_SPAWN_COUNTS = -1;
int __RESOURCE_MAX_SPAWN_COUNTS_IS_PER_PLAYER = -1;
int __RESOURCE_GROUP_NAMES = -1;

// ---------< Arrays where resource ID is reference to other Array (2D) >--------- \\
int __ARRAY_RESOURCE_LOCATIONS = -1;
int __ARRAY_RESOURCE_INDICES = -1;
int __ARRAY_RESOURCE_PLACED = -1;
int __ARRAY_RESOURCE_PLACED_INDICES = -1;
int __ARRAY_RESOURCE_CONFIGS = -1;          // [i][0]: dist self, [i][1]: dist other
int __ARRAY_RESOURCE_PROGRESS = -1;         // [i][0]: placed,    [i][1]: skipped

// ---------< Functions >--------- \\
float getXyDistance(vector loc1 = vector(-1, -1, -1), vector loc2 = vector(-1, -1, -1)) {
    float x = pow(xsVectorGetX(loc1) - xsVectorGetX(loc2), 2);
    float y = pow(xsVectorGetY(loc1) - xsVectorGetY(loc2), 2);
    return (sqrt(x + y));
}

string getVectorAsString(vector loc = vector(-1, -1, -1)) {
    return ("x: " + xsVectorGetX(loc) + ", y:" + xsVectorGetY(loc));
}

void disableResourceSpawnsInArea__5986235478(int areaId = -1, int areaIndex = -1) {
    if (areaId == -1 || areaIndex == -1)
        return;

    int resourceCount = xsArrayGetInt(__AREA_RESOURCE_COUNTS, areaId);

    int areaArrayResourceIds = xsArrayGetInt(__ARRAY_AREA_RESOURCE_IDS, areaId);
    int areaResourceIds = xsArrayGetInt(areaArrayResourceIds, areaIndex);

    int resourceId = -1;
    for (i = 0; < resourceCount) {
        resourceId = xsArrayGetInt(areaResourceIds, i);

        xsArraySetInt(__RESOURCE_SPAWN_COUNTS, resourceId, 0);
        xsArraySetInt(__RESOURCE_MAX_SPAWN_COUNTS, resourceId, 0);
    }
}

void __debug__(string message = "") {
    static int l = 0;

    if (__AOE2_SCENARIO_RMS_DEBUG) {

        if (__AOE2_SCENARIO_RMS_DEBUG_OUTPUT == "console") {
            xsChatData("L" + l + ": " + message);

            l++;
        }

        if (__AOE2_SCENARIO_RMS_DEBUG_OUTPUT == "file") {
            static int lines = 0;
            lines++;

            bool success = xsCreateFile(true);

            if (success == false) {
                xsChatData("Opening log file failed");
                return;
            }

            xsWriteString(message);
            xsCloseFile();
        }
    }
}

bool spawnArea__618941981(int areaId = -1) {
    if (areaId == -1)
        return (false);

    string name = xsArrayGetString(__AREA_GROUP_NAMES, areaId);

    int areaSpawnCount = xsArrayGetInt(__AREA_SPAWN_COUNTS, areaId);
    float areaMaxSpawnCount = xsArrayGetFloat(__AREA_MAX_SPAWN_COUNTS, areaId);

    /* TODO: ADD SCALING */

    int areaLocationsArray             = xsArrayGetInt(__ARRAY_AREA_LOCATIONS, areaId);
    int areaIndicesArray               = xsArrayGetInt(__ARRAY_AREA_INDICES, areaId);
    int areaPlacedLocationsArray       = xsArrayGetInt(__ARRAY_AREA_PLACED, areaId);
    int areaPlacedLocationsIndexArray  = xsArrayGetInt(__ARRAY_AREA_PLACED_INDICES, areaId);
    int areaConfigArray                = xsArrayGetInt(__ARRAY_AREA_CONFIGS, areaId);
    int progressArray                  = xsArrayGetInt(__ARRAY_AREA_PROGRESS, areaId);

    int placedAreaCount = xsArrayGetInt(progressArray, 0);
    int skippedAreaCount = xsArrayGetInt(progressArray, 1);
    int startAtIndex = placedAreaCount + skippedAreaCount;

    __debug__("Spawning: " + name + "[ Placed: " + placedAreaCount + ", Skipped: " + skippedAreaCount + " | Max: " + areaSpawnCount + " or " + areaMaxSpawnCount + " ]");

    int minimumDistToSelf = xsArrayGetInt(areaConfigArray, 0);
    int minimumDistToOther = xsArrayGetInt(areaConfigArray, 1);

    for (i = startAtIndex; < areaSpawnCount) {
        Vector v = xsArrayGetVector(areaLocationsArray, i);

        bool allowed = true;
    	for (currAreaId = 0; < __AREA_COUNT) {
			int minDistance = minimumDistToOther;
			if (currAreaId == areaId) {
				minDistance = minimumDistToSelf;
            }

			int otherPlacedLocArray = xsArrayGetInt(__ARRAY_AREA_PLACED, currAreaId);
            int otherProgressArray = xsArrayGetInt(__ARRAY_AREA_PROGRESS, currAreaId);

            int otherPlacedAreasCount = xsArrayGetInt(otherProgressArray, 0);

			bool finished = false;
			for (j = 0; < otherPlacedAreasCount) {
            	Vector v2 = xsArrayGetVector(otherPlacedLocArray, j);

                float d = getXyDistance(v, v2);
                __debug__("["+areaId+"/"+currAreaId+"] Distance between: " + i + " and: " + j + ": " + minDistance + " < " + d);
				if (d < minDistance) {
					allowed = false;
					finished = true;
					break;
				}
			}

			if (finished) {
				break;
			}
		}

        __debug__("["+areaId+"] allowed: " + allowed);
        if (allowed) {
            xsArraySetBool(areaPlacedLocationsIndexArray, xsArrayGetInt(areaIndicesArray, i), true);
            xsArraySetVector(areaPlacedLocationsArray, placedAreaCount, v);
            xsArraySetInt(progressArray, 0, placedAreaCount + 1);

            /* REPLACE:XS_ON_SUCCESSFUL_AREA_SPAWN */

            if (placedAreaCount + 1 >= areaMaxSpawnCount) {

                __debug__(name + " MAX IS REACHED");
                // Next NOT allowed to be placed. Max is reached.
                return (false);
            }

            // Next allowed to be placed because end is not reached yet
            return (true);
        } else {
            disableResourceSpawnsInArea__5986235478(areaId, i);

            xsArraySetInt(progressArray, 1, skippedAreaCount + 1);
        }
    }

    // Next NOT allowed to be placed because the end is reached. Nothing fits anymore.
    __debug__(name + " -> CANT FIT MORE ON MAP");
    return (false);
}

bool spawnResource__024510896(int resourceId = -1) {
    if (resourceId == -1)
        return (false);

    string name = xsArrayGetString(__RESOURCE_GROUP_NAMES, resourceId);

    int resourceSpawnCount = xsArrayGetInt(__RESOURCE_SPAWN_COUNTS, resourceId);
    float resourceMaxSpawnCount = xsArrayGetFloat(__RESOURCE_MAX_SPAWN_COUNTS, resourceId);

    if (xsArrayGetBool(__RESOURCE_MAX_SPAWN_COUNTS_IS_PER_PLAYER, resourceId)) {
        resourceMaxSpawnCount = resourceMaxSpawnCount * xsGetNumPlayers();
    }

    int resourceLocationsArray             = xsArrayGetInt(__ARRAY_RESOURCE_LOCATIONS, resourceId);
    int resourceIndicesArray               = xsArrayGetInt(__ARRAY_RESOURCE_INDICES, resourceId);
    int resourcePlacedLocationsArray       = xsArrayGetInt(__ARRAY_RESOURCE_PLACED, resourceId);
    int resourcePlacedLocationsIndexArray  = xsArrayGetInt(__ARRAY_RESOURCE_PLACED_INDICES, resourceId);
    int resourceConfigArray                = xsArrayGetInt(__ARRAY_RESOURCE_CONFIGS, resourceId);
    int progressArray                      = xsArrayGetInt(__ARRAY_RESOURCE_PROGRESS, resourceId);

    int placedResourcesCount = xsArrayGetInt(progressArray, 0);
    int skippedResourceCount = xsArrayGetInt(progressArray, 1);
    int startAtIndex = placedResourcesCount + skippedResourceCount;

    __debug__("Spawning: " + name + "[ Placed: " + placedResourcesCount + ", Skipped: " + skippedResourceCount + " | Max: " + resourceSpawnCount + " or " + resourceMaxSpawnCount + " ]");

    int minimumDistToSelf = xsArrayGetInt(resourceConfigArray, 0);
    int minimumDistToOther = xsArrayGetInt(resourceConfigArray, 1);

    for (i = startAtIndex; < resourceSpawnCount) {
        Vector v = xsArrayGetVector(resourceLocationsArray, i);
        
        bool allowed = true;
    	for (r = 0; < __RESOURCE_COUNT) {
			int minDistance = minimumDistToOther;
			if (r == resourceId) {
				minDistance = minimumDistToSelf;
            }

			int otherPlacedLocArray = xsArrayGetInt(__ARRAY_RESOURCE_PLACED, r);
            int otherProgressArray = xsArrayGetInt(__ARRAY_RESOURCE_PROGRESS, r);

            int otherPlacedResourcesCount = xsArrayGetInt(otherProgressArray, 0);
			
			bool finished = false;
			for (j = 0; < otherPlacedResourcesCount) {
            	Vector v2 = xsArrayGetVector(otherPlacedLocArray, j);

                float d = getXyDistance(v, v2);
				if (d < minDistance) {
					allowed = false;
					finished = true;
					break;
				}
			}
			
			if (finished) {
				break;
			}
		}

        if (allowed) {
            xsArraySetBool(resourcePlacedLocationsIndexArray, xsArrayGetInt(resourceIndicesArray, i), true);
            xsArraySetVector(resourcePlacedLocationsArray, placedResourcesCount, v);
            xsArraySetInt(progressArray, 0, placedResourcesCount + 1);
            
            /* REPLACE:XS_ON_SUCCESSFUL_RESOURCE_SPAWN */
            
            if (placedResourcesCount + 1 >= resourceMaxSpawnCount) {

                __debug__(name + " -> MAX IS REACHED");
                // Next NOT allowed to be placed. Max is reached.
                return (false);
            }
            
            // Next allowed to be placed because end is not reached yet
            return (true);
        } else {
            xsArraySetInt(progressArray, 1, skippedResourceCount + 1);
        }
    }

    // Next NOT allowed to be placed because the end is reached. Nothing fits anymore.
    __debug__(name + " -> CANT FIT MORE ON MAP");
    return (false);
}

rule main_initialise__023658412
    active
    runImmediately
    minInterval 1
    maxInterval 1
    priority 1000
{
    if (__AOE2_SCENARIO_RMS_DEBUG && __AOE2_SCENARIO_RMS_DEBUG_OUTPUT == "file") {
        xsCreateFile(false);  /* Remove previous debug file*/
        xsCloseFile();
    }

/* REPLACE:XS_ON_INIT_RULE */

    /* ########################################################### */
    /* #######################>>> Areas <<<####################### */
    /* ########################################################### */

    __AREA_GROUP_NAMES = xsArrayCreateString(__AREA_COUNT, "", "__AREA_GROUP_NAMES__245005639");
/* REPLACE:AREA_GROUP_NAMES_DECLARATION */

    __AREA_SPAWN_COUNTS = xsArrayCreateInt(__AREA_COUNT, -1, "__AREA_SPAWN_COUNTS__502659885");
/* REPLACE:AREA_COUNT_DECLARATION */

    __AREA_MAX_SPAWN_COUNTS = xsArrayCreateFloat(__AREA_COUNT, -1, "__AREA_MAX_SPAWN_COUNTS__754202236");
/* REPLACE:AREA_MAX_SPAWN_DECLARATION */

    __AREA_BLOCK_RESOURCE_SPAWNS = xsArrayCreateBool(__AREA_COUNT, false, "__AREA_BLOCK_RESOURCE_SPAWNS__51248775");
/* REPLACE:AREA_BLOCK_RESOURCE_SPAWNS_DECLARATION */

    __AREA_RESOURCE_COUNTS = xsArrayCreateInt(__AREA_COUNT, 0, "__AREA_RESOURCE_COUNTS__581465840");
/* REPLACE:AREA_RESOURCE_COUNTS_DECLARATION */

    __ARRAY_AREA_LOCATIONS          = xsArrayCreateInt(__AREA_COUNT, -1, "__ARRAY_AREA_LOCATIONS__658595235");
    __ARRAY_AREA_INDICES            = xsArrayCreateInt(__AREA_COUNT, -1, "__ARRAY_AREA_INDICES__316452948");
    __ARRAY_AREA_PLACED             = xsArrayCreateInt(__AREA_COUNT, -1, "__ARRAY_AREA_PLACED__002452896");
    __ARRAY_AREA_PLACED_INDICES     = xsArrayCreateInt(__AREA_COUNT, -1, "__ARRAY_AREA_PLACED_INDICES__653512128");
    __ARRAY_AREA_CONFIGS            = xsArrayCreateInt(__AREA_COUNT, -1, "__ARRAY_AREA_CONFIGS__658921548");
    __ARRAY_AREA_PROGRESS           = xsArrayCreateInt(__AREA_COUNT, -1, "__ARRAY_AREA_PROGRESS__211153268");

    /* [3D] Create __ARRAY_AREA_RESOURCE_IDS[x] (Entry Per Area Type) */
    __ARRAY_AREA_RESOURCE_IDS       = xsArrayCreateInt(__AREA_COUNT, -1, "__ARRAY_AREA_RESOURCE_IDS__568820591");

    int areaCount = -1;
    int areaResourceCount = -1;
    for (i = 0; < __AREA_COUNT) {
        areaCount = xsArrayGetInt(__AREA_SPAWN_COUNTS, i);
        areaResourceCount = xsArrayGetInt(__AREA_RESOURCE_COUNTS, i);

        int areaArray            = xsArrayCreateVector(areaCount, vector(-1, -1, -1), "areaArray__582659358__v" + i);
        int areaIndexArray       = xsArrayCreateInt(areaCount, -1, "areaIndexArray__052691427__v" + i);
        int areaPlaced           = xsArrayCreateVector(areaCount, vector(-1, -1, -1), "areaPlaced__026358320__v" + i);
        int areaIndexPlaced      = xsArrayCreateBool(areaCount, false, "areaIndexPlaced__963630218__v" + i);
        int areaConfig           = xsArrayCreateInt(2, -1, "areaConfig__264812522__v" + i);
        int areaProgress         = xsArrayCreateInt(2, 0, "areaProgress__536248009__v" + i);

        /* [3D] Create __ARRAY_AREA_RESOURCE_IDS[x][y] (Entry Per Area Index) */
        int areaArrayResourceIds = xsArrayCreateInt(areaCount, 0, "areaArrayResourceIds__358154580__v" + i);

        for (areaIndex = 0; < areaCount) {
            xsArraySetInt(areaIndexArray, areaIndex, areaIndex);

            /* [3D] Create __ARRAY_AREA_RESOURCE_IDS[x][y][z] (Entry Per Resource In Single Area Index) */
            int resourceIdsInSingleArea = xsArrayCreateInt(areaResourceCount, 0, "resourceIdsInSingleArea__952475691__v" + i + "_" + areaIndex);
            xsArraySetInt(areaArrayResourceIds, areaIndex, resourceIdsInSingleArea);
        }

        xsArraySetInt(__ARRAY_AREA_LOCATIONS,      i, areaArray);
        xsArraySetInt(__ARRAY_AREA_INDICES,        i, areaIndexArray);
        xsArraySetInt(__ARRAY_AREA_PLACED,         i, areaPlaced);
        xsArraySetInt(__ARRAY_AREA_PLACED_INDICES, i, areaIndexPlaced);
        xsArraySetInt(__ARRAY_AREA_CONFIGS,        i, areaConfig);
        xsArraySetInt(__ARRAY_AREA_PROGRESS,       i, areaProgress);
        xsArraySetInt(__ARRAY_AREA_RESOURCE_IDS,   i, areaArrayResourceIds);
    }

    /*                                      S                                                      */
    /*                                        E                                                    */
    /*                                          P                                                  */
    /*                                            A                                                */
    /*                                              R                                              */
    /*                                                A                                            */
    /*                                                  T                                          */
    /*                                                    O                                        */
    /*                                                      R                                      */

    /* ############################################################### */
    /* #######################>>> Resources <<<####################### */
    /* ############################################################### */

    __RESOURCE_GROUP_NAMES = xsArrayCreateString(__RESOURCE_COUNT, "", "__RESOURCE_GROUP_NAMES__594522389");
/* REPLACE:RESOURCE_GROUP_NAMES_DECLARATION */

    __RESOURCE_SPAWN_COUNTS = xsArrayCreateInt(__RESOURCE_COUNT, -1, "__RESOURCE_SPAWN_COUNTS__538652012");
/* REPLACE:RESOURCE_COUNT_DECLARATION */

    __RESOURCE_MAX_SPAWN_COUNTS = xsArrayCreateFloat(__RESOURCE_COUNT, -1, "__RESOURCE_MAX_SPAWN_COUNTS__503956013");
/* REPLACE:RESOURCE_MAX_SPAWN_DECLARATION */

    __RESOURCE_MAX_SPAWN_COUNTS_IS_PER_PLAYER = xsArrayCreateBool(__RESOURCE_COUNT, false, "__RESOURCE_MAX_SPAWN_COUNTS_IS_PER_PLAYER__024698552");
/* REPLACE:RESOURCE_MAX_SPAWN_IS_PER_PLAYER_DECLARATION */

    __ARRAY_RESOURCE_LOCATIONS      = xsArrayCreateInt(__RESOURCE_COUNT, -1, "__ARRAY_RESOURCE_LOCATIONS__056985215");
    __ARRAY_RESOURCE_INDICES        = xsArrayCreateInt(__RESOURCE_COUNT, -1, "__ARRAY_RESOURCE_INDICES__021548785");
    __ARRAY_RESOURCE_PLACED         = xsArrayCreateInt(__RESOURCE_COUNT, -1, "__ARRAY_RESOURCE_PLACED__542150369");
    __ARRAY_RESOURCE_PLACED_INDICES = xsArrayCreateInt(__RESOURCE_COUNT, -1, "__ARRAY_RESOURCE_PLACED_INDICES__520001548");
    __ARRAY_RESOURCE_CONFIGS        = xsArrayCreateInt(__RESOURCE_COUNT, -1, "__ARRAY_RESOURCE_CONFIGS__522094889");
    __ARRAY_RESOURCE_PROGRESS       = xsArrayCreateInt(__RESOURCE_COUNT, -1, "__ARRAY_RESOURCE_PROGRESS__510369984");

    int resourceCount = -1;
    for (i = 0; < __RESOURCE_COUNT) {
        resourceCount = xsArrayGetInt(__RESOURCE_SPAWN_COUNTS, i);

        int resourceArray       = xsArrayCreateVector(resourceCount, vector(-1, -1, -1), "resourceArray__352901574__v" + i);
        int resourceIndexArray  = xsArrayCreateInt(resourceCount, -1, "resourceIndexArray__456875221__v" + i);
        int resourcePlaced      = xsArrayCreateVector(resourceCount, vector(-1, -1, -1), "resourcePlaced__548476523__v" + i);
        int resourceIndexPlaced = xsArrayCreateBool(resourceCount, false, "resourceIndexPlaced__301548796__v" + i);
        int resourceConfig      = xsArrayCreateInt(2, -1, "resourceConfig__985256327__v" + i);
        int resourceProgress    = xsArrayCreateInt(2, 0, "resourceProgress__524875963__v" + i);

        for (resourceIndex = 0; < resourceCount) {
            xsArraySetInt(resourceIndexArray, resourceIndex, resourceIndex);
        }

        xsArraySetInt(__ARRAY_RESOURCE_LOCATIONS,      i, resourceArray);
        xsArraySetInt(__ARRAY_RESOURCE_INDICES,        i, resourceIndexArray);
        xsArraySetInt(__ARRAY_RESOURCE_PLACED,         i, resourcePlaced);
        xsArraySetInt(__ARRAY_RESOURCE_PLACED_INDICES, i, resourceIndexPlaced);
        xsArraySetInt(__ARRAY_RESOURCE_CONFIGS,        i, resourceConfig);
        xsArraySetInt(__ARRAY_RESOURCE_PROGRESS,       i, resourceProgress);
    }
    int tempArray = -1;
    int temp2Array = -1;
/* REPLACE:AREA_CONFIG_DECLARATION */
/* REPLACE:RESOURCE_CONFIG_DECLARATION */

    int rArray = -1;
/* REPLACE:AREA_LOCATION_INJECTION */
/* REPLACE:RESOURCE_LOCATION_INJECTION */

    /* ############################################################## */
    /* #######################>>> SPAWNING <<<####################### */
    /* ############################################################## */

    string name = "";
    int progressArray = -1;
    int placedResourcesCount = -1;

    bool success = true;
    for (areaId = 0; < __AREA_COUNT) {
        success = true;

        while (success) {
            success = spawnArea__618941981(areaId);
        }

        progressArray = xsArrayGetInt(__ARRAY_AREA_PROGRESS, areaId);
        name = xsArrayGetString(__AREA_GROUP_NAMES, areaId);
        placedResourcesCount = xsArrayGetInt(progressArray, 0);

        __debug__("Area `" + name + "` spawned " + placedResourcesCount + " successfully!");


        /* REPLACE:AFTER_AREA_SPAWN_EVENT */
    }

    for (resourceId = 0; < __RESOURCE_COUNT) {
        success = true;

        while (success) {
            success = spawnResource__024510896(resourceId);
        }

        progressArray = xsArrayGetInt(__ARRAY_RESOURCE_PROGRESS, resourceId);
        name = xsArrayGetString(__RESOURCE_GROUP_NAMES, resourceId);
        placedResourcesCount = xsArrayGetInt(progressArray, 0);

        __debug__("Group `" + name + "` spawned " + placedResourcesCount + " successfully!");


        /* REPLACE:AFTER_RESOURCE_SPAWN_EVENT */
    }

    xsDisableSelf();
}
