# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog]
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[keep a changelog]: https://keepachangelog.com/en/1.0.0/

[//]: # (---)

[//]: # ()
[//]: # (## [Unreleased])

[//]: # ()
[//]: # (- ...)

---

## 0.3.8 - 2025-March-19

### Added

- Automatically disabling all resource spawn triggers once spawning has finished

### Fixed

- Resources not spawning if ran without any delay (before XS arrays init was finished)

---

## 0.3.7 - 2025-March-17

> All releases from `0.3.0` to `0.3.6` published correctly but the pipeline failed afterward

### Added

- Resource spawning control features
  - New attributes to the `AoE2ScenarioRms` object:
    - `automatic_resource_spawning` (If resources should spawn without manual activation; Default: `True`) 
    - `staggered_resource_spawning` (If resources should spawn staggered (not all at once); Default: `False`)
    - `staggered_resource_offset` (Seconds before staggered spawning starts; Default: `0`)
    - `staggered_resource_delay` (Seconds between staggered spawns; Default: `1`)
    - `staggered_resource_batch_size` (Amount of resources to spawn each staggered cycle; Default: `1`)
  - The `AoE2ScenarioRms.create_objects(...)` function now returns a dictionary
    - Keys are the names of the configs given to the function
    - Values are the triggers used to activate the resource spawning. 
      - If staggered spawning is enabled, the timer conditions will be added at scenario writing. 
        So these cannot be adjusted manually. If you want manual timing, disable the automatic staggered 
        spawning and add timers (or other) to the returned triggers yourself.  

### Fixed

- The randomization logic used in XS no longer has a `void main` function.

---

## 0.2.21 - 2024-May-25

### Fixed

- `UnitInfo.BEAR.ID` missing from the list when clearing with `ObjectClear.WOLFS`

---

## 0.2.20 - 2024-May-25

### Fixed

- The `xs` `ShuffleVectorArray` function

---

## 0.2.19 - 2024-Januari-04

### Fixed

- Missing `xs` files from the python package

> All releases from `0.2.8` to `0.2.19` were release tests

---

## 0.2.7 - 2024-Januari-01

### Fixed

- Package dependencies (`requirements.txt`, `pyproject.toml`)

---

## 0.2.6 - 2024-Januari-01

### Added

- Added support for an `Area` object in the `GridMapFactory`

---

## 0.2.5 - 2023-April-16

> `0.2.2`, `0.2.3`, `0.2.4` & `0.2.5` were just release tests

---

## 0.2.1 - 2023-April-16

### Fixed

- Typo in name `TerrainMark.WATER_SHORE_BEACH`

---

## 0.2.0 - 2023-April-16

### Added

- Docstrings to all functions
- `TileUtil.within_range(...)` function to get all tiles that are within a range of a given tile
- Support for objects bigger than 1x1! (Use the `object_size` config option)

### Changed

- `XsUtil.read(...)` renamed to `XsUtil.file(...)`
- `XsUtil.format_name(...)` renamed to `XsUtil.constant(...)`
- `GridMap.reset_all(...)` renamed to `GridMap.set_all(...)`
- `Locator.find_...(...)` functions all return `List[Tile], bool` instead of `Tile|None`
- `Locator.find_...(...)` functions no longer use random guessing anymore, all tiles are shuffled and looped through for consistent 100% coverage

### Fixed

- Issue with `Locator.find_random_tile_within_range(...)` using `random.randrange` (exclusive)
- Issue with multiple `create_objects` appending their counts instead of counting the total

---

## 0.1.0 - 2023-February-25 (Not on PyPI)

### Added

- `GridMapFactory` class for creating `GridMap`s easily
- `ScenarioUtil` class for utility functions regarding scenarios
- `as_layer` parameter for `ApplyBlockedAsBlack(...)` to use the layer feature instead of the terrain itself  
- `DEEP_FISH`, `SHORE_FISH` and `FISH_OBJECTS` (combination of the two) entries to `ObjectClear`
- `SHORE` entry to `TerrainMark` for selecting the line of water right next to the beach
- `TileUtil` class

### Changed

- `AoE2ScenarioRms.mark_blocked_tiles(...)` was moved to `GridMapFactory.block(...)`
- `AoE2ScenarioRms.clear_scenario(...)` was moved to `ScenarioUtil.clear(...)`
- `ApplyDebug` classes now have to be applied manually just before `scenario.write_to_file(...)`
- `Locator` now uses a shuffled list of available tiles instead of guessing tiles
- `const` parameter from `CreateObjectConfig(...)` can now be list to randomize const per group
- Renamed `ImproperCreateObjectError` to `InvalidCreateObjectError`
- Using `TerrainMark.WATER` will no longer include the first line of water around land. Add `TerrainMark.SHORE` for those tiles

### Removed

- `XsEntry` class due to being redundant when moving the `join_string` to a global state (which it should be) 
- `Debug` class due to being redundant as the `ApplyDebug` classes can be used themselves. 
- `AoE2ScenarioRms.write(...)` function due to now being done automatically when calling `scenario.write_to_file(...)`
- `debug` parameter from `AoE2ScenarioRms(...)`

---

## 0.0.2 - 2023-February-23 (Not on PyPI)

### Added

- `Debug` class (IntFlag)
- `ApplyDebug` classes for the logic of applying the debug features (`units`/`terrain`/`triggers`/`xs`)
  - `ApplyXsPrint`
  - `ApplyBlockedAsBlack`
  - `ApplyNoClutter`
  - `ApplyAllVisible`

### Changed

- `debug` parameter from `AoE2ScenarioRms(...)` now takes the `Debug` class instead of a boolean

---

## 0.0.1 - 2023-February-22 (Not on PyPI)

- Official start of this package. (No longer just a script)

---

[//]: # ( Added:      for new features. )
[//]: # ( Changed:    for changes in existing functionality. )
[//]: # ( Deprecated: for soon-to-be removed features. )
[//]: # ( Removed:    for now removed features. )
[//]: # ( Fixed:      for any bug fixes. )
[//]: # ( Security:   in case of vulnerabilities. )
