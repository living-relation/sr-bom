# Overview

SR BOM is a Spark Robotic add-in for Autodesk Fusion. It counts components in the active design,
fills bill-of-materials fields from a `build.json` or by hand, writes those fields back, and
exports CSV and Excel plus a report of anything blocked or still empty.

It is part of the Spark Robotic (SR-) tool set for Fusion.

## Features

- A toolbar button named **SR BOM** in the Design workspace, Solid tab, SR Tools, Add-Ins, Make, and Insert panels.
- Three BOM styles: top level, indented (layered), or parts only.
- Editable fields: part number, description, material, vendor, vendor part number, and notes.
- Part number, description and material are written to the Fusion components.
- Vendor, vendor part number and notes are stored as attributes in the group `srbom`, because Fusion custom properties need a commercial plan.
- Optional thumbnails of top-level items in the dialog.
- Optional fill from a `build.json`. Filling never replaces what you already typed unless **build.json overwrites filled cells** is ticked. Fusion's own defaults (part number = component name, the design's default material) count as empty.

Linked (external) components are read-only; the report lists them. A material name must match a name in your material libraries exactly, or the report lists it as blocked.

## Requirements

- Autodesk Fusion
- No extra Python packages

## Settings

The last output folder, selected columns, BOM style, thumbnail preference, and last `build.json` path are saved in `%APPDATA%\SRBom\`.

## Further reading

- [Install](install.md)
- [Usage](usage.md)
- [Development](development.md)
