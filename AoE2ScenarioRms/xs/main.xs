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

// ---------< Arrays where area ID is reference to other Array (2D) >--------- \\
int __ARRAY_AREA_LOCATIONS = -1;
int __ARRAY_AREA_INDICES = -1;
int __ARRAY_AREA_PLACED = -1;
int __ARRAY_AREA_PLACED_INDICES = -1;
int __ARRAY_AREA_CONFIGS = -1;             // [i][0]: dist self, [i][1]: dist other
int __ARRAY_AREA_PROGRESS = -1;            // [i][0]: placed,    [i][1]: skipped

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

bool spawnArea__618941981(int areaId = -1) {
    if (areaId == -1)
        return (false);

    /* -- Implement -- */

    return (false);
}

bool spawnResource__024510896(int resourceId = -1) {
    if (resourceId == -1)
        return (false);

    int resourceSpawnCount = xsArrayGetInt(__RESOURCE_SPAWN_COUNTS, resourceId);
    float resourceMaxSpawnCount = xsArrayGetFloat(__RESOURCE_MAX_SPAWN_COUNTS, resourceId);

    if (xsArrayGetBool(__RESOURCE_MAX_SPAWN_COUNTS_IS_PER_PLAYER, resourceId)) {
        resourceMaxSpawnCount = resourceMaxSpawnCount * xsGetNumPlayers();
    }

    int resourceLocationsArray             = xsArrayGetInt(__ARRAY_RESOURCE_LOCATIONS, resourceId);
    int resourceIndexsArray               = xsArrayGetInt(__ARRAY_RESOURCE_INDICES, resourceId);
    int resourcePlacedLocationsArray       = xsArrayGetInt(__ARRAY_RESOURCE_PLACED, resourceId);
    int resourcePlacedLocationsIndexArray = xsArrayGetInt(__ARRAY_RESOURCE_PLACED_INDICES, resourceId);
    int resourceConfigArray                = xsArrayGetInt(__ARRAY_RESOURCE_CONFIGS, resourceId);
    int progressArray                      = xsArrayGetInt(__ARRAY_RESOURCE_PROGRESS, resourceId);

    int placedResourcesCount = xsArrayGetInt(progressArray, 0);
    int skippedResourceCount = xsArrayGetInt(progressArray, 1);
    int startAtIndex = placedResourcesCount + skippedResourceCount;

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
            xsArraySetBool(resourcePlacedLocationsIndexArray, xsArrayGetInt(resourceIndexsArray, i), true);
            xsArraySetVector(resourcePlacedLocationsArray, placedResourcesCount, v);
            xsArraySetInt(progressArray, 0, placedResourcesCount + 1);
            
            /* REPLACE:XS_ON_SUCCESSFUL_SPAWN */
            
            if (placedResourcesCount + 1 >= resourceMaxSpawnCount) {
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
    return (false);
}

rule main_initialise__023658412
    active
    runImmediately
    minInterval 1
    maxInterval 1
    priority 1000
{
    int count = -1;

/* REPLACE:XS_ON_INIT_RULE */

    /* #######################>>> Areas <<<####################### */

    __AREA_GROUP_NAMES = xsArrayCreateString(__AREA_COUNT, "", "__AREA_GROUP_NAMES__245005639");
/* REPLACE:AREA_GROUP_NAMES_DECLARATION */

    __AREA_SPAWN_COUNTS = xsArrayCreateInt(__AREA_COUNT, -1, "__AREA_SPAWN_COUNTS__502659885");
/* REPLACE:AREA_COUNT_DECLARATION */

    __AREA_MAX_SPAWN_COUNTS = xsArrayCreateFloat(__AREA_COUNT, -1, "__AREA_MAX_SPAWN_COUNTS__754202236");
/* REPLACE:AREA_MAX_SPAWN_DECLARATION */

    __AREA_BLOCK_RESOURCE_SPAWNS = xsArrayCreateBool(__AREA_COUNT, false, "__AREA_BLOCK_RESOURCE_SPAWNS__51248775");
/* REPLACE:AREA_BLOCK_RESOURCE_SPAWNS_DECLARATION */

    __ARRAY_AREA_LOCATIONS = xsArrayCreateInt(__AREA_COUNT, -1, "__ARRAY_AREA_LOCATIONS__910548260");
    __ARRAY_AREA_CONFIGS   = xsArrayCreateInt(__AREA_COUNT, -1, "__ARRAY_AREA_CONFIGS__522094889");

    for (i = 0; < __AREA_COUNT) {
        count = xsArrayGetInt(__AREA_SPAWN_COUNTS, i);

        int areaArray       = xsArrayCreateVector(count, vector(-1, -1, -1), "areaArray__582659358__v" + i);
        int areaIndexArray  = xsArrayCreateInt(count, -1, "areaIndexArray__052691427__v" + i);
        int areaPlaced      = xsArrayCreateVector(count, vector(-1, -1, -1), "areaPlaced__026358320__v" + i);
        int areaIndexPlaced = xsArrayCreateBool(count, false, "areaIndexPlaced__963630218__v" + i);
        int areaConfig      = xsArrayCreateInt(2, -1, "areaConfig__264812522__v" + i);
        int areaProgress    = xsArrayCreateInt(2, 0, "areaProgress__536248009__v" + i);

        for (ii = 0; < count) {
            xsArraySetInt(areaIndexArray, ii, ii);
        }

        xsArraySetInt(__ARRAY_AREA_LOCATIONS,      i, areaArray);
        xsArraySetInt(__ARRAY_AREA_INDICES,        i, areaIndexArray);
        xsArraySetInt(__ARRAY_AREA_PLACED,         i, areaPlaced);
        xsArraySetInt(__ARRAY_AREA_PLACED_INDICES, i, areaIndexPlaced);
        xsArraySetInt(__ARRAY_AREA_CONFIGS,        i, areaConfig);
        xsArraySetInt(__ARRAY_AREA_PROGRESS,       i, areaProgress);
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

    /* #######################>>> Resources <<<####################### */

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

    for (i = 0; < __RESOURCE_COUNT) {
        count = xsArrayGetInt(__RESOURCE_SPAWN_COUNTS, i);

        int resourceArray       = xsArrayCreateVector(count, vector(-1, -1, -1), "resourceArray__352901574__v" + i);
        int resourceIndexArray  = xsArrayCreateInt(count, -1, "resourceIndexArray__456875221__v" + i);
        int resourcePlaced      = xsArrayCreateVector(count, vector(-1, -1, -1), "resourcePlaced__548476523__v" + i);
        int resourceIndexPlaced = xsArrayCreateBool(count, false, "resourceIndexPlaced__301548796__v" + i);
        int resourceConfig      = xsArrayCreateInt(2, -1, "resourceConfig__985256327__v" + i);
        int resourceProgress    = xsArrayCreateInt(2, 0, "resourceProgress__524875963__v" + i);

        for (ii = 0; < count) {
            xsArraySetInt(resourceIndexArray, ii, ii);
        }

        xsArraySetInt(__ARRAY_RESOURCE_LOCATIONS,      i, resourceArray);
        xsArraySetInt(__ARRAY_RESOURCE_INDICES,        i, resourceIndexArray);
        xsArraySetInt(__ARRAY_RESOURCE_PLACED,         i, resourcePlaced);
        xsArraySetInt(__ARRAY_RESOURCE_PLACED_INDICES, i, resourceIndexPlaced);
        xsArraySetInt(__ARRAY_RESOURCE_CONFIGS,        i, resourceConfig);
        xsArraySetInt(__ARRAY_RESOURCE_PROGRESS,       i, resourceProgress);
    }
    int cArray = -1;
/* REPLACE:AREA_CONFIG_DECLARATION */
/* REPLACE:RESOURCE_CONFIG_DECLARATION */

    int rArray = -1;
/* REPLACE:AREA_LOCATION_INJECTION */
/* REPLACE:RESOURCE_LOCATION_INJECTION */

    bool success = true;
    for (areaId = 0; < __AREA_COUNT) {
        while (success) {
            success = spawnArea__618941981(areaId);
        }

        /* REPLACE:AFTER_AREA_SPAWN_EVENT */
    }

    success = true;
    for (resourceId = 0; < __RESOURCE_COUNT) {
        while (success) {
            success = spawnResource__024510896(resourceId);
        }

        /* REPLACE:AFTER_RESOURCE_SPAWN_EVENT */
    }

    xsDisableSelf();
}
