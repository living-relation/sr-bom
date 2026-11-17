# Agent rules for sr-bom

- This repo is **public**. Never commit secrets, tokens, personal or machine paths, or vendor CAD
  files (STEP, f3d, SLDPRT, and the like). `tools/check.py` scans for these.
- Work on a branch and open a PR. Never commit to `main`. Delete the branch once it is merged.
- Run `python tools/check.py` before every push. CI runs the same check.
- This is the SR BOM Fusion add-in. Keep the add-in folder (`SRBom/`) self-contained: the shared
  helper lives in `SRBom/sr_fusion_common/` so a junction of `SRBom` into Fusion's AddIns folder works.
- Do not write assembly instructions such as tightening torque or threadlocker notes.
- Live Fusion tests: take the machine's Fusion lock first, and never touch other people's open documents.
  The smoke test closes its own design without saving.
