#!/usr/bin/env python3
"""Run a CadQuery model script, validate the STL, render a 6-view PNG.

Usage: python tools/run_model.py model.py [--preview]

Replaces the skill's pyrender-based runner with a matplotlib renderer
(pyrender needs a GL context that is unreliable on headless Windows).
Reports watertightness + bounding box; writes <stl>.preview.png on --preview.
"""
import sys, subprocess, glob, os, json, time

def main():
    if len(sys.argv) < 2:
        print("usage: run_model.py model.py [--preview]"); sys.exit(2)
    script = sys.argv[1]
    preview = "--preview" in sys.argv[2:]
    here = os.path.dirname(os.path.abspath(__file__))
    py = sys.executable
    t0 = time.time()
    r = subprocess.run([py, script], capture_output=True, text=True, timeout=300)
    out = {"success": r.returncode == 0, "returncode": r.returncode,
           "stdout": r.stdout, "stderr": r.stderr, "stls": []}
    if r.returncode != 0:
        print(json.dumps(out, indent=2)); sys.exit(1)

    import trimesh
    stls = sorted(glob.glob(os.path.join(os.path.dirname(script) or ".", "output", "*.stl")),
                  key=lambda p: os.path.getmtime(p))
    stls = [p for p in stls if os.path.getmtime(p) >= t0 - 1]
    for s in stls:
        m = trimesh.load(s)
        info = {"file": s, "watertight": bool(m.is_watertight),
                "bbox_mm": [round(float(d), 2) for d in m.extents],
                "volume_cm3": round(float(m.volume) / 1000.0, 2) if m.is_watertight else None}
        if preview:
            info["preview"] = render(m, s)
        out["stls"].append(info)
    print(json.dumps(out, indent=2))

def render(m, stl_path):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    v = m.vertices; f = m.faces
    tris = v[f]
    views = [("iso", 25, -60), ("top", 89, -90), ("front", 0, -90),
             ("right", 0, 0), ("back", 0, 90), ("bottom", -89, -90)]
    fig = plt.figure(figsize=(15, 9))
    for i, (name, el, az) in enumerate(views, 1):
        ax = fig.add_subplot(2, 3, i, projection="3d")
        pc = Poly3DCollection(tris, alpha=1.0, facecolor="#9bb7d4",
                              edgecolor="none", linewidths=0)
        ax.add_collection3d(pc)
        mins = v.min(axis=0); maxs = v.max(axis=0)
        ext = (maxs - mins); ctr = (mins + maxs) / 2
        pad = ext * 0.05
        ax.set_xlim(mins[0]-pad[0], maxs[0]+pad[0])
        ax.set_ylim(mins[1]-pad[1], maxs[1]+pad[1])
        ax.set_zlim(mins[2]-pad[2], maxs[2]+pad[2])
        try: ax.set_box_aspect(tuple(ext + 1e-6))   # true proportions
        except Exception: pass
        ax.view_init(elev=el, azim=az)
        ax.set_title(name, fontsize=11)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    fig.suptitle(os.path.basename(stl_path), fontsize=13)
    png = stl_path.rsplit(".", 1)[0] + ".preview.png"
    fig.tight_layout()
    fig.savefig(png, dpi=90)
    plt.close(fig)
    return png

if __name__ == "__main__":
    main()
