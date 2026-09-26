#!/usr/bin/env python3
"""Build the Android AR (Scene Viewer) models: ar/halo1-<colorway>.glb.

Scene Viewer needs a real .glb URL, so each colorway gets its own file. The
colors come from the swatch inputs in index.html (one source of truth). Only
the glTF JSON is rewritten: material colors, plus a root node that scales the
shoe to AR_LENGTH_M and puts it on the floor at the origin. The Draco-compressed
geometry and textures are copied through byte for byte.

Run from the repo root after changing a colorway:  python3 tools/build_ar_models.py
"""
import base64, json, re, struct
from pathlib import Path

AR_LENGTH_M = 0.27  # heel-to-toe length in AR, US M9 (keep in sync with index.html)
SLOTS = {"upper": ["M_UpperMesh"], "foam": ["M_Foam"], "base": ["M_FoamBase"],
         "trim": ["M_Graphite", "M_Eyestay"], "accent": ["M_Lace", "M_Eyelet"]}

root = Path(__file__).resolve().parent.parent


def srgb_to_linear(hex_color):
    out = []
    for i in (1, 3, 5):
        c = int(hex_color[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return out


def read_glb():
    b = base64.b64decode((root / "shoe.glb.b64.txt").read_bytes().strip())
    json_len = struct.unpack("<I", b[12:16])[0]
    return json.loads(b[20:20 + json_len]), b[20 + json_len:]  # rest = BIN chunk incl. header


def write_glb(path, gltf, bin_chunk):
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    body = struct.pack("<II", len(js), 0x4E4F534A) + js + bin_chunk
    path.write_bytes(struct.pack("<III", 0x46546C67, 2, 12 + len(body)) + body)


def quat_rotate(q, v):
    x, y, z, w = q
    tx, ty, tz = 2 * (y * v[2] - z * v[1]), 2 * (z * v[0] - x * v[2]), 2 * (x * v[1] - y * v[0])
    return [v[0] + w * tx + (y * tz - z * ty), v[1] + w * ty + (z * tx - x * tz), v[2] + w * tz + (x * ty - y * tx)]


def bounds(gltf):
    """World-space bounds from accessor min/max (the glTF nodes here use TRS only)."""
    lo, hi = [1e9] * 3, [-1e9] * 3

    def walk(i, chain):
        n = gltf["nodes"][i]
        chain = chain + [n]
        if "mesh" in n:
            for prim in gltf["meshes"][n["mesh"]]["primitives"]:
                a = gltf["accessors"][prim["attributes"]["POSITION"]]
                for x in (a["min"][0], a["max"][0]):
                    for y in (a["min"][1], a["max"][1]):
                        for z in (a["min"][2], a["max"][2]):
                            v = [x, y, z]
                            for m in reversed(chain):
                                v = [c * s for c, s in zip(v, m.get("scale", [1, 1, 1]))]
                                v = quat_rotate(m.get("rotation", [0, 0, 0, 1]), v)
                                v = [c + t for c, t in zip(v, m.get("translation", [0, 0, 0]))]
                            for k in range(3):
                                lo[k], hi[k] = min(lo[k], v[k]), max(hi[k], v[k])
        for c in n.get("children", []):
            walk(c, chain)

    for r in gltf["scenes"][gltf.get("scene", 0)]["nodes"]:
        walk(r, [])
    return lo, hi


def main():
    html = (root / "index.html").read_text()
    colorways = [dict(re.findall(r'data-(\w+)="([^"]+)"', tag), id=re.search(r'id="cw-(\w+)"', tag)[1])
                 for tag in re.findall(r'<input type="radio" name="colorway"[^>]*>', html)]
    # "Design your own" (cw-custom) carries no colors; Android AR falls back to the closest preset for it
    colorways = [cw for cw in colorways if "upper" in cw]
    assert colorways, "no colorway inputs found in index.html"

    base, bin_chunk = read_glb()
    lo, hi = bounds(base)
    s = AR_LENGTH_M / max(hi[0] - lo[0], hi[2] - lo[2])
    # centre on x/z, sole on the floor (y = 0)
    offset = [-s * (lo[0] + hi[0]) / 2, -s * lo[1], -s * (lo[2] + hi[2]) / 2]

    out_dir = root / "ar"
    out_dir.mkdir(exist_ok=True)
    for cw in colorways:
        g = json.loads(json.dumps(base))
        mats = {m["name"]: m for m in g["materials"]}
        for slot, names in SLOTS.items():
            for name in names:
                pbr = mats[name]["pbrMetallicRoughness"]
                alpha = pbr.get("baseColorFactor", [1, 1, 1, 1])[3]
                pbr["baseColorFactor"] = srgb_to_linear(cw[slot]) + [alpha]
        g["nodes"].append({"name": "AR_Root", "scale": [s, s, s], "translation": offset,
                           "children": g["scenes"][0]["nodes"]})
        g["scenes"][0]["nodes"] = [len(g["nodes"]) - 1]
        # the texture transform only nudges the tongue print; let viewers without it still open the file
        g["extensionsRequired"] = [e for e in g["extensionsRequired"] if e != "KHR_texture_transform"]
        path = out_dir / f"halo1-{cw['id']}.glb"
        write_glb(path, g, bin_chunk)
        print(f"{path.relative_to(root)}  {path.stat().st_size / 1e6:.2f} MB")
    print(f"scale {s:.4f}: {max(hi[0] - lo[0], hi[2] - lo[2]) * 100:.1f} cm model -> {AR_LENGTH_M * 100:.0f} cm")


if __name__ == "__main__":
    main()
