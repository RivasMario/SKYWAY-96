"""6 degree tilt feet with a dovetail slide-rail that locks into the case bottom.

Each foot is a wedge built in the CASE frame: its flat top (z=0) carries a male
dovetail rail that slides along Y into the channel cut in the case bottom
(see FEET_DOVETAIL in skyway_case.py). The wedge body hangs below z=0, sloped 6
deg, so the desk contact tilts the board USB-edge-up. Slide a foot into each
channel from the end; friction holds, add a dab of glue if you want it permanent.
"""
import cadquery as cq, os, math
from skyway_case import build_case, FOOT, foot_x_off, FEET_DOVETAIL

assert FEET_DOVETAIL, "set FEET_DOVETAIL=True in skyway_case.py"
_, p = build_case()
od = p["out_d"]
xo = foot_x_off(p)

tilt = math.radians(FOOT["tilt_deg"])
front_h = FOOT["front_h"]
rise = od * math.tan(tilt)                 # extra height at the USB (-Y) edge
ch_h, o, d, clr = FOOT["ch_h"], FOOT["ch_open"], FOOT["ch_deep"], FOOT["clr"]
length = od - 2*FOOT["inset"]              # rail length along Y

def foot():
    # wedge body (built at x=0): flat top at z=0, sloped bottom (thicker at -Y/USB)
    prof = [(-od/2, 0), (od/2, 0), (od/2, -front_h), (-od/2, -(front_h + rise))]
    body = (cq.Workplane("YZ").polyline(prof).close().extrude(FOOT["w"])
            .translate((-FOOT["w"]/2, 0, 0)))
    # male dovetail rail on top (channel minus clearance), runs along Y, centered
    oo, dd = o - 2*clr, d - 2*clr
    rpts = [(-oo/2, 0.0), (oo/2, 0.0), (dd/2, ch_h), (-dd/2, ch_h)]
    rail = (cq.Workplane("XZ").workplane(offset=length/2)
            .polyline(rpts).close().extrude(-length))
    return body.union(rail)

os.makedirs("output", exist_ok=True)
# one symmetric design — print this STL x2 (one per bottom channel)
f = foot()
cq.exporters.export(f, "output/skyway96_foot.stl", tolerance=0.01, angularTolerance=0.1)
for old in ("output/skyway96_foot_left.stl", "output/skyway96_foot_right.stl"):
    if os.path.exists(old):
        os.remove(old)

import trimesh
m = trimesh.load("output/skyway96_foot.stl")
print(f"foot (print x2) watertight={m.is_watertight} bbox={[round(float(x),1) for x in m.extents]}")
print(f"tilt {FOOT['tilt_deg']} deg | rail {o}/{d}mm dovetail x {length:.0f}mm | front {front_h} back {front_h+rise:.1f}")
