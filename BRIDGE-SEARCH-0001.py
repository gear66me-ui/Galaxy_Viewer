# BRIDGE-SEARCH-0001
from __future__ import annotations

import urllib.request
from pathlib import Path

from google.colab import userdata

BRIDGE_VERSION = "BRIDGE-SEARCH-0001"
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/3ea32960113663c80a9693c747332ab551b5c46c/BRIDGE-SEARCH-0001.py"
UPLOAD_HELPER_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/BRIDGE-SEARCH-0001-UPLOAD.py"
SECRET_NAME = "GITHUB_TOKEN"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    base_source = response.read().decode("utf-8")
exec(compile(base_source, "BRIDGE-SEARCH-0001-base.py", "exec"), globals())

with urllib.request.urlopen(UPLOAD_HELPER_URL, timeout=60) as response:
    upload_source = response.read().decode("utf-8")
exec(compile(upload_source, "BRIDGE-SEARCH-0001-UPLOAD.py", "exec"), globals())

try:
    github_token = userdata.get(SECRET_NAME)
except Exception as exc:
    raise RuntimeError(
        f"Colab Secret {SECRET_NAME!r} is unavailable. Add it in the Colab Secrets panel and grant notebook access."
    ) from exc

if not github_token:
    raise RuntimeError(
        f"Colab Secret {SECRET_NAME!r} is empty. Add a fine-grained GitHub token with Contents read/write access to Galaxy_Viewer."
    )

csv_candidates = sorted(Path("/content").glob(f"{BRIDGE_VERSION}_*_GALAXIES.csv"))
txt_candidates = sorted(Path("/content").glob(f"{BRIDGE_VERSION}_*_GALAXIES_COPY_REPORT.txt"))
if not csv_candidates or not txt_candidates:
    raise RuntimeError("Bridge output files were not created.")

csv_path = csv_candidates[-1]
txt_path = txt_candidates[-1]

print()
print("Uploading bridge audit files to the sandbox branch...")
csv_url = upload_bridge_file(csv_path, github_token)
txt_url = upload_bridge_file(txt_path, github_token)

print()
print("RAW HTTPS LINKS")
print(f"CSV: {csv_url}")
print(f"TEXT: {txt_url}")
print()
print("Send either raw HTTPS address to ChatGPT for cross-checking.")
print(BRIDGE_VERSION)
