"""Split the 3D plate into Left + Right for normal-size beds.

The plate is 361 mm long -> needs a seam to fit a ~220 mm bed. A 96% layout has
NO full-height clear vertical gap (stagger), so a straight cut would slice switch
holes in half. Instead the seam runs vertically at SEAM_X but JOGS around the few
cutouts it would cross, keeping every switch hole whole in one half.

Those jog tongues also key the two halves together in X and Y, so they self-align
at assembly. Glue the seam; the PCB + screws below lock the final sandwich.

Halves: Left ~192 mm, Right ~170 mm  (both < 220).
"""
import cadquery as cq, os
from plate import build_plate, _bbox

SEAM_X = 192.0
M      = 2.0            # wall margin kept around each jogged cutout (seam-edge wall)
ZLO, ZHI = -1.0, None   # tall prism in Z (set after build)

plate, info = build_plate()
ox0, oy0, ox1, oy1 = info["bbox"]
PT = info["PLATE_T"]
ZHI = PT + 1.0
H = ZHI - ZLO

def slab(x0, x1, y0, y1):
    return (cq.Workplane("XY").workplane(offset=ZLO)
            .moveTo((x0 + x1) / 2.0, (y0 + y1) / 2.0)
            .rect(x1 - x0, y1 - y0).extrude(H))

# crossing cutouts -> assign each wholly to the side of its centre
cross = []
for c in info["cutouts"]:
    x0, y0, x1, y1 = _bbox(c)
    if x0 < SEAM_X < x1:
        cross.append((x0, y0, x1, y1, (x0 + x1) / 2.0))

# left region = everything left of SEAM, jogged around crossing cutouts
left_region = slab(ox0 - 5, SEAM_X, oy0 - 5, oy1 + 5)
for x0, y0, x1, y1, cx in cross:
    if cx < SEAM_X:                      # keep on LEFT -> bump boundary right past it
        left_region = left_region.union(slab(SEAM_X, x1 + M, y0 - M, y1 + M))
    else:                                # keep on RIGHT -> notch boundary left of it
        left_region = left_region.cut(slab(x0 - M, SEAM_X, y0 - M, y1 + M))

left  = plate.intersect(left_region)
right = plate.cut(left_region)

os.makedirs("output", exist_ok=True)
cq.exporters.export(left,  "output/skyway96_plate_left.stl",  tolerance=0.01, angularTolerance=0.1)
cq.exporters.export(right, "output/skyway96_plate_right.stl", tolerance=0.01, angularTolerance=0.1)

import trimesh
for n in ("left", "right"):
    m = trimesh.load(f"output/skyway96_plate_{n}.stl")
    print(f"{n:5s} watertight={m.is_watertight} bbox={[round(float(v),1) for v in m.extents]}")
nl = sum(1 for *_, cx in cross if cx < SEAM_X)
print(f"seam X={SEAM_X} | {len(cross)} jogged cutouts ({nl} left / {len(cross)-nl} right)")
