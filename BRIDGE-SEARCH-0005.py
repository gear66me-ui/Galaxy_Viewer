# BRIDGE-SEARCH-0005
from __future__ import annotations

import html
import urllib.request

from IPython.display import HTML, display

BRIDGE_VERSION = "BRIDGE-SEARCH-0005"
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/f7844e4d56b62cacce5c9b1be5d5acfff86ae5c5/BRIDGE-SEARCH-0004.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace('BRIDGE_VERSION = "BRIDGE-SEARCH-0004"', 'BRIDGE_VERSION = "BRIDGE-SEARCH-0005"')

old_workbook_call = '''    combined = build_combined(source_rows, backup1, backup2)
    make_workbook({"Main": source_rows, "Backup 1": backup1, "Backup 2": backup2, "Combined": combined})

    token = userdata.get(TOKEN_SECRET)
'''

new_workbook_call = '''    combined = build_combined(source_rows, backup1, backup2)
    make_workbook({
        "Main": source_rows,
        "Backup 1": backup1,
        "Backup 2": backup2,
        "Combined": combined,
        "Viewer Preview": combined,
    })

    display_viewer_preview(combined)

    token = userdata.get(TOKEN_SECRET)
'''

if old_workbook_call not in source:
    raise RuntimeError("BRIDGE-SEARCH-0004 workbook block did not match the expected release source")

source = source.replace(old_workbook_call, new_workbook_call)

preview_code = r'''

def display_viewer_preview(rows):
    preview_fields = [
        "Object",
        "Source catalog",
        "ICRS coordinates",
        "Galaxy age",
        "Redshift (z) / Distance",
        "Morphological type",
        "Angular size",
        "Radial velocity",
        "Physical size",
        "Magnitude",
        "Interest score",
        "Distance method",
        "Data source",
        "Data score",
    ]

    def esc(value):
        return html.escape(str(value or "Not available"))

    header_cells = "".join(f"<th>{esc(field)}</th>" for field in preview_fields)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{esc(row.get(field, 'Not available'))}</td>" for field in preview_fields)
        body_rows.append(f"<tr>{cells}</tr>")

    markup = f"""
    <div id="bridge0005-preview" style="margin:14px 0;padding:12px;background:#000;color:#7FDBFF;border:1px solid #0b4f6c;border-radius:10px;font-family:Arial,Helvetica,sans-serif;">
      <div style="font-weight:800;font-size:18px;margin-bottom:9px;color:#9dff00;">Galaxy Viewer Data Preview — {BRIDGE_VERSION}</div>
      <div style="font-size:12px;margin-bottom:10px;color:#c7d2fe;">Final reconciled values. Scroll horizontally and vertically to inspect all 40 galaxies before opening the workbook.</div>
      <div style="max-height:620px;overflow:auto;border:1px solid #203040;border-radius:8px;">
        <table style="border-collapse:collapse;min-width:2500px;width:100%;font-size:12px;line-height:1.35;">
          <thead style="position:sticky;top:0;z-index:2;background:#0b4f6c;color:#fff;">
            <tr>{header_cells}</tr>
          </thead>
          <tbody>{''.join(body_rows)}</tbody>
        </table>
      </div>
    </div>
    <style>
      #bridge0005-preview th {{padding:8px;border:1px solid #31566b;text-align:left;white-space:nowrap;}}
      #bridge0005-preview td {{padding:7px;border:1px solid #203040;vertical-align:top;min-width:135px;max-width:290px;white-space:normal;word-break:break-word;}}
      #bridge0005-preview tbody tr:nth-child(even) {{background:#071019;}}
      #bridge0005-preview tbody tr:hover {{background:#132432;}}
      #bridge0005-preview td:first-child {{position:sticky;left:0;background:#02070b;color:#ffd84d;font-weight:700;z-index:1;}}
    </style>
    """
    display(HTML(markup))
'''

insert_marker = '\ndef main():\n'
if insert_marker not in source:
    raise RuntimeError("BRIDGE-SEARCH-0004 main definition marker was not found")
source = source.replace(insert_marker, preview_code + insert_marker, 1)

exec(compile(source, "BRIDGE-SEARCH-0005-runtime.py", "exec"), globals())
