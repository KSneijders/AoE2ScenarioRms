progressArray = xsArrayGetInt(__ARRAY_RESOURCE_PROGRESS, resourceId);
name = xsArrayGetString(__RESOURCE_GROUP_NAMES, resourceId);
placedResourcesCount = xsArrayGetInt(progressArray, 0);

__debug__("Group `" + name + "` spawned " + placedResourcesCount + " successfully!");
