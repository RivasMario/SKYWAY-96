# Case — SKYWAY 96

![Case preview](case-preview.png)

Two 3D-printable case designs fit the SKYWAY 96 PCB. Both target the **Melody96 / YMDK96** 96% footprint the board is based on.

| Design | Folder | Construction | Tilt | Bed need |
|---|---|---|---|---|
| **Melody96 (HughMann)** | `Melody96 Case (HughMann)/` | 3-piece: L + Stripe + R (+ one-piece remix) | optional 5° riser | small (split) → large (1pc) |
| **96% (RobotDoctor)** | `96% Case (RobotDoctor)/` | 2-piece: L + R | built into model (angle vs flat) | small |
| **SKYWAY Custom (CadQuery)** | `SKYWAY Custom (CadQuery)/` | tray, 15× M2 posts; 1-piece **or** lap-split L/R; 6° feet | flat or 6° feet | 369 mm 1pc / 220 mm split |

The **SKYWAY Custom** tray is an original parametric design (CadQuery) fitted to
*this* PCB's exact outline + USB position — see its README to edit/regenerate.

See each folder's `README.md` for the full parts list.

---

## Design spec — what you need to make your own case

Both cases are built around the **same PCB**, so the hard constraints below are fixed. Everything else (wall style, seam, tilt) is a design choice — the two cases just make different choices.

### Fixed constraints (from the PCB / 96% standard)
| Spec | Value | Source |
|---|---|---|
| Layout footprint | Melody96 / YMDK96 96% | board lineage |
| Key pitch | 19.05 mm | MX standard |
| Switch cutout | 14.0 × 14.0 mm | MX plate |
| Plate thickness | 1.5 mm | MX clip seat |
| Mount holes present | M2 (1.75 mm) + M3 (3.0 mm) | `NPTH.drl` |
| PCB outline ref | `3D Step File/PCB 3D.step` | exact edge + holes |

### How the two cases solve it
| Aspect | Melody96 (HughMann) | 96% (RobotDoctor) |
|---|---|---|
| Pieces | 3 (L + Stripe + R) | 2 (L + R) |
| Seam | center stripe joins halves | direct center seam |
| Alignment | printed dowels | model-mated edge |
| Tilt | separate 5° riser parts | baked in: **angle** or **flat** body |
| Wall options | standard **or** 2 mm | single wall (per variant) |
| Assembled W × D × H | 387.6 × 140.3 × 21.7 mm | ≈376 × 128.8 × 31.5 (angle) / 18.0 (flat) |
| Half max footprint | 221.9 × 140.3 mm (Body R) | 188.0 × 128.8 mm |
| PCB hold | standoffs + dowels + feet | integrated bosses |
| Extras included | risers, feet, dowels, standoffs, remixes | none — body only |

### Compare / contrast — takeaways
- **Modularity:** Melody96 is a kit (swap stripe, risers, wall thickness, remixes). RobotDoctor is monolithic — fewer choices, fewer parts to align.
- **Tilt strategy:** Melody96 = add-on riser (mix and match). RobotDoctor = pick angle vs flat at print time (no extra parts, but no in-between).
- **Print effort:** RobotDoctor halves (max 188 mm) print on any bed with no stripe/dowel steps. Melody96 split also fits small beds but has more pieces; its one-piece remix needs a ~388 mm bed.
- **Assembly:** Melody96 needs dowels + standoffs + feet. RobotDoctor mates halves directly.
- **Hardware:** Melody96 ships printable hardware (feet/dowels/standoffs); RobotDoctor expects you to mount the PCB to integrated bosses (see its `Images/pcb_marked_1.jpg`).

### To design a fresh case
1. Pull exact outline + hole positions from `3D Step File/PCB 3D.step`.
2. Pull key positions from `skyway96.layout.json` (or `KLE DATA/`).
3. Use the fixed constraints table above for plate cutouts (19.05 pitch, 14×14, 1.5 mm).
4. Choose construction (tray / sandwich / split like these two), tilt, wall thickness.

Want a parametric OpenSCAD case generated from these? Pick tray vs sandwich and a tilt angle.
