"""SKYWAY 96 — 3D-printable stepped switch plate.

Source geometry = the validated laser plate ../Plate/skyway96_plate.dxf
(KB_PLATE_VALIDATOR output, already in PCB frame: 0..361.95 x 0..113.3 mm,
99 switch cutouts incl. combo+stab, 11 screw holes, 4 edge notches).

FDM plates can't be a flat 1.5 mm sheet (warps, flexes, fragile). So this is a
STEPPED plate:
  - top  CLIP_T (1.5 mm): the EXACT DXF cutout profile (14 mm body + 1 mm clip
    wings) -> MX switch top-clips snap exactly like a real 1.5 mm plate.
  - bottom (PLATE_T-CLIP_T): each cutout opened to a >=16 mm square so the
    switch's wider lower housing clears. Extra material = stiffness + low warp.

The step shelf (~0.8 mm wide ring) faces down at z=CLIP_T; it's a tiny annular
overhang that bridges fine, so print bottom-on-bed as modelled (no supports).

build_plate() returns (solid, INFO) for plate_split.py to reuse.
"""
import cadquery as cq, ezdxf, os

DXF = os.path.join("..", "Plate", "skyway96_plate.dxf")

PLATE_T = 3.0          # total thickness
CLIP_T  = 1.5          # top layer that keeps the exact clip profile
BODY_MIN = 15.8        # min square opening for the switch lower housing (15.6 +clr)
BODY_GROW = 0.4        # extra around combo/stab cutouts on the body layer
EPS = 0.1

# Adaptive screw holes: each hole grown as large as its neighbourhood allows
# while keeping >= SCREW_WALL to the nearest cutout / other hole / plate edge.
# Roomy holes open up for screwdriver/head clearance; crowded ones (boxed in by
# switch cutouts) stay small so the wall stays printable.
SCREW_WALL  = 1.0      # min wall (mm) hole-edge -> nearest obstacle
SCREW_CAP_D = 5.0      # functional max Ø (driver / M2 washer bearing)
SCREW_MIN_D = 2.4      # min Ø (M2 shaft + clearance)

def _read_dxf(path):
    d = ezdxf.readfile(path)
    msp = d.modelspace()
    outline = None
    cutouts, screws = [], []
    for e in msp:
        L = e.dxf.layer
        if L == "PLATE_OUTLINE":
            outline = [(round(p[0], 4), round(p[1], 4)) for p in e.get_points()]
        elif L == "SWITCH_CUTOUTS":
            cutouts.append([(round(p[0], 4), round(p[1], 4)) for p in e.get_points()])
        elif L == "PCB_SCREW_HOLES":
            c = e.dxf.center
            screws.append((round(c[0], 4), round(c[1], 4), round(e.dxf.radius, 4)))
    if outline is None:
        raise RuntimeError("no PLATE_OUTLINE layer in " + path)
    return outline, cutouts, screws

def _bbox(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)

def _body_rects(cutouts):
    """The body-relief openings (largest material removed) as (x0,y0,x1,y1)."""
    rects = []
    for c in cutouts:
        x0, y0, x1, y1 = _bbox(c)
        cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        w = max((x1 - x0) + BODY_GROW, BODY_MIN)
        h = max((y1 - y0) + BODY_GROW, BODY_MIN)
        rects.append((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))
    return rects

def screw_radii(outline, cutouts, screws):
    """Per-hole max radius: grow to SCREW_WALL of the nearest obstacle, clamped
    to [SCREW_MIN_D, SCREW_CAP_D]. Returns list of (x, y, r)."""
    ox0, oy0, ox1, oy1 = _bbox(outline)
    rects = _body_rects(cutouts)
    def d_pt_rect(px, py, r):
        x0, y0, x1, y1 = r
        dx = max(x0 - px, 0.0, px - x1); dy = max(y0 - py, 0.0, py - y1)
        return (dx * dx + dy * dy) ** 0.5
    out = []
    for i, (sx, sy, _r) in enumerate(screws):
        dc = min(d_pt_rect(sx, sy, rr) for rr in rects)
        dh = min((((sx - ax) ** 2 + (sy - ay) ** 2) ** 0.5 - ar)
                 for j, (ax, ay, ar) in enumerate(screws) if j != i) if len(screws) > 1 else 1e9
        de = min(sx - ox0, ox1 - sx, sy - oy0, oy1 - sy)
        near = min(dc, dh, de)
        r = max(SCREW_MIN_D / 2, min(near - SCREW_WALL, SCREW_CAP_D / 2))
        out.append((sx, sy, round(r, 3)))
    return out

def build_plate(dxf_path=None):
    outline, cutouts, screws = _read_dxf(dxf_path or DXF)

    # solid plate body (outline incl. edge notches), extruded full thickness
    plate = (cq.Workplane("XY").polyline(outline).close().extrude(PLATE_T))

    z_clip = PLATE_T - CLIP_T            # 1.5 : top layer base

    # --- top layer: exact DXF clip profile, ALL cutouts (z_clip .. top) ---
    # switches AND stab cutouts are stepped: the top 1.5 mm shelf adds strength
    # everywhere and keeps the clip lip on the 1u switches.
    top = cq.Workplane("XY").workplane(offset=z_clip)
    for c in cutouts:
        top = top.polyline(c).close()
    top = top.extrude(CLIP_T + EPS)
    plate = plate.cut(top)

    # --- bottom layer: >=16mm square body-clearance per cutout (z=-eps .. z_clip) ---
    body = cq.Workplane("XY").workplane(offset=-EPS)
    for c in cutouts:
        x0, y0, x1, y1 = _bbox(c)
        cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        w = max((x1 - x0) + BODY_GROW, BODY_MIN)
        h = max((y1 - y0) + BODY_GROW, BODY_MIN)
        body = body.moveTo(cx, cy).rect(w, h)
    body = body.extrude((z_clip + EPS))
    plate = plate.cut(body)

    # --- screw holes (full depth, adaptive per-hole radii) ---
    screws_r = screw_radii(outline, cutouts, screws)
    holes = cq.Workplane("XY").workplane(offset=-EPS)
    for (sx, sy, r) in screws_r:
        holes = holes.moveTo(sx, sy).circle(r)
    holes = holes.extrude(PLATE_T + 2 * EPS)
    plate = plate.cut(holes)

    info = dict(outline=outline, cutouts=cutouts, screws=screws_r,
                bbox=_bbox(outline), PLATE_T=PLATE_T, CLIP_T=CLIP_T)
    return plate, info


if __name__ == "__main__":
    plate, info = build_plate()
    os.makedirs("output", exist_ok=True)
    out = "output/skyway96_plate.stl"
    cq.exporters.export(plate, out, tolerance=0.01, angularTolerance=0.1)
    x0, y0, x1, y1 = info["bbox"]
    import trimesh
    m = trimesh.load(out)
    print(f"plate watertight={m.is_watertight} bbox={[round(float(v),1) for v in m.extents]}")
    print(f"frame {x1-x0:.2f} x {y1-y0:.2f} mm | {len(info['cutouts'])} cutouts | "
          f"{len(info['screws'])} screws | {PLATE_T}mm (clip {CLIP_T}mm)")
    ds = sorted(round(2 * r, 2) for *_, r in info["screws"])
    print(f"screw Ø (adaptive, {SCREW_WALL}mm wall): {ds}")
