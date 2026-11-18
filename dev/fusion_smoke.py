"""In-Fusion smoke test for SR BOM. Run from Fusion (Scripts and Add-Ins, or a Python bridge).
Works only in a NEW scratch document that it closes WITHOUT saving; your open documents are not
touched. Output goes to %TEMP%/srbom_fusion_smoke.
"""
import importlib
import json
import os
import sys
import tempfile

import adsk.core
import adsk.fusion

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if '__file__' in globals() else os.environ['SRBOM_ROOT']


def main():
    addin = os.path.join(ROOT, 'SRBom')
    for p in (ROOT, addin):
        if p not in sys.path:
            sys.path.insert(0, p)
    for m in [m for m in sys.modules if m.split('.')[0] in ('SRBom', 'sr_fusion_common', 'bom_core', 'bom_ops')]:
        del sys.modules[m]
    bops = importlib.import_module('SRBom.bom_ops')
    bcore = importlib.import_module('SRBom.bom_core')
    bmain = importlib.import_module('SRBom.SRBom')
    app = adsk.core.Application.get()
    out_dir = os.path.join(tempfile.gettempdir(), 'srbom_fusion_smoke')
    os.makedirs(out_dir, exist_ok=True)
    res = {}
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    try:
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        for i, (w, h) in enumerate(((2, 1), (1, 1))):
            sk = root.sketches.add(root.xYConstructionPlane)
            sk.sketchCurves.sketchLines.addTwoPointRectangle(adsk.core.Point3D.create(i * 5, 0, 0),
                                                              adsk.core.Point3D.create(i * 5 + w, h, 0))
            root.features.extrudeFeatures.addSimple(sk.profiles.item(0), adsk.core.ValueInput.createByReal(1),
                                                    adsk.fusion.FeatureOperations.NewComponentFeatureOperation)
        root.occurrences.item(0).component.name = 'Plate'
        root.occurrences.item(1).component.name = 'Block'
        root.occurrences.addExistingComponent(root.occurrences.item(1).component, adsk.core.Matrix3D.create())
        rows = bops.collect_rows(des)
        res['counts'] = {r['name']: r['qty'] for r in rows}
        table = bcore.parse_build_json({'parts': [{'name': 'Plate', 'pn': 'SM-001', 'description': 'plate',
                                                   'material': 'Aluminum 6061'},
                                                  {'name': 'Block', 'pn': 'SM-002', 'material': 'NoSuchMat'}]})
        res['filled'] = bcore.fill_from_build(rows, table)
        blocked = bops.apply_rows(des, rows)
        res['blocked'] = blocked
        back = {r['name']: r for r in bops.collect_rows(des)}
        res['written_plate'] = {k: back['Plate'][k] for k in ('part_number', 'description', 'material')}
        res['written_block_pn'] = back['Block']['part_number']
        files = bmain.run_exports(out_dir, 'smoke v2', list(back.values()), blocked, res['filled'])
        res['bom_files'] = [os.path.basename(f) for f in files]
        ui = app.userInterface
        # Skipped while the installed add-in is running: stop() would delete its shared command and button.
        if ui.commandDefinitions.itemById(bmain.CMD_ID) is not None:
            res['button_check'] = 'skipped: the installed SR BOM is running'
        else:
            bmain.run(None)
            res['button_registered'] = bool(ui.commandDefinitions.itemById(bmain.CMD_ID))
            bmain.stop(None)
            res['button_removed'] = not ui.commandDefinitions.itemById(bmain.CMD_ID)
    finally:
        doc.close(False)
    res['files'] = sorted(os.listdir(out_dir))
    print(json.dumps(res, indent=1, default=str))
    return res


def run(context):
    try:
        res = main()
        adsk.core.Application.get().userInterface.messageBox(json.dumps(res, indent=1, default=str)[:3000])
    except Exception:
        import traceback
        adsk.core.Application.get().userInterface.messageBox(traceback.format_exc())


if __name__ == '__main__' and 'SRBOM_ROOT' in os.environ:
    main()
