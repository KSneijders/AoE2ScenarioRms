# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog]
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[keep a changelog]: https://keepachangelog.com/en/1.0.0/

---

## [Unreleased]

### Added

- `GridMapFactory` class for creating `GridMap`s easily
- `ScenarioUtil` class for utility functions regarding scenarios

### Changed

- `AoE2ScenarioRms.mark_blocked_tiles(...)` was moved to `GridMapFactory.default(...)`
- `AoE2ScenarioRms.clear_scenario(...)` was moved to `ScenarioUtil.clear(...)`
- Debug classes now have to be applied manually just before `scenario.write_to_file(...)`

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
