# SKYWAY 96 — Hotswap Keyboard PCB

A 96% mechanical keyboard PCB built around the RP2040, with Kailh hotswap sockets and underglow RGB. Designed for JLCPCB assembly and Melody96-compatible cases.

![Keyboard](96%25%20Keyboard.png)

## Contents

- [Specs](#specs)
- [Photos & Renders](#photos--renders)
- [Layout](#layout)
- [Repository Layout](#repository-layout)
- [Firmware: Setup & Flashing](#firmware-setup--flashing)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)

---

## Specs

| | |
|---|---|
| MCU | RP2040 (QFN-56) |
| Flash | W25Q128JVS (128 Mb, SOIC-8) |
| Layout | 96% — 99 keys |
| Switches | Kailh hotswap (MX compatible) |
| RGB | 18× WS2812B underglow |
| USB | USB-C (HRO TYPE-C-31-M-12) |
| Regulator | AMS1117-3.3 |
| ESD | PRTR5V0U2X |
| Firmware | QMK + VIA / Vial |
| Case | Melody96 / YMDK96 compatible (see [`Case/`](Case/)) |

---

## Photos & Renders

| PCB | Layout |
|---|---|
| ![PCB Top](PCB.png) | ![PCB Layout](PCB%20Layout.png) |

| Rendered Top | Rendered Back |
|---|---|
| ![Rendered Top](<3D%20Images/Renderred%20Top.png>) | ![Rendered Back](<3D%20Images/Renderred%20Back.png>) |

| Board Top | Board Bottom |
|---|---|
| ![Board Top](<3D%20Images/Board%20Top.png>) | ![Board Bottom](<3D%20Images/Board%20Bottom.png>) |

More renders (keycaps, stabilizers, alternate angles) live in [`3D Images/`](<3D%20Images/>).

### 3D-Printable Case

Melody96-compatible printed case — full part breakdown in [`Case/`](Case/).

![Case preview](<Case/case-preview.png>)

---

## Layout

96% — 99 keys. Matrix is 6 rows × 19 columns (COL2ROW).

| 2D Layout | KLE |
|---|---|
| ![96% Layout](<3D%20Images/96%25%20Layout.png>) | ![Layout](<KLE%20DATA/96%25.png>) |

Wiring, key labels, and VIA labelling diagrams are in [`KLE DATA/`](<KLE%20DATA/>).

---

## Repository Layout

| Folder | Contents |
|---|---|
| [`qmk_src/`](qmk_src/) | QMK firmware source + VIA keymap |
| [`Manufacturing & Assembly Files/`](<Manufacturing%20&%20Assembly%20Files/>) | BOM, CPL, Gerbers (for JLCPCB) |
| [`KiCAD Source Files/`](<KiCAD%20Source%20Files/>) | KiCad project + schematics |
| [`Schematic/`](Schematic/) | Schematic PDF |
| [`3D Step File/`](<3D%20Step%20File/>) | STEP / 3D model files |
| [`3D Images/`](<3D%20Images/>) | Renders and 2D images |
| [`KLE DATA/`](<KLE%20DATA/>) | Keyboard-Layout-Editor data + diagrams |
| [`VIA Json/`](<VIA%20Json/>) | VIA / Vial config + layout backups |
| [`Layout PDFs/`](<Layout%20PDFs/>) | Printable layout / keymap PDFs |
| [`Case/`](Case/) | 3D-printable case (Melody96-compatible) |

---

## Firmware: Setup & Flashing

### 1. Install the toolchain
You need the [QMK CLI](https://docs.qmk.fm/newbs_getting_started) and the `arm-none-eabi` toolchain. On Fedora:
```bash
sudo dnf install -y arm-none-eabi-gcc-cs-c++ arm-none-eabi-newlib arm-none-eabi-binutils
```

### 2. Link the source into QMK
```bash
ln -sf "$(pwd)/qmk_src" ~/qmk_firmware/keyboards/skyway96
```

### 3. Compile
```bash
qmk compile -kb skyway96 -km via
```
Produces `skyway96_via.uf2` in your `qmk_firmware` directory.

### 4. Flash
1. Enter bootloader: **hold BOOT → tap RESET → release BOOT**.
2. The board mounts as a USB drive named `RPI-RP2`.
3. Drag `skyway96_via.uf2` onto that drive, **or** run:
   ```bash
   qmk flash -kb skyway96 -km via
   ```

---

## Troubleshooting

### Linux USB detection (udev)
If VIA / Remap doesn't see the board on Linux, add a udev rule:
```bash
export USER_GID=`id -g`; sudo --preserve-env=USER_GID sh -c 'echo "KERNEL==\"hidraw*\", SUBSYSTEM==\"hidraw\", ATTRS{idVendor}==\"6969\", ATTRS{idProduct}==\"0096\", MODE=\"0660\", GROUP=\"$USER_GID\", TAG+=\"uaccess\", TAG+=\"udev-acl\"" > /etc/udev/rules.d/99-skyway96.rules && udevadm control --reload && udevadm trigger'
```

### Restore the "known good" layout
A verified layout backup (with RGB controls on Layer 1) lives at:
`VIA Json/skyway96_GOOD_BACKUP_2026-04-23.json`
Sideload it in VIA / Remap after flashing.

### GitHub push fails (password auth disabled)
Switch the remote to SSH:
```bash
git remote set-url origin git@github.com:RivasMario/SKYWAY-96.git
```
Make sure your SSH key (e.g. `~/.ssh/github`) is loaded in your SSH agent or set in `~/.ssh/config`.

---

## Credits

- **PCB** — Ahsan Mehmood Awan · `engrahsanmehmoodawan@gmail.com`
- **Case** — HughMann · [Thingiverse #3883](https://www.thingiverse.com/thing:3883)
