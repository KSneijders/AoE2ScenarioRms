# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog]
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[keep a changelog]: https://keepachangelog.com/en/1.0.0/

---

## [Unreleased]

### Removed

- `XsEntry` class

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

- `AoE2ScenarioRms` `debug` parameter now takes the `Debug` class instead of a boolean

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
