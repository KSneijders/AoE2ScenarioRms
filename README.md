# AoE2ScenarioRandomizedSpawning

Project to add replay-ability to scenarios by adding triggers and XS to the scenario to cause random resource placements 

## Todo

1. Change tile selection to `random.choice(all_possible_tiles)` instead of looking for completely random tiles
   Potentially conditionally? Or with parameter? As big surfaces are faster with completely random tiles
2. Move XS logic to own class(es)
3. Move Debug logic to own class
4. More (?)

## Ideas

1. Player areas :monkaS:
2. Scale with map size (hardcoded on parser level as map_size cannot be changed dynamically)
3. More (?)
4. Support larger objects (currently only 1x1 is supported)
5. Automatically figure out what to remove based on CreateObject configs 
