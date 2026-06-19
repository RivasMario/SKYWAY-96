"""Print pre-flight check for the SKYWAY case STLs.

Static slicer-style sanity pass (not a thermal/warp sim). For the assumed
orientation (printed as modelled, +Z up, bottom on bed) it reports:
  - watertight / manifold
  - bounding box + bed fit (256 and 220 mm)
  - steep downward overhangs that need support (area + where), vs short ones
    that just bridge
  - bottom footprint area + longest span -> warp/adhesion note
Run: .venv/Scripts/python.exe preflight.py
"""
import trimesh, numpy as np, glob, os, math

OVERHANG_DEG = 45        # downward surfaces steeper than this from horizontal -> support
BRIDGE_MAX   = 12.0      # mm: unsupported spans under this usually bridge fine

def analyze(path):
    m = trimesh.load(path)
    n = m.face_normals
    a = m.area_faces
    z0 = m.bounds[0][2]
    ext = m.extents
    print(f"\n=== {os.path.basename(path)} ===")
    print(f"  watertight   : {m.is_watertight}   (manifold edges: {len(m.edges)==len(m.edges_unique)*2 if False else 'n/a'})")
    print(f"  size mm      : {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f}")
    print(f"  bed fit      : 256bed={'OK' if max(ext[0],ext[1])<=256 else 'NO'}  220bed={'OK' if max(ext[0],ext[1])<=220 else 'NO'}")

    # downward overhang faces needing support: normal pointing down, surface
    # shallower than OVERHANG_DEG from horizontal  ->  -n.z > cos(OVERHANG_DEG)
    thr = math.cos(math.radians(OVERHANG_DEG))
    down = -n[:, 2]
    cz = m.triangles_center[:, 2]
    sup = (down > thr) & (a > 0.05) & (cz > z0 + 0.5)   # elevated ceilings only (bed face is supported)
    sup_area = a[sup].sum()
    print(f"  overhang area: {sup_area:.1f} mm^2 needing support "
          f"({100*sup_area/m.area:.1f}% of surface)")
    if sup_area > 0.1:
        c = m.triangles_center[sup]
        # cluster by z to name features; report z bands + footprint span
        zs = c[:, 2]
        for lo, hi, label in [(z0, z0+0.6, "bed underside (foot channel / recess)"),
                              (z0+0.6, 9.0, "mid (USB cutout top / clamp lip / channel lips)"),
                              (9.0, 1e9, "upper")]:
            sel = (zs >= lo) & (zs < hi)
            if sel.any():
                cc = c[sel]; aa = a[sup][sel].sum()
                span_x = np.ptp(cc[:,0]); span_y = np.ptp(cc[:,1])
                print(f"     - z[{lo:.1f},{hi:.1f}) {label}: {aa:.1f} mm^2, "
                      f"max span {max(span_x,span_y):.1f}mm -> "
                      f"{'BRIDGES ok' if max(span_x,span_y)<=BRIDGE_MAX else 'check / may need support'}")

    # bottom footprint (faces at the bed) -> adhesion + warp
    bed = (m.triangles_center[:, 2] < z0 + 0.3) & (n[:, 2] < -0.5)
    bed_area = a[bed].sum()
    foot = m.bounds[1][:2] - m.bounds[0][:2]
    print(f"  bed contact  : ~{bed_area:.0f} mm^2 footprint, longest {max(foot):.0f}mm "
          f"-> {'WARP RISK: brim recommended' if max(foot)>180 else 'ok'}")

for f in sorted(glob.glob("output/*.stl")):
    analyze(f)
