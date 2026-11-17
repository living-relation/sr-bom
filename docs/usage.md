# Usage

## Before you start

1. Install the add-in as described in [Install](install.md).
2. Open the Fusion design you want to work with.

## Run

Click **SR BOM** on the **SR Tools** panel (on the SOLID tab), or in the Design workspace Add-Ins, Make, or Insert panel. The dialog lists the current assembly.

- **BOM style:** Top level (root's direct children, quantity per assembly), Indented (every level, item numbers such as 1, 1.1, 1.1.1), or Parts only (leaf parts, total quantity across the assembly).
- **Columns:** Choose which columns appear. Item and QTY are counted automatically and are not editable.
- **build.json:** Optionally fill empty cells from a JSON file. Tick **build.json overwrites filled cells** only if the file should replace values you already typed.
- **Thumbnails:** Optional pictures of top-level items, shown in the dialog only. They are not written into the CSV or Excel files.
- **Apply + export** writes Fusion-writable fields back onto the components, then saves the export files in the folder you pick.

## Export files

In the output folder, named after the design (Fusion's ` v12` suffix dropped):

- `<design>_BOM.csv`
- `<design>_BOM.xlsx`
- `<design>_BOM_report.txt` — filled cells, anything blocked, and anything still empty

If no design is open, the add-in asks you to open one first.

## build.json

Any of these shapes work. Parts match by component name or part number (not case-sensitive):

```json
{"parts": [{"name": "Hinge leaf", "part_number": "Hinge-01", "description": "Door hinge leaf",
            "material": "Aluminum 6061", "vendor": "McMaster", "vendor_pn": "1234A56", "notes": ""}]}
```

also `{"bom": [...]}`, a plain list, or `{"Hinge leaf": {"pn": "Hinge-01", ...}}`. Accepted aliases: `pn`, `desc`, `mat`, `supplier`, `mcmaster`, `note`.

## Limits and known issues

- Linked (external) components cannot be edited here; the report tells you to edit them in their own design.
- A material must match a library name exactly, or it is reported as blocked.
- Custom BOM properties are not available on non-commercial Fusion plans, so vendor fields are stored as attributes in the group `srbom`.
