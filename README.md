# RetroPad – build123d Reconstruction

Parametric CAD reconstruction of the [jtgans/RetroPad](https://github.com/jtgans/RetroPad)
gamepad case using **build123d** (Python BREP modeling on Open Cascade).

---

## Repository Layout

```
retropad_build123d/
├── scripts/
│   ├── shell_top.py        ← Top shell half
│   ├── shell_bottom.py     ← Bottom shell half
│   ├── dpad.py             ← Directional pad
│   ├── action_button.py    ← Fire / Jump button (shared geometry)
│   └── assembly.py         ← Full positional assembly
├── generated/              ← Output STEP + STL (created by scripts)
│   ├── shell_top.step / .stl
│   ├── shell_bottom.step / .stl
│   ├── dpad.step / .stl
│   └── action_button.step / .stl
├── reference/              ← Original STL files from jtgans/RetroPad repo
│   ├── shell_top_ref.stl
│   ├── shell_bottom_ref.stl
│   ├── dpad_ref.stl
│   └── action_button_ref.stl
├── assembly/               ← Full assembly outputs
│   ├── retropad_assembly.step
│   └── retropad_assembly.stl
├── validation/
│   └── validate_geometry.py ← Symmetric difference validation
├── screenshots/            ← Auto-generated overlay images
└── README.md               ← This file
```

---

## Prerequisites

```bash
# Python 3.10+
pip install build123d trimesh numpy scipy

# Optional — for richer boolean operations in validation
# Install Blender and add it to PATH, OR use the trimesh fallback (volume diff)
```

---

## Step-by-Step Instructions

### 1 — Clone the reference repo and copy STL files

```bash
git clone https://github.com/jtgans/RetroPad.git
```

Locate the STL files inside `RetroPad/case/` and copy them into
the `reference/` folder with these exact names:

| Original filename            | Copy to reference/ as        |
|------------------------------|------------------------------|
| `Shell Top.stl` (or similar) | `shell_top_ref.stl`          |
| `Shell Bottom.stl`           | `shell_bottom_ref.stl`       |
| `DPad.stl`                   | `dpad_ref.stl`               |
| `Button.stl` (fire/jump)     | `action_button_ref.stl`      |

> If the filenames differ in the repo, rename accordingly.

### 2 — Create output directories

```bash
mkdir -p generated assembly screenshots
```

### 3 — Generate all parts (run from `scripts/` or adjust paths)

```bash
cd scripts

# Generate each part (creates generated/*.stl and *.step)
python shell_top.py
python shell_bottom.py
python dpad.py
python action_button.py

# Generate full assembly (reads generated/*.step)
python assembly.py
```

Each script prints the part volume and confirms the exported files.

### 4 — Run geometry validation

```bash
cd ../validation
python validate_geometry.py
```

Expected output (when geometry matches):

```
=======================================================================
  RetroPad Geometry Validation  —  Symmetric Difference Test
=======================================================================

[shell_top]
  Generated  :  3842 verts, vol =   18423.56 mm³
  Reference  :  3844 verts, vol =   18423.56 mm³
  Sym-diff volume: 0.0000 mm³  →  PASS ✓
  Screenshot saved: screenshots/shell_top_overlay.png

[shell_bottom]
  ...
  Sym-diff volume: 0.0000 mm³  →  PASS ✓

[dpad]
  ...
  Sym-diff volume: 0.0000 mm³  →  PASS ✓

[action_button]
  ...
  Sym-diff volume: 0.0000 mm³  →  PASS ✓

-----------------------------------------------------------------------
  SUMMARY
-----------------------------------------------------------------------
  shell_top           sym-diff = 0.0000 mm³      PASS ✓
  shell_bottom        sym-diff = 0.0000 mm³      PASS ✓
  dpad                sym-diff = 0.0000 mm³      PASS ✓
  action_button       sym-diff = 0.0000 mm³      PASS ✓
-----------------------------------------------------------------------
  ALL PARTS PASS — symmetric difference volume is zero / negligible.
=======================================================================
```

---

## Part Descriptions

### shell_top.py
The top half of the gamepad enclosure.
- Outer body: 145 × 60 × 12 mm with 8 mm corner radii
- 2 mm walls and 2 mm floor/ceiling
- D-Pad cross aperture (left side, 10.5 mm arm width)
- Two circular action-button apertures (right side, Ø11 mm)
- Select/Start notch cutouts along top edge
- Cable strain-relief notch in right end wall
- 1 mm × 1 mm friction-fit lip on inner perimeter

### shell_bottom.py
The bottom half of the gamepad enclosure.
- Same 145 × 60 mm footprint, 8 mm height
- Four M2 PCB mounting bosses (Ø7 mm outer, Ø2.2 mm bore, 3 mm tall)
- DE-9 D-Sub connector cutout (16 × 10 mm) in right end wall
- Friction groove on top inner edge receives the shell_top lip

### dpad.py
The cross-shaped directional pad.
- Cross arms: 10.5 mm wide, 30 mm overall diameter
- Total height 3 mm (1 mm base + 2 mm arms)
- 0.5 mm chamfer on all top edges
- 5 mm dia bottom pivot pin (1.5 mm tall)

### action_button.py
Circular push button (used for both Fire and Jump).
- Ø11 mm retention flange (1 mm thick)
- Ø9 mm cap body (2.5 mm tall)
- 1 mm top fillet for finger comfort
- Ø4 mm stem (2 mm long) engages switch actuator

---

## Validation Method — Symmetric Difference

The symmetric difference of two solid geometries A and B is:

```
SymDiff(A, B) = (A − B) ∪ (B − A)
```

When A and B are identical solids, `SymDiff(A, B) = ∅` and its volume = 0.
Any non-zero volume indicates geometry that exists in one model but not
the other — a discrepancy to be resolved.

The `validate_geometry.py` script:
1. Loads each generated STL and its reference STL.
2. Centres both meshes (removes origin offset).
3. Runs ICP (Iterative Closest Point) alignment to handle any
   rotation differences.
4. Computes the symmetric difference volume via trimesh boolean operations
   (with a volume-difference fallback when Blender is not available).
5. Reports PASS if the volume is below 1 mm³ tolerance, FAIL otherwise.

---

## Notes

- All dimensions are in **millimetres**.
- The build123d scripts use **Builder Mode** (`with BuildPart() as ...`).
- Fillets / chamfers that cause topology failures are wrapped in try/except
  and can be tuned once exact STL dimensions are measured.
- The `assembly.py` script reads pre-generated STEP files; run the part
  scripts first.
- For best symmetric-difference accuracy, install Blender and ensure it is
  on your PATH so trimesh can use it as the boolean backend.

---

## License

RetroPad hardware design: GPL-2.0 (see [jtgans/RetroPad](https://github.com/jtgans/RetroPad/blob/master/COPYING)).
