# SR BOM

A Spark Robotic Fusion add-in that counts components, fills part number, description and material
from a `build.json` or by hand, writes those fields back, and exports a BOM to CSV and Excel plus a
report of anything blocked or still empty.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## How this add-in is installed

**SR BOM is junctioned straight to the repo clone**, so a `git pull` updates what Fusion loads. Fusion's AddIns entry must be named exactly `SRBom` and must point at the `SRBom` folder inside this repo, not the repo root.

Fusion does not pick up new code until the add-in restarts: restart Fusion, or press **Shift+S**, open **Add-Ins**, and **Stop** then **Run**.

An automatic updater (coming soon, in the workstation repo) will pull updates hourly and notify you to restart Fusion.

To create the junction, open a normal Command Prompt (not Run as administrator). `mklink /J` does not need elevation. Both paths below are absolute, so no `cd` is required. Run:

```
mklink /J "%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\SRBom" "<path-to-this-clone>\SRBom"
```

Replace `<path-to-this-clone>` with this repo's clone path on that PC. The active-folder path differs per PC.

## Features

- **Toolbar button** "SR BOM" on several Design-workspace panels, including the **SR Tools** panel on the SOLID tab, plus Add-Ins, Make, and Insert. The panel list is configurable in `%APPDATA%/SRBom/panels.json`.
- Counts every component (pieces per part) in one of three styles: top level, indented, or parts only.
- Fills part number, description and material from a `build.json`.
- The table can be edited by hand. **Apply + export** writes Fusion-writable fields back onto the components, then saves `<design>_BOM.csv`, `<design>_BOM.xlsx` and `<design>_BOM_report.txt`.
- BOM columns: Item, QTY, Part Number, Part Description and Material. Component name, vendor, vendor part number and notes are not offered.
- Linked (external) components are read-only; the report lists them. A material name must match a library material exactly, or the report lists it as blocked.

## Requirements

- Autodesk Fusion
- No extra Python packages (the Excel export is written with the standard library)

## Install

1. Clone this repo and keep the folder on disk.
2. Create the AddIns junction as described in [How this add-in is installed](#how-this-add-in-is-installed). Do not copy the folder into AddIns; a copy will not follow `git pull`.
3. In Fusion, press **Shift+S**, open the **Add-Ins** tab, select **SR BOM**, tick **Run on Startup**, and click **Run**. After a later `git pull`, restart the add-in the same way (**Stop**, then **Run**) or restart Fusion.
4. The button shows up on the default panels listed in [Where the buttons go](#where-the-buttons-go).

Settings (last folder, checked columns, last build.json) are saved in `%APPDATA%\SRBom\`.

See [docs/install.md](docs/install.md) for the full steps, including uninstall.

## Where the buttons go

The **SR BOM** button can show on several Design-workspace toolbar panels at once. By default it is added to:

- **Utilities > Add-ins** (`SolidScriptsAddinsPanel`)
- **Make** (`SolidMakePanel`)
- **Insert** (`InsertPanel`)
- **SR Tools** (`SRToolsPanel`)

By default the button is pinned on SR Tools and on Add-ins. Insert and Make still get the command; Fusion keeps your own pin or unpin choice after the first run.

The list lives in `%APPDATA%\SRBom\panels.json`. Create or edit that file, then Stop and Run the add-in (or restart Fusion) so the change takes effect. Example:

```json
{
  "panel_ids": [
    "SolidScriptsAddinsPanel",
    "SolidMakePanel",
    "InsertPanel",
    "SRToolsPanel"
  ]
}
```

Unknown panel ids are skipped. If the file is missing or `panel_ids` is empty or unusable, the defaults above are used. Stopping the add-in removes every toolbar button for this command, including leftovers from an older list.

If `SRToolsPanel` already exists (for example because another SR add-in created it on the SOLID tab), this add-in reuses it. If it does not exist, this add-in creates an **SR Tools** tab in the Design workspace and puts the panel on that tab. If the panel (and its tab) are empty after stop, they are removed too.

## Usage

Open a design, click **SR BOM**, edit or fill the table, then **Apply + export**. See [docs/usage.md](docs/usage.md) for styles, columns, and the `build.json` format.

## Documentation

- [Overview](docs/overview.md)
- [Install](docs/install.md)
- [Usage](docs/usage.md)
- [Development](docs/development.md)
- [Documentation index](docs/README.md)

## Development

```
python tools/check.py
```

CI runs the same check. `dev/fusion_smoke.py` is a live test that runs inside Fusion. See [docs/development.md](docs/development.md).

## Contributing

Work on a branch and open a pull request against `main`. Update `docs/` when behavior changes. See [docs/development.md](docs/development.md) and [AGENTS.md](AGENTS.md).

## License

This project is licensed under the [MIT License](LICENSE). Copyright (c) 2026 Spark Robotic.
