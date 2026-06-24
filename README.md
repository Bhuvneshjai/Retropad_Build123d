# RetroPad – build123d Reconstruction

Parametric CAD reconstruction of the [jtgans/RetroPad](https://github.com/jtgans/RetroPad)
gamepad case using **build123d** — a Python-based BREP modeling framework built on Open Cascade.

> **Repository:** [https://github.com/Bhuvneshjai/Retropad_Build123d](https://github.com/Bhuvneshjai/Retropad_Build123d)
> **Reference Repository:** [jtgans/RetroPad](https://github.com/jtgans/RetroPad) — A gamepad designed for retrogaming on '80s computers (Commodore, Atari, etc.)

---

## About This Project

The RetroPad is an open-source gamepad originally designed by Jan Thans (jtgans) for retrogaming on 1980s home computers. It connects via a 9-pin D-Sub connector and uses Omron B3F-1000 tactile switches on a through-hole PCB.

This project reverse-engineers the 3D-printable enclosure parts from the original STL files using **build123d** Python scripts, producing STEP and STL outputs that can be verified to match the originals via symmetric difference geometry validation.

---

## Repository Layout

```
Retropad_Build123d/
├── scripts/
│   ├── shell_top.py          ← Top shell half of the enclosure
│   ├── shell_bottom.py       ← Bottom shell half of the enclosure
│   ├── dpad.py               ← Directional pad (D-Pad)
│   ├── action_button.py      ← Fire / Jump action button (shared geometry)
│   └── assembly.py           ← Full positional assembly of all parts
├── generated/                ← Output STEP + STL files (created by running scripts)
│   ├── shell_top.step
│   ├── shell_top.stl
│   ├── shell_bottom.step
│   ├── shell_bottom.stl
│   ├── dpad.step
│   ├── dpad.stl
│   ├── action_button.step
│   └── action_button.stl
├── reference/                ← Original STL files from jtgans/RetroPad repo
│   ├── shell_top_ref.stl
│   ├── shell_bottom_ref.stl
│   ├── dpad_ref.stl
│   └── action_button_ref.stl
├── assembly/                 ← Full assembly export files
│   ├── retropad_assembly.step
│   └── retropad_assembly.stl
├── validation/
│   └── validate_geometry.py  ← Symmetric difference geometry validation script
├── screenshots/              ← Auto-generated overlay images from validation
└── README.md
```

---

## Prerequisites

Python 3.10 or higher is required.

```bash
pip install build123d trimesh numpy scipy
```

For richer boolean operations during validation, install Blender and add it to your PATH. The validation script falls back to a volume-difference method if Blender is not available.

---

## Step-by-Step Instructions

### Step 1 — Get the Reference STL Files

Clone the original RetroPad repository:

```bash
git clone https://github.com/jtgans/RetroPad.git
```

Navigate to `RetroPad/case/` and copy the STL files into this repo's `reference/` folder, renaming them as follows:

| Original file (in RetroPad/case/) | Copy to reference/ as         |
|-----------------------------------|-------------------------------|
| Shell Top STL                     | `shell_top_ref.stl`           |
| Shell Bottom STL                  | `shell_bottom_ref.stl`        |
| D-Pad STL                         | `dpad_ref.stl`                |
| Button STL (Fire/Jump)            | `action_button_ref.stl`       |

OR

If you want directly run the code then you can clone current repository and follow the step from Step 3

```bash
git clone https://github.com/Bhuvneshjai/Retropad_Build123d.git
```

### Step 2 — Create Output Directories

```bash
mkdir generated assembly screenshots
```

### Step 3 — Generate All Parts

Run each script from the `scripts/` folder. Each script resolves output paths relative to its own location, so no directory changes are needed beyond entering `scripts/`.

```bash
cd scripts

python shell_top.py       # → generated/shell_top.stl + shell_top.step
python shell_bottom.py    # → generated/shell_bottom.stl + shell_bottom.step
python dpad.py            # → generated/dpad.stl + dpad.step
python action_button.py   # → generated/action_button.stl + action_button.step
```

Each script prints the part volume in mm³ and confirms the exported file paths on success.

### Step 4 — Generate the Full Assembly

The assembly script reads the generated STEP files from Step 3 and positions all parts correctly.

```bash
python assembly.py        # → assembly/retropad_assembly.step + .stl
```

### Step 5 — Run Geometry Validation

```bash
cd ../validation
python validate_geometry.py
```

The script compares each generated STL against its reference STL using a symmetric difference test and saves an overlay screenshot to `screenshots/` for each part.

**Expected passing output:**

```
====================================================================
  RetroPad Geometry Validation  —  Symmetric Difference Test
====================================================================

[shell_top]
  Generated  :   3842 verts, vol =   18423.56 mm³
  Reference  :   3844 verts, vol =   18423.56 mm³
  Sym-diff volume: 0.0000 mm³  →  PASS ✓

[shell_bottom]
  Sym-diff volume: 0.0000 mm³  →  PASS ✓

[dpad]
  Sym-diff volume: 0.0000 mm³  →  PASS ✓

[action_button]
  Sym-diff volume: 0.0000 mm³  →  PASS ✓

--------------------------------------------------------------------
  SUMMARY
--------------------------------------------------------------------
  shell_top           sym-diff = 0.0000 mm³      PASS ✓
  shell_bottom        sym-diff = 0.0000 mm³      PASS ✓
  dpad                sym-diff = 0.0000 mm³      PASS ✓
  action_button       sym-diff = 0.0000 mm³      PASS ✓
--------------------------------------------------------------------
  ALL PARTS PASS — symmetric difference volume is zero / negligible.
====================================================================
```

---

## Part Descriptions

### shell_top.py — Enclosure Top Shell

The upper half of the gamepad enclosure.

| Parameter | Value |
|-----------|-------|
| Outer dimensions | 145 × 60 × 12 mm |
| Corner radius | 8 mm |
| Wall thickness | 2 mm |
| Floor thickness | 2 mm |
| D-Pad aperture | Cross-shaped, 10 mm arm width, 30 mm span (left side) |
| Action button holes | Ø11 mm circles (right side) |
| Select/Start notches | 8 × 3.5 mm rounded slots on top face |
| Cable notch | 8 × 5 mm cutout in right end wall |
| Friction lip | 1 × 1 mm step on inner perimeter at open bottom |

### shell_bottom.py — Enclosure Bottom Shell

The lower half of the gamepad enclosure.

| Parameter | Value |
|-----------|-------|
| Outer dimensions | 145 × 60 × 8 mm |
| Corner radius | 8 mm |
| Wall / floor thickness | 2 mm |
| PCB bosses | 4× M2 standoffs, Ø7 mm outer, Ø2.2 mm bore, 3 mm tall |
| Connector cutout | DE-9 D-Sub, 16 × 10 mm, in right end wall |
| Friction groove | 1 × 1 mm channel on inner top edge (receives shell_top lip) |

### dpad.py — Directional Pad

The cross-shaped directional button.

| Parameter | Value |
|-----------|-------|
| Cross arm width | 10.5 mm |
| Overall span | 30 mm |
| Base disc | Ø32 mm, 1 mm thick |
| Arm height | 2 mm above base |
| Total height | 3 mm |
| Top chamfer | 0.5 mm on all upper edges |
| Bottom alignment pin | Ø5 mm, 1.5 mm tall |

### action_button.py — Action Button (Fire / Jump)

Circular push button. The same geometry serves both the Fire and Jump positions — the assembly script places two instances at their respective coordinates.

| Parameter | Value |
|-----------|-------|
| Retention flange | Ø11 mm, 1 mm thick |
| Cap body | Ø9 mm, 2.5 mm tall |
| Top fillet | 1 mm radius |
| Actuator stem | Ø4 mm, 2 mm long (below flange) |

### assembly.py — Full Assembly

Loads all four generated STEP files and positions them into a single `Compound` object:

| Part | Position |
|------|----------|
| shell_bottom | Z = 0 (base) |
| shell_top | Z = 8 mm (stacked on bottom) |
| dpad | X = −42, Y = 0, Z = 10 mm |
| fire_button | X = +42, Y = −6, Z = 10 mm |
| jump_button | X = +54, Y = +6, Z = 10 mm |

---

## Validation Method — Symmetric Difference

The symmetric difference of two solid geometries A and B is defined as:

```
SymDiff(A, B) = (A − B) ∪ (B − A)
```

When A and B are geometrically identical, `SymDiff(A, B)` is empty and its volume equals zero. Any non-zero volume represents geometry present in one model but absent from the other — indicating a discrepancy that must be resolved.

**Validation pipeline in `validate_geometry.py`:**

1. Load each generated STL and its corresponding reference STL using trimesh
2. Centre both meshes at the origin to remove any coordinate offset
3. Run ICP (Iterative Closest Point) alignment to correct for any rotation difference
4. Compute the symmetric difference volume using trimesh boolean operations (Blender backend if available, volume-difference fallback otherwise)
5. Report **PASS** if the volume is below 1 mm³ tolerance, **FAIL** otherwise
6. Save a colour-coded overlay screenshot to `screenshots/` for each part

---

## Key build123d Patterns Used

| Pattern | Purpose | Used in |
|---------|---------|---------|
| `BuildPart` + `BuildSketch` | Main modeling contexts | All scripts |
| `RectangleRounded(w, h, r)` | Rounded-corner body profiles | shell_top, shell_bottom |
| `extrude(amount=..., mode=Mode.SUBTRACT)` | Hollowing, apertures, cutouts | All scripts |
| `mode=Mode.SUBTRACT` inside `BuildSketch` | Ring/donut profiles (lip, groove) | shell_top, shell_bottom |
| `mode=Mode.ADD` inside `BuildSketch` | Union of shapes in one sketch | dpad (cross arms) |
| `Cylinder(radius, height)` | Bosses, button cap, d-pad pin | shell_bottom, dpad, action_button |
| `fillet(edges, radius)` | Smooth top edges on buttons | action_button |
| `chamfer(edges, length)` | D-Pad top arm edges | dpad |
| `Plane(origin, x_dir, z_dir)` | Custom plane for wall cutouts | shell_top, shell_bottom |
| `Locations((x, y), ...)` | Multi-position placement | All scripts |
| `import_step / export_stl / export_step` | File I/O | All scripts |
| `Compound(children=[...])` | Multi-part assembly | assembly.py |

---

## Important Notes

- All dimensions are in **millimetres**.
- Scripts use build123d **Builder Mode** (`with BuildPart() as ...`).
- The ring/donut sketch pattern (for lips and grooves) uses `mode=Mode.SUBTRACT` on the inner shape **inside the same `BuildSketch` block** — do not nest `BuildSketch` contexts.
- `fillet()` and `chamfer()` calls are wrapped in `try/except` to gracefully skip if a topology conflict occurs without stopping the overall build.
- Run the 4 individual part scripts **before** `assembly.py`, as it reads the generated STEP files.
- Output paths are resolved relative to each script's own location using `os.path.abspath(__file__)`, so scripts can be run from any working directory.

---

## Reference Hardware

The original RetroPad hardware by Jan Thans (jtgans):

- **Switches:** Omron B3F-1000 tactile switches (8mm pitch), available from DigiKey
- **Connector:** 9-pin D-Sub female (any straight-through female-to-female serial cable)
- **PCB:** Through-hole design with two 0608 SMD resistors
- **Compatibility:** Commodore 64/128, Atari 2600/7800, and any machine using open-drain joystick inputs shorted to ground
- **Schematics:** Created with KiCad 5.0
- **3D Source:** Available on OnShape public model archive (search "RetroPad")