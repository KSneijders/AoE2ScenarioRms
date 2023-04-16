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

## 0.1.0 - 2023-February-25 (Not released)

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

## 0.0.2 - 2023-February-23 (Not released)

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

## 0.0.1 - 2023-February-22 (Not released)

- Official start of this package. (No longer just a script)

---

[//]: # ( Added:      for new features. )
[//]: # ( Changed:    for changes in existing functionality. )
[//]: # ( Deprecated: for soon-to-be removed features. )
[//]: # ( Removed:    for now removed features. )
[//]: # ( Fixed:      for any bug fixes. )
[//]: # ( Security:   in case of vulnerabilities. )
