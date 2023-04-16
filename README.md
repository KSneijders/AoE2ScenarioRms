# AoE2ScenarioRms

Add replay-ability to scenarios through random resource placement using triggers & XS!
A library built on top of the [AoE2ScenarioParser].

> Keep in mind this project is a **work-in-progress**

[AoE2ScenarioParser]: https://github.com/KSneijders/AoE2ScenarioParser

## Installation

You can install the project using **pip**:

```bash
pip install AoE2ScenarioRms
```

## Updating AoE2ScenarioRms

If you have the library already installed, you can use the following command to update it:

```bash
pip install --no-cache-dir --upgrade AoE2ScenarioRms
```

To read about the changes between versions, checkout the [changelog.md](./CHANGELOG.md) file.

## Examples

Please check out the example [here](https://github.com/KSneijders/AoE2ScenarioRms/tree/main/examples). 
(no _real_ docs atm)

## Ideas for future releases:

- Player areas :monkaS:
- Scale with map size (hardcoded on parser level as map_size cannot be changed dynamically)
- **v0.2.0** ~~Support larger objects (currently only 1x1 is supported)~~
- Automatically figure out what to remove based on CreateObjectConfig configs
- Add ability to mock the XS spawning process to estimate the amount of necessary successful spawn attempts
- Ability to bind ID to list of create objects and be able to differentiate distance to each group 
- (Somehow) remove spawn order bias. Currently, the earlier the spawns the more chance they have to succeed because 
- the map isn't filled up yet.
- ...

---

**Suggestions are always welcome!**

# Authors

- Kerwin Sneijders (Main Author)

# License

MIT License: Please see the [LICENSE file].

[license file]: https://github.com/KSneijders/AoE2ScenarioRms/blob/main/LICENSE
