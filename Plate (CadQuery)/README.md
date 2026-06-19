# SKYWAY 96 — 3D-Printable Switch Plate (CadQuery)

A **3D-printable** version of the switch plate, generated from the same validated
geometry as the laser-cut [`../Plate/skyway96_plate.dxf`](../Plate/) (99 switch
cutouts incl. combo + stabilizer, 11 screw holes, 4 edge notches, PCB frame
361.95 × 113.30 mm). Pairs with the case in
[`../Case/SKYWAY Custom (CadQuery)`](../Case/SKYWAY%20Custom%20(CadQuery)).

## Why it isn't a flat 1.5 mm sheet

MX top-clips are made for a **1.5 mm** plate. A flat 1.5 mm × 360 mm FDM print
warps, flexes, and is fragile. So this is a **stepped** plate:

```
top  ──┐  1.5 mm   exact DXF profile (14 mm body + 1 mm clip wings)  → clips snap
body ──┘  1.5 mm   opened to ≥16 mm square                           → housing clears
total      3.0 mm  → stiff, low warp
```

The switch top (14 mm) seats in the top layer and the clip catches the step
shelf at z = 1.5 mm — exactly like a real 1.5 mm plate. The wider lower layer
just clears the switch's bottom housing and adds rigidity.

## Files

| File | What |
|---|---|
| `plate.py` | Builds the one-piece stepped plate → `output/skyway96_plate.stl` |
| `plate_split.py` | Left + Right halves for a ~220 mm bed → `output/skyway96_plate_{left,right}.stl` |
| `preflight.py` | Overhang / bed-fit / warp check |
| `tools/run_model.py` | Runs a script, validates watertight, renders a 6-view PNG |

Regenerate (uses the case folder's `.venv`):

```bash
PY="../Case/SKYWAY Custom (CadQuery)/.venv/Scripts/python.exe"
"$PY" plate.py            # one-piece
"$PY" plate_split.py      # L/R halves
"$PY" preflight.py
```

## Variants

| Print | Size (mm) | Bed |
|---|---|---|
| `skyway96_plate.stl` | 361 × 113 × 3 | 350 mm+ only |
| `skyway96_plate_left.stl` | 198 × 113 × 3 | any ≥ 220 |
| `skyway96_plate_right.stl` | 176 × 113 × 3 | any ≥ 220 |

### Split seam
At **x = 192 mm**, clear of the spacebar. A 96% layout has no full-height clear
column (stagger), so the seam **jogs** around the 3 cutouts it would cross —
every switch hole stays whole in one half, and the jog tongues key the halves
together in X and Y. Glue the seam faces; the PCB + screws lock the final stack.

## Screw holes (adaptive)

Each of the 11 holes is grown **as large as its neighbourhood allows** while
keeping a printable **1.0 mm** wall to the nearest cutout / hole / edge:

- 3 roomy holes (bottom row, near the edge) → **Ø5.0** (clears an M2 washer / a
  driver tip)
- 8 holes boxed in between switch cutouts → **~Ø2.4–2.5** (M2 shaft clearance)

The laser plate ran Ø4.0 everywhere on ~0.3 mm walls — fine for FR4, but those
walls won't print in FDM, so the crowded holes are deliberately smaller here.
Tune with `SCREW_WALL` / `SCREW_CAP_D` in `plate.py`.

## Print recipe

- Material: **PETG** (or PLA); 0.2 mm layers, 4 walls, 20 % infill
- **Print top-face DOWN** (flip in slicer) → the 14 mm clip openings print crisp
  on the bed and the step shelf prints fully supported. (Printed bottom-down also
  works; the ~1 mm step ledge is a trivial bridge.)
- **No supports.**
- **Brim** — 360 mm (one-piece) / ~190 mm (halves) flat parts are warp-prone.

## Assembly

1. Drop switches through the plate; clips snap at the 1.5 mm step.
2. Seat the switch pins into the PCB hotswap sockets (plate + PCB sandwich).
3. (split) glue the two halves at the jogged seam before populating across it.
4. Screw the PCB down into the case standoffs as normal.

## Source

Geometry from KiCad `MX1–MX99` switch centers via the laser plate DXF
([KB_PLATE_VALIDATOR](https://github.com/RivasMario/KB_PLATE_VALIDATOR)),
re-lofted to a stepped solid in CadQuery (OpenCASCADE).
