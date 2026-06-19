# Case — 96% (RobotDoctor)

Second 3D-printable case option for the SKYWAY 96 PCB.

Design by **RobotDoctor** — [Thingiverse thing #4401525](https://www.thingiverse.com/thing:4401525). Files mirrored here for convenience; CC Attribution license (see `LICENSE.txt`).

## Print Layout

Prints in two halves (**left** + **right**), no center stripe. Choose **one** tilt variant:

```
[ left half ] [ right half ]
   angle  (5° typing tilt)
   flat   (0° low profile)
```

## Parts

### `Main Body/`
| File | Notes |
|---|---|
| `96plate_angle_left.STL` / `96plate_angle_right.STL` | Tilted variant — built-in typing angle |
| `96plate_flat_left.STL` / `96plate_flat_right.STL` | Flat variant — low profile |

> Print **either** the angle pair **or** the flat pair — not both.

## Dimensions (STL bounding box, mm)

| File | W × D × H |
|---|---|
| `96plate_angle_left` / `_right` | 188.0 × 31.5 × 128.8 |
| `96plate_flat_left` / `_right` | 188.0 × 18.0 × 128.8 |

Halves are modeled on their side (Z = board depth). Two halves seam at center → assembled width ≈ 376 mm. Fits the Melody96 / YMDK96 96% footprint shared by the SKYWAY 96 PCB.

## Print Tips

- **Material:** PLA or PETG.
- **Bed size:** each half ≈ 188 × 129 mm — fits most beds; no large-bed one-piece needed.
- **Orientation:** print as oriented (long axis up) for clean side walls, or lay flat if your slicer adds supports for the key cutouts.
- See `Images/pcb_marked_1.jpg` for PCB mounting reference.
