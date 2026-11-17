"""Tests for the pure (no adsk) parts of the SR BOM add-in."""
import csv
import io
import json
import os
import struct
import sys
import zipfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADDIN = os.path.join(ROOT, 'SRBom')
sys.path.insert(0, ADDIN)

import bom_core  # noqa: E402
from sr_fusion_common import settings  # noqa: E402
from sr_fusion_common.names import safe_name  # noqa: E402


def test_safe_name_strips_version_and_bad_chars():
    assert safe_name('Filament Cabinet v12') == 'Filament Cabinet'
    assert safe_name('a/b:c*?') == 'a_b_c__'
    assert safe_name('  ') == 'export'


def test_settings_roundtrip_ignores_unknown_and_bad(tmp_path):
    settings.save('bom', {'folder': '/tmp/x', 'junk': 1}, str(tmp_path))
    got = settings.load('bom', bom_core.DEFAULTS, str(tmp_path))
    assert got['folder'] == '/tmp/x' and 'junk' not in got
    (tmp_path / 'bad.json').write_text('{oops')
    assert settings.load('bad', {'a': 1}, str(tmp_path)) == {'a': 1}


def test_settings_dir_uses_srbom():
    assert settings.APP_FOLDER == 'SRBom'


def test_count_parts():
    assert bom_core.count_parts(['a', 'b', 'a']) == {'a': 2, 'b': 1}


@pytest.mark.parametrize('data', [
    {'parts': [{'Name': 'Leg', 'PN': 'P-1', 'Material': 'Aluminum 6061', 'McMaster': '91290A'}]},
    [{'component': 'Leg', 'part_number': 'P-1', 'material': 'Aluminum 6061', 'vendor_pn': '91290A'}],
    {'Leg': {'pn': 'P-1', 'mat': 'Aluminum 6061', 'mcmaster_pn': '91290A'}},
])
def test_parse_build_json_shapes(data):
    t = bom_core.parse_build_json(data)
    assert t['leg']['part_number'] == 'P-1'
    assert t['p-1']['material'] == 'Aluminum 6061'
    assert t['leg']['vendor_pn'] == '91290A'


def test_fill_from_build_respects_overwrite():
    rows = [{'name': 'Leg', 'qty': 4, 'part_number': 'KEEP', 'description': ''},
            {'name': 'Other', 'qty': 1}]
    t = bom_core.parse_build_json({'Leg': {'pn': 'NEW', 'description': 'leg'}})
    got = bom_core.fill_from_build(rows, t)
    assert rows[0]['part_number'] == 'KEEP' and rows[0]['description'] == 'leg'
    assert got == [('Leg', 'description')]
    bom_core.fill_from_build(rows, t, overwrite=True)
    assert rows[0]['part_number'] == 'NEW'


def test_fill_replaces_fusion_defaults():
    rows = [{'name': 'Leg', 'part_number': 'Leg', 'material': 'Steel', '_soft': ['part_number', 'material']}]
    t = bom_core.parse_build_json({'Leg': {'pn': 'P-1', 'material': 'Aluminum 6061'}})
    assert sorted(f for _, f in bom_core.fill_from_build(rows, t)) == ['material', 'part_number']
    assert rows[0]['part_number'] == 'P-1' and rows[0]['_soft'] == []


def test_empty_and_report():
    rows = [{'name': 'Leg', 'qty': 2, 'part_number': 'P', 'description': '', 'material': 'Steel'}]
    assert bom_core.empty_cells(rows) == [('Leg', 'description')]
    rep = bom_core.report(rows, [('Leg', 'material', 'no material')], [])
    assert 'SR BOM report' in rep
    assert '2 pieces' in rep and 'Leg: material - no material' in rep and 'Leg: description' in rep


def test_csv_and_xlsx(tmp_path):
    rows = [{'name': 'A & <B>', 'qty': 3, 'part_number': 'P1'}]
    out = list(csv.reader(io.StringIO(bom_core.to_csv(rows, ['name', 'qty', 'part_number']))))
    assert out[0] == ['QTY', 'Part Number', 'Component'] and out[1] == ['3', 'P1', 'A & <B>']
    p = bom_core.write_xlsx(str(tmp_path / 'b.xlsx'), rows, columns=['qty', 'name'])
    with zipfile.ZipFile(p) as z:
        sheet = z.read('xl/worksheets/sheet1.xml').decode()
        assert 'A &amp; &lt;B&gt;' in sheet and '<v>3</v>' in sheet
        assert '[Content_Types].xml' in z.namelist()


def test_col_letters():
    assert [bom_core._col(i) for i in (0, 25, 26, 27)] == ['A', 'Z', 'AA', 'AB']


def test_manifest_valid():
    with open(os.path.join(ADDIN, 'SRBom.manifest'), encoding='utf-8') as f:
        m = json.load(f)
    assert m['type'] == 'addin' and m['autodeskProduct'] == 'Fusion'
    assert m['author'] == 'Spark Robotic'
    assert 'SR BOM' in m['description']['']


def _png_size(path):
    with open(path, 'rb') as f:
        assert f.read(8) == b'\x89PNG\r\n\x1a\n'
        length, typ = struct.unpack('>I4s', f.read(8))
        assert typ == b'IHDR'
        w, h = struct.unpack('>II', f.read(8))
        return w, h


def test_icons_present():
    d = os.path.join(ADDIN, 'resources', 'icon')
    for name, n in (('16x16', 16), ('32x32', 32)):
        assert _png_size(os.path.join(d, name + '.png')) == (n, n)
    src = open(os.path.join(ADDIN, 'SRBom.py'), encoding='utf-8').read()
    assert "'resources', 'icon'" in src
    assert 'SR BOM' in src and 'HB BOM' not in src
    assert "CMD_ID = 'srBomCmd'" in src


def _n(i, kids=(), pn=''):
    return {'id': i, 'name': i, 'part_number': pn or i.upper(), 'description': 'd' + i, 'children': list(kids)}


TREE = [_n('suba', [_n('screw'), _n('screw'), _n('screw'), _n('screw'), _n('plate')]),
        _n('base'),
        _n('suba', [_n('screw'), _n('screw'), _n('screw'), _n('screw'), _n('plate')]),
        _n('screw'), _n('screw'), _n('screw')]


def test_column_order_and_no_uom():
    assert bom_core.KEYS[:4] == ['item', 'qty', 'part_number', 'description']
    assert not any('unit' in k or 'uom' in k for k in bom_core.KEYS)
    assert 'item' not in bom_core.EDITABLE and 'qty' not in bom_core.EDITABLE
    assert bom_core.pick_columns(['notes', 'qty', 'item', 'bogus']) == ['item', 'qty', 'notes']
    assert bom_core.pick_columns([]) == bom_core.DEFAULT_COLUMNS


def test_top_level_style():
    rows = bom_core.build_rows(TREE, 'top')
    assert [(r['item'], r['id'], r['qty']) for r in rows] == [('1', 'suba', 2), ('2', 'base', 1), ('3', 'screw', 3)]
    assert all(r['top'] for r in rows) and rows[0]['has_children']


def test_indented_style():
    rows = bom_core.build_rows(TREE, 'indented')
    assert [(r['item'], r['id'], r['qty'], r['level']) for r in rows] == [
        ('1', 'suba', 2, 0), ('1.1', 'screw', 4, 1), ('1.2', 'plate', 1, 1),
        ('2', 'base', 1, 0), ('3', 'screw', 3, 0)]
    assert [r['id'] for r in bom_core.thumb_rows(rows)] == ['suba', 'base', 'screw']


def test_parts_only_style_totals():
    rows = bom_core.build_rows(TREE, 'parts')
    assert [(r['item'], r['id'], r['qty']) for r in rows] == [('1', 'screw', 11), ('2', 'plate', 2), ('3', 'base', 1)]


def test_edits_merge_across_duplicate_rows():
    rows = bom_core.build_rows(TREE, 'indented')
    rows[4]['part_number'] = '91290A115'
    merged = bom_core.merge_edits(rows)
    assert len(merged) == 4
    assert next(m for m in merged if m['id'] == 'screw')['part_number'] == '91290A115'
    new = bom_core.spread_edits(bom_core.build_rows(TREE, 'top'), merged)
    assert new[2]['part_number'] == '91290A115' and new[0]['part_number'] == 'SUBA'


def test_export_follows_style_and_columns(tmp_path):
    rows = bom_core.build_rows(TREE, 'indented')
    out = list(csv.reader(io.StringIO(bom_core.to_csv(rows, ['description', 'item', 'qty', 'part_number']))))
    assert out[0] == ['Item', 'QTY', 'Part Number', 'Part Description']
    assert out[2] == ['1.1', '4', 'SCREW', 'dscrew']
    p = bom_core.write_xlsx(str(tmp_path / 'i.xlsx'), rows, columns=['item', 'qty'])
    with zipfile.ZipFile(p) as z:
        sheet = z.read('xl/worksheets/sheet1.xml').decode()
    assert '>1.1<' in sheet and 'thumb' not in sheet


def test_pin_not_forced_each_start():
    texts = []
    for dirpath, _, files in os.walk(ADDIN):
        for name in files:
            if name.endswith('.py'):
                texts.append(open(os.path.join(dirpath, name), encoding='utf-8').read())
    blob = chr(10).join(texts)
    assert 'isPromotedByDefault' in blob
    assert 'isPromoted =' not in blob.replace('isPromotedByDefault', '')

def test_attr_group_renamed():
    src = open(os.path.join(ADDIN, 'bom_ops.py'), encoding='utf-8').read()
    assert "ATTR_GROUP = 'srbom'" in src
    assert 'handbuiltcad' not in src
