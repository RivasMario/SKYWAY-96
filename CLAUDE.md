# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**SKYWAY 96** — a custom 96% hotswap keyboard PCB. RP2040-based, Kailh hotswap sockets, 18x WS2812B underglow, QMK + VIA/Vial firmware, designed for JLCPCB assembly.

## QMK Firmware

To compile the firmware, QMK must be set up separately (see [qmk.fm](https://qmk.fm)). The keyboard folder name for QMK is `skyway96`.

```bash
# Compile
qmk compile -kb skyway96 -km via

# Flash (put board in bootloader mode first via BOOT + RESET buttons)
qmk flash -kb skyway96 -km via
```

To enter bootloader: hold BOOT button, tap RESET, release BOOT. Board mounts as a USB drive (RP2040 UF2 bootloader).

## Firmware Architecture

All firmware lives in `QMK Firmware/`:

| File | Purpose |
|---|---|
| `info.json` | Keyboard identity, matrix pins, RGB config — source of truth for pin assignments |
| `config.h` | Mirrors `info.json` for older QMK compatibility |
| `rules.mk` | Enables RGBLIGHT, WS2812 PIO driver, VIA |
| `skyway96.c` | Post-init: drives GP26 high (status LED) |
| `keymaps/via/keymap.c` | Default keymap, VIA-remappable |
| `via.json` | VIA app layout definition |

`VIA Json/vial.json` is the Vial app layout (a VIA fork with more features). VIA and Vial use the same VID/PID (`0xFEED` / `0x0001`).

## Pin Assignments

| GPIO | Function |
|---|---|
| GP0–GP5 | Matrix rows (Row0–Row5) |
| GP6–GP24 | Matrix columns (Col0–Col18) |
| GP25 | WS2812B RGB data (underglow) |
| GP26 | Status LED output |

Matrix is 6×19 = 114 positions, COL2ROW diode direction. ~99 positions are populated (rest are KC_NO).

## Key Files for Manufacturing

All in `Manufacturing & Assembly Files/`:
- `BOM Partlist.xlsx` — correct BOM for JLCPCB assembly
- `CPL Pickplace.xlsx` — component placement file
- `Gerber File/` — fabrication files

**Do not use** `KiCAD Source Files/rivasmario 96% Hotswap Rp2040.xml` — it is a leftover from a different project (65% ATmega32U4 keyboard) and has wrong parts.

## KiCad Source

Main schematic: `KiCAD Source Files/rivasmario 96% Hotswap Rp2040.kicad_sch`
Sub-sheets: `Hotswap Switch Matrix.kicad_sch`, `RGBLeds.kicad_sch`
Custom footprints: `KiCAD Source Files/Library.pretty/`

The schematic uses global net labels (Row0–Row5, Col0–Col18, RGB_Underglow) to connect the switch matrix and RGB sub-sheets to the RP2040 on the main sheet.
