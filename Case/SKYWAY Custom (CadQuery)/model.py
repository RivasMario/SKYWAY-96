"""SKYWAY 96 custom tray — full one-piece body.
Needs a 350 mm+ bed. For normal beds run split.py; for tilt run feet.py.
"""
import cadquery as cq, os
from skyway_case import build_case

case, p = build_case()
os.makedirs("output", exist_ok=True)
cq.exporters.export(case, "output/skyway96_case.stl", tolerance=0.01, angularTolerance=0.1)
print(f"full body {p['out_w']:.1f} x {p['out_d']:.1f} x {p['out_h']:.1f} mm | {p['screw_mode']} posts")
