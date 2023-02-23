# AoE2ScenarioRms

A library built on top of the [AoE2ScenarioParser]. 
Allows you to add `triggers` and `XS` to your AoE2:DE scenarios which will add logic to allow for random resource 
placements each play-through.

> Keep in mind this project is still heavily a **WORK-IN-PROGRESS**

[AoE2ScenarioParser]: https://github.com/KSneijders/AoE2ScenarioParser

## Example

Please check out the example [here](https://github.com/KSneijders/AoE2ScenarioRms/tree/main/examples). (no real docs atm)

This project is still a work-in-progress. 
So everything can still change without notice (most likely will).  
If you'd like to try anyway, for now just clone this repository to the root of your source folder and import from there.

Make sure `AoE2ScenarioParser` is installed: [link](https://github.com/KSneijders/AoE2ScenarioParser).

## Rough todo:

1. Change tile selection to `random.choice(all_possible_tiles)` instead of looking for completely random tiles
   Potentially conditionally? Or with parameter? As big surfaces are faster with completely random tiles
2. ~~Move XS logic to own class(es)~~
3. ~~Move Debug logic to own class~~
4. Change `asr.write()` as triggers are always added directly, so why isn't the script?
5. Add docs, docstrings and tests
6. ~~Allow XS to log the amount that spawned succesfully so you can limit the amount of spawns for performance~~
7. More (?)

## Potential Ideas:

1. Player areas :monkaS:
2. Scale with map size (hardcoded on parser level as map_size cannot be changed dynamically)
3. Support larger objects (currently only 1x1 is supported)
4. Automatically figure out what to remove based on CreateObjectConfig configs 
5. Add ability to mock the XS spawning process to know 
6. More (?)

---

**Suggestions are always welcome!** 

# Authors

- Kerwin Sneijders (Main Author)

# License

> Will be added soon

Most likely (but not 100% sure): GNU General Public License v3.0
