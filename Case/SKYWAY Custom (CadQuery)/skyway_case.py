"""SKYWAY 96 custom tray — shared case builder.

build_case() returns (solid, P) where P holds the derived dimensions other
scripts (split.py, feet.py) need. Fit data from the repo gerbers / kicad_pcb:
  PCB 361.95 x 114.30 x 1.6 mm ; USB-C on the -Y wall ; screw notches on +Y.
"""
import cadquery as cq

P = dict(
    pcb_w=361.95, pcb_d=114.30, pcb_t=1.60, clear=0.40,
    wall=3.00, floor=2.50, standoff_h=4.00, above_pcb=7.00,
    ledge_w=2.20, lip_w=0.80, lip_h=1.20, corner_fillet=4.0,
    screw_mode="insert",                 # "insert" | "selftap"
    usb_w=13.0, usb_h=6.0, usb_x_left=19.03, usb_z_pcb=1.2,
    post_dia_insert=6.5, bore_insert=3.20, bore_depth_insert=4.0,
    post_dia_tap=5.0,    bore_tap=1.65,   bore_depth_tap=4.5,
)

# PCB-local mount points (x from left, y from USB edge)
MOUNT_HOLES = [
    (23.82, 104.77), (38.10, 19.05), (128.57, 68.82), (133.35, 19.05),
    (185.74, 57.15), (188.86, 104.77), (228.60, 19.05), (245.24, 104.77),
    (285.75, 19.05), (342.90, 19.05), (342.90, 76.20),
]
NOTCH_HOLES = [  # edge arc-notches: 3 on +Y (spacebar) edge + 1 on left edge
    (2.62, 76.05), (23.48, 111.68), (154.49, 111.68), (285.74, 111.68),
]

# X-flip of the post holes only (mirror left<->right about the PCB center).
# USB-C cutout stays put -> notches stay on the far long edge, opposite the USB.
FLIP_X = True

# Put the USB-C hole on the diagonally-opposite corner: right end + far (+Y) wall.
USB_FAR_CORNER = True

# Dovetail slide-rail feet: cut a matching channel into the case bottom (so the
# foot rail slides in along Y). Shared geometry so feet.py builds the exact mate.
FEET_DOVETAIL = True
FOOT = dict(inset=6.0, w=26.0,            # rail/channel X-width + setback from ends
            ch_h=1.6, ch_open=8.0, ch_deep=11.0, clr=0.30,   # dovetail channel
            tilt_deg=6.0, front_h=3.0)    # wedge

def foot_x_off(p):
    return p["out_w"]/2 - FOOT["inset"] - FOOT["w"]/2

def foot_channel(p, xc, grow=0.0):
    """Female dovetail channel solid (to cut from the case bottom), runs along Y."""
    import cadquery as cq
    o, d = FOOT["ch_open"] + 2*grow, FOOT["ch_deep"] + 2*grow
    h = FOOT["ch_h"]
    pts = [(xc - o/2, -0.01), (xc + o/2, -0.01), (xc + d/2, h), (xc - d/2, h)]
    return (cq.Workplane("XZ").workplane(offset=p["out_d"]/2)
            .polyline(pts).close().extrude(-p["out_d"]))

def mount_points(P):
    pts = MOUNT_HOLES + NOTCH_HOLES
    if FLIP_X:
        pts = [(P["pcb_w"] - lx, ly) for lx, ly in pts]
    return pts

def usb_x(P):
    return (P["pcb_w"] - P["usb_x_left"]) if USB_FAR_CORNER else P["usb_x_left"]


# ---- exterior flair (off — kept as optional toggles) --------------------
BEZEL = False         # 45-deg chamfer around the top rim
bezel = 3.0
STRIPE = False        # recessed accent groove around the side walls
stripe_h, stripe_depth, stripe_drop = 3.5, 1.2, 6.0   # band height, depth, drop from top


def derived(P):
    d = dict(P)
    d["cav_w"] = P["pcb_w"] + 2*P["clear"]
    d["cav_d"] = P["pcb_d"] + 2*P["clear"]
    d["out_w"] = d["cav_w"] + 2*P["wall"]
    d["out_d"] = d["cav_d"] + 2*P["wall"]
    d["z_pcb"] = P["floor"] + P["standoff_h"]
    d["cav_h"] = P["standoff_h"] + P["pcb_t"] + P["above_pcb"]
    d["out_h"] = P["floor"] + d["cav_h"]
    if P["screw_mode"] == "insert":
        d["post_dia"], d["bore_dia"], d["bore_depth"] = (
            P["post_dia_insert"], P["bore_insert"], P["bore_depth_insert"])
    else:
        d["post_dia"], d["bore_dia"], d["bore_depth"] = (
            P["post_dia_tap"], P["bore_tap"], P["bore_depth_tap"])
    return d


def build_case(params=None):
    p = derived(params or P)
    out_w, out_d, out_h = p["out_w"], p["out_d"], p["out_h"]
    cav_w, cav_d = p["cav_w"], p["cav_d"]
    wall, floor, z_pcb = p["wall"], p["floor"], p["z_pcb"]
    pcb_w, pcb_d, pcb_t = p["pcb_w"], p["pcb_d"], p["pcb_t"]

    case = (cq.Workplane("XY")
            .box(out_w, out_d, out_h, centered=(True, True, False))
            .edges("|Z").fillet(p["corner_fillet"]))

    if BEZEL:
        # chamfer the top rim while the top face is still solid (outer edge only)
        try:    case = case.faces(">Z").edges().chamfer(bezel)
        except Exception as e: print("bezel skipped:", e)

    low = (cq.Workplane("XY").workplane(offset=floor)
           .box(cav_w - 2*p["ledge_w"], cav_d - 2*p["ledge_w"], p["standoff_h"] + 0.01,
                centered=(True, True, False)))
    cav = (cq.Workplane("XY").workplane(offset=z_pcb)
           .box(cav_w, cav_d, (out_h - z_pcb) + 1, centered=(True, True, False)))
    case = case.cut(low).cut(cav)

    # clamp lip
    lip_z = z_pcb + pcb_t
    lip = ((cq.Workplane("XY").workplane(offset=lip_z)
            .box(cav_w, cav_d, p["lip_h"], centered=(True, True, False)))
           .cut(cq.Workplane("XY").workplane(offset=lip_z - 0.01)
                .box(cav_w - 2*p["lip_w"], cav_d - 2*p["lip_w"], p["lip_h"] + 0.02,
                     centered=(True, True, False))))
    case = case.union(lip)

    # standoff posts at real mount holes + edge notches (mirrored if MIRROR_X)
    pts = [(lx - pcb_w/2, ly - pcb_d/2) for lx, ly in mount_points(p)]
    posts = (cq.Workplane("XY").workplane(offset=floor)
             .pushPoints(pts).circle(p["post_dia"]/2).extrude(p["standoff_h"]))
    bores = (cq.Workplane("XY").workplane(offset=z_pcb + 0.01)
             .pushPoints(pts).circle(p["bore_dia"]/2).extrude(-(p["bore_depth"] + 0.01)))
    case = case.union(posts).cut(bores)

    # USB-C cutout: -Y wall by default, or +Y wall for the far corner
    usb_cx = usb_x(p) - pcb_w/2
    usb_cz = z_pcb + pcb_t + p["usb_z_pcb"]
    if USB_FAR_CORNER:
        usb = (cq.Workplane("XZ").workplane(offset=out_d/2 + 1)
               .center(usb_cx, usb_cz).rect(p["usb_w"], p["usb_h"]).extrude(-(wall + 2)))
    else:
        usb = (cq.Workplane("XZ").workplane(offset=-out_d/2 - 1)
               .center(usb_cx, usb_cz).rect(p["usb_w"], p["usb_h"]).extrude(wall + 2))
    case = case.cut(usb)

    if FEET_DOVETAIL:
        # dovetail channels in the bottom for the slide-rail feet
        xo = foot_x_off(p)
        case = case.cut(foot_channel(p, +xo)).cut(foot_channel(p, -xo))
    else:
        # rubber-foot recesses
        fx, fy = out_w/2 - 14.0, out_d/2 - 14.0
        feet = (cq.Workplane("XY").pushPoints([(fx, fy), (-fx, fy), (fx, -fy), (-fx, -fy)])
                .circle(5.0).extrude(1.5))
        case = case.cut(feet)

    if STRIPE:
        # recessed accent groove around the 4 side walls (paint / 2nd-colour line)
        sz = out_h - stripe_drop - stripe_h/2          # band centre Z
        ring = (cq.Workplane("XY").workplane(offset=sz - stripe_h/2)
                .box(out_w + 2, out_d + 2, stripe_h, centered=(True, True, False))
                .cut(cq.Workplane("XY").workplane(offset=sz - stripe_h/2 - 1)
                     .box(out_w - 2*stripe_depth, out_d - 2*stripe_depth, stripe_h + 2,
                          centered=(True, True, False))))
        case = case.cut(ring)

    # cosmetic edges
    if not BEZEL:
        try:    case = case.edges(">Z").edges("|X or |Y").fillet(0.8)
        except Exception: pass
    try:    case = case.faces("<Z").edges().chamfer(0.6)
    except Exception: pass
    return case, p
