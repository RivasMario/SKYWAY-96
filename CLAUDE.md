# Keyboard Projects Handoff

## 1. SKYWAY-96 (Good Baseline)
- **Status**: Stable and verified.
- **Lessons Learned**: RP2040 SMD stack (Flash, LDO, Crystal, ESD) is the blueprint for future projects.
- **Recent Updates**: RGB animations enabled, VIA/Remap "lighting" tag added, verified layout backup created.

## 2. Delta Split 75 (Original Replication)
- **Location**: `C:\Users\v-mariorivas\OneDrive - Microsoft\Documents\GitHub\Delta Split 75`
- **Status**: Physical placement complete.
- **Done**: 
  - 86 Switches and 86 Diodes placed via script to match original 2017 Gerber geometry.
  - Pro Micro headers and TRRS jack placed.
  - Net definitions (`ROW0-8`, `COL0-9`, `S1_D1...`) added to PCB header.
- **Next Steps**: Link Pro Micro pins to nets in KiCad and finalize copper routing to match original Gerbers.

## 3. deltasplit75-rp2040 (New Upgrade)
- **Location**: `C:\Users\v-mariorivas\OneDrive - Microsoft\Documents\GitHub\deltasplit75-rp2040`
- **Status**: Initialized.
- **Done**:
  - Project created with `docs/RP2040_SMD_GUIDE.md`.
  - Schematic core started with two **RP2040 MCUs** (dual-master split design).
  - Symbol libraries linked (MCU, Memory, Power).
- **Next Steps**: 
  - Complete the RP2040 supporting circuits (Flash, 12MHz Crystal, AMS1117-3.3V).
  - Implement USB-C interconnect communication (UART Rx/Tx) based on the "modern" Fiverr schematic analysis.

## 4. PublicSecurity96 (To Be Fixed)
- **Location**: `C:\Users\v-mariorivas\OneDrive - Microsoft\Documents\GitHub\PublicSecurity96`
- **Status**: On hold.
- **Issue**: "Bad" engineering from a previous designer. Missing RGB, ESD, and potentially unstable power circuit.
- **Plan**: After Delta Split 75 is finished, "re-skin" the good SKYWAY-96 project to replace this one.
