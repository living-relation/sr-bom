# SR BOM

A Spark Robotic Fusion add-in that counts components, fills part number, description and material
from a `build.json` or by hand, writes those fields back, and exports a BOM to CSV and Excel plus a
report of anything blocked or still empty.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- **Toolbar button** "SR BOM" on several Design-workspace panels, including the **SR Tools** panel on the SOLID tab, plus Add-Ins, Make, and Insert. The panel list is configurable in `%APPDATA%/SRBom/panels.json`.
- Counts every component (pieces per part) in one of three styles: top level, indented, or parts only.
- Fills part number, description, material, vendor, vendor part number and notes from a `build.json`.
- The table can be edited by hand. **Apply + export** writes Fusion-writable fields back onto the components, then saves `<design>_BOM.csv`, `<design>_BOM.xlsx` and `<design>_BOM_report.txt`.
- Vendor, vendor part number and notes are stored as attributes in the group `srbom` (Fusion custom properties need a commercial plan).
- Linked (external) components are read-only; the report lists them. A material name must match a library material exactly, or the report lists it as blocked.

## Requirements

- Autodesk Fusion
- No extra Python packages (the Excel export is written with the standard library)

## Install

1. Clone this repo and keep the folder on disk.
2. In Fusion: **Utilities > Add-ins > Scripts and Add-ins > Add-ins tab > + (green plus)**, and pick the `SRBom` folder inside the clone. Tick **Run on Startup** and click **Run**.

   Or copy or link the `SRBom` folder into `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\` and restart Fusion.
3. The button shows up on the **SR Tools** panel on the SOLID tab, and in the Add-Ins, Make, and Insert panels.

Settings (last folder, checked columns, last build.json) are saved in `%APPDATA%\SRBom\`.

See [docs/install.md](docs/install.md) for the full steps, including uninstall.

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
