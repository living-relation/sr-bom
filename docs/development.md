# Development

**SR BOM** is a Fusion add-in written in Python.

## Clone

```
git clone https://github.com/living-relation/sr-bom.git
```

Load the `SRBom` folder into Fusion as described in [Install](install.md).

## Layout

- `SRBom/` — the Fusion add-in (junction this folder into AddIns). Entry point: `SRBom.py` and `SRBom.manifest`.
- `SRBom/sr_fusion_common/` — settings and file-name helpers, vendored so the add-in stands alone.
- `SRBom/bom_core.py` — pure BOM logic (no Fusion import); unit-tested.
- `SRBom/bom_ops.py` — Fusion-side read/write of component fields.
- `tests/` — unit tests that do not need Fusion.
- `dev/fusion_smoke.py` — live test that runs inside Fusion.
- `tools/check.py` — secret/path scan plus pytest. CI runs the same command.

## Coding notes

- This repository is public. Do not commit secrets, tokens, passwords, personal email addresses, machine-specific paths, or vendor CAD files.
- Keep Spark Robotic / SR- naming in user-visible text and repository docs.
- Work on a branch and open a pull request against `main`. Never commit to `main` directly.
- Run `python tools/check.py` before every push. See [AGENTS.md](../AGENTS.md).

## Tests

```
python tools/check.py
```

`dev/fusion_smoke.py` is a live test. Take the machine's Fusion lock first. It opens a new scratch design, fills and exports a BOM, registers and removes the button, then closes the design without saving. Output goes to `%TEMP%\srbom_fusion_smoke`. Your open documents are not touched.

## Contributing

1. Create a branch from `main`.
2. Add or update documentation in `docs/` when behavior changes.
3. Run `python tools/check.py`.
4. Open a pull request against `main`. CI must stay green.
