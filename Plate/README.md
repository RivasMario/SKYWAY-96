# Switch Plate

Switch/stabilizer mounting plate for the SKYWAY 96 PCB.

![Switch plate](skyway96_plate.png)

| | |
|---|---|
| Size | 361.95 × 114.30 mm |
| Switch cutouts | 100 (Cherry MX, 14 mm) incl. 5 combo (space, enter, backspace, numpad enter/plus) |
| Screw holes | 11 × M2 (2.2 mm), aligned to PCB mounting holes |
| Edge notches | bottom + left, cut into perimeter |
| Format | `skyway96_plate.dxf` — layered (outline / switch / stab / screw) |

Cut from 1.5 mm FR4, brass, aluminium, or POM (laser / waterjet). The DXF is
SendCutSend-ready (no zero-length segments).

## Source

Generated from the KLE layout + `KiCAD Source Files/*.kicad_pcb` by
[**KB_PLATE_VALIDATOR**](https://github.com/RivasMario/KB_PLATE_VALIDATOR),
which auto-registers the plate to the PCB and validates that every M2 screw
clears all switch/stab cutouts. Regenerate:

```bash
python scripts/build_plate.py \
  --kle skyway96_kle.json \
  --pcb "../skyway-96/KiCAD Source Files/rivasmario 96% Hotswap Rp2040.kicad_pcb" \
  --out output/skyway96_plate.dxf --pad 0 --snap-screws
```
