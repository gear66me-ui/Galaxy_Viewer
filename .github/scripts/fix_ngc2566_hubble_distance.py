#!/usr/bin/env python3
import json
from pathlib import Path

PATH = Path("viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0035-ESA-FOV.json")
Z = 0.005448
C_KM_S = 299792.458
H0 = 70.0
MPC_TO_MLY = 3.26156
DISTANCE_MLY = (Z * C_KM_S / H0) * MPC_TO_MLY

def size_kly(distance_mly, arcmin):
    return round(distance_mly * 1000.0 * arcmin / 3437.74677, 3)

data = json.loads(PATH.read_text(encoding="utf-8"))
matches = [e for e in data.get("entries", []) if e.get("archiveId") == "potw2451a" or e.get("name") == "NGC 2566"]
if len(matches) != 1:
    raise SystemExit(f"Expected exactly one Hubble NGC 2566 entry; found {len(matches)}")
entry = matches[0]
entry["distance"] = round(DISTANCE_MLY, 6)
entry["redshift"] = Z
science = entry.setdefault("science", {})
science["distanceMly"] = round(DISTANCE_MLY, 6)
science["distanceMethod"] = "redshift_Hubble_flow_H0_70_from_SIMBAD_z_0.005448"
science["distanceDisplay"] = f"{DISTANCE_MLY:.2f} million light-years"
science["distanceEstimated"] = True
science["distanceEvidence"] = "Derived from SIMBAD NGC 2566 emission redshift z=0.005448 using v≈cz and H0=70 km/s/Mpc; peculiar velocity may materially affect distance."
science["redshift"] = Z
science["redshiftDisplay"] = "z = 0.005448 (SIMBAD emission redshift)"
science["redshiftEstimated"] = False
science["redshiftMethod"] = "SIMBAD_emission_redshift"
science["sizeKly"] = [size_kly(DISTANCE_MLY, entry["imageFovXArcmin"]), size_kly(DISTANCE_MLY, entry["imageFovYArcmin"])]
science["sizeMethod"] = "estimated_from_fov_and_redshift_Hubble_flow_distance"
science["sizeDisplay"] = f"EST. {round(science['sizeKly'][0])} × {round(science['sizeKly'][1])} KLY"
PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"archiveId": entry.get("archiveId"), "distanceMly": science["distanceMly"], "redshift": science["redshift"], "sizeKly": science["sizeKly"]}))
