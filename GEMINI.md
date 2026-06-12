# GEMINI.md

This file provides instructional context for Gemini CLI when working in the `SKYWAY-96` repository.

## Project Overview

**SKYWAY 96** is a custom 96% (99-key) hotswap keyboard PCB project.
- **Hardware:** Based on the **RP2040** MCU (QFN-56), with Kailh hotswap sockets and 18x WS2812B underglow RGB LEDs.
- **Design:** Optimized for JLCPCB manufacturing and assembly.
- **Firmware:** Supports **QMK**, **VIA**, and **Vial**.

## Firmware Development (QMK)

The firmware source code is located in the `QMK Firmware/` directory.

### Build and Flash
Requires the [QMK CLI](https://qmk.fm) to be installed.
- **Compile:** `qmk compile -kb skyway96 -km via`
- **Flash:** 
  1. Put the board in bootloader mode: Hold the `BOOT` button, tap the `RESET` button, then release `BOOT`.
  2. Run: `qmk flash -kb skyway96 -km via`

### Key Files
| File | Purpose |
|---|---|
| `info.json` | Matrix pins, RGB configuration, and metadata. |
| `config.h` | Configuration overrides for QMK. |
| `rules.mk` | Feature flags (RGBLIGHT, VIA, etc.). |
| `keymaps/via/keymap.c` | Default keymap and VIA configuration. |
| `via.json` | Layout definition for the VIA application. |

## Hardware & PCB Design

- **MCU:** Raspberry Pi RP2040.
- **Flash:** W25Q128JVS (128Mb).
- **Matrix:** 6 rows × 19 columns (COL2ROW diodes).
- **RGB:** 18x WS2812B LEDs on GPIO 25.
- **Design Tools:** KiCad 6.x or newer.

### Pin Assignments (GPIO)
- `GP0–GP5`: Matrix Rows (0-5).
- `GP6–GP24`: Matrix Columns (0-18).
- `GP25`: WS2812B RGB Data.
- `GP26`: Status LED.

## Manufacturing and Assembly

All files required for fabrication are in `Manufacturing & Assembly Files/`:
- **BOM:** `BOM Partlist.xlsx` (optimized for JLCPCB).
- **CPL:** `CPL Pickplace.xlsx`.
- **Gerbers:** Located in `Gerber File/`.

> [!IMPORTANT]
> **Do not use** `KiCAD Source Files/rivasmario 96% Hotswap Rp2040.xml`. It is a legacy file from a different project and contains incorrect component data.

## Directory Structure

| Path | Description |
|---|---|
| `KiCAD Source Files/` | KiCad project, schematics, and custom footprints. |
| `QMK Firmware/` | QMK firmware source and VIA configuration. |
| `VIA Json/` | JSON files for VIA and Vial apps. |
| `Schematic/` | PDF version of the circuit schematic. |
| `Photos/` | Renders of the PCB and final keyboard. |
| `KLE DATA/` | Keyboard Layout Editor data and wiring diagrams. |
