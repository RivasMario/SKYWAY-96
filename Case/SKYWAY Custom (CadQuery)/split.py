"""Split the SKYWAY tray into Left + Right halves for normal-size beds.

Joint = a row of DROP-IN dovetails on a seam rib. Each tenon flares in Y, so once
seated it locks the halves against pulling apart in X. Tenons are extruded
vertically (constant cross-section in Z) -> they print support-free, and you
assemble by lowering the right half straight down onto the left.

The seam rib (raised floor strip) also acts as an anti-sag gusset across the
joint. Rib height is kept under the hotswap sockets so it never touches the PCB.
Seam is offset to a key-column gap, clear of every standoff post.

NOTE: dovetails only (no screws yet) per request - add cross-bolts later if the
walls need clamping.
"""
import cadquery as cq, os
from skyway_case import build_case, FLIP_X

case, p = build_case()
ow, od, oh = p["out_w"], p["out_d"], p["out_h"]
floor, cav_d, z_pcb = p["floor"], p["cav_d"], p["z_pcb"]

seam   = (+9.525 if FLIP_X else -9.525)   # column-gap, clear of posts
rib_h  = 4.0          # < socket clearance (PCB underside 6.5, sockets ~4.7)
rib_w  = 18.0         # seam rib width in X
dt     = 6.0          # dovetail depth into the right half
w_root = 7.0          # tenon width in Y at the seam face
w_tip  = 11.0         # tenon width in Y at the tip (flare -> X lock)
clr    = 0.30         # socket clearance
tenon_ys = [-45.0, -15.0, 15.0, 45.0]
BIG = 3000.0

# seam rib (raised floor) spanning the cavity depth
rib = (cq.Workplane("XY").box(rib_w, cav_d, rib_h, centered=(True, True, False))
       .translate((seam + dt/2, 0, 0)))
case = case.union(rib)

def half(cx):
    return cq.Workplane("XY").box(BIG, BIG, BIG).translate((cx, 0, 0))
left  = case.intersect(half(seam - BIG/2))
right = case.intersect(half(seam + BIG/2))

def tenon(yi, grow):
    t, w = w_root + 2*grow, w_tip + 2*grow
    pts = [(seam - 0.01, yi - t/2), (seam - 0.01, yi + t/2),
           (seam + dt,   yi + w/2), (seam + dt,   yi - w/2)]
    return cq.Workplane("XY").polyline(pts).close().extrude(rib_h)

for yi in tenon_ys:
    left  = left.union(tenon(yi, 0.0))      # tenon belongs to the left half
    right = right.cut(tenon(yi, clr))       # matching socket in the right half

os.makedirs("output", exist_ok=True)
cq.exporters.export(left,  "output/skyway96_left.stl",  tolerance=0.01, angularTolerance=0.1)
cq.exporters.export(right, "output/skyway96_right.stl", tolerance=0.01, angularTolerance=0.1)

import trimesh
for n in ("left", "right"):
    m = trimesh.load(f"output/skyway96_{n}.stl")
    print(f"{n:5s} watertight={m.is_watertight} bbox={[round(float(x),1) for x in m.extents]}")
print(f"seam X={seam} | {len(tenon_ys)} drop-in dovetails | rib {rib_w}x{rib_h}mm")
