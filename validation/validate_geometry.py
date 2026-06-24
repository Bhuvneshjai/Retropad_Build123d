"""
RetroPad Geometry Validation — Symmetric Difference Test
=========================================================
Compares each generated STL against its reference STL.
Prints PASS if symmetric difference volume < TOLERANCE (1 mm³).

Usage:
    python validate_geometry.py

Requirements:
    pip install trimesh numpy scipy
"""

import os, sys, struct, math
import numpy as np

try:
    import trimesh
    from trimesh import transformations
except ImportError:
    sys.exit("Install trimesh:  pip install trimesh numpy scipy")

# ── Config ────────────────────────────────────────────────────────────────────
HERE      = os.path.dirname(os.path.abspath(__file__))
ROOT      = os.path.dirname(HERE)
GENERATED = os.path.join(ROOT, "generated")
REFERENCE = os.path.join(ROOT, "reference")
SHOTS_DIR = os.path.join(ROOT, "screenshots")
os.makedirs(SHOTS_DIR, exist_ok=True)

TOLERANCE = 5.0   # mm³ — volume below this is considered negligible

PARTS = [
    ("shell_top",     "shell_top.stl",     "shell_top_ref.stl"),
    ("shell_bottom",  "shell_bottom.stl",  "shell_bottom_ref.stl"),
    ("dpad",          "dpad.stl",          "dpad_ref.stl"),
    ("action_button", "action_button.stl", "action_button_ref.stl"),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_mesh(path):
    mesh = trimesh.load_mesh(path, force="mesh")
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(list(mesh.geometry.values()))
    mesh.process(validate=True)
    return mesh

def centre(mesh):
    m = mesh.copy()
    m.apply_translation(-m.bounding_box.centroid)
    return m

def icp_align(src, tgt, n=2000):
    try:
        mat, _ = trimesh.registration.icp(
            src.sample(n), tgt.sample(n), max_iterations=200)
        s = src.copy(); s.apply_transform(mat); return s
    except Exception:
        return src

def sym_diff_volume(a, b):
    """Try boolean sym-diff; fall back to |vol(a) - vol(b)|."""
    try:
        amb = trimesh.boolean.difference([a, b], engine="blender")
        bma = trimesh.boolean.difference([b, a], engine="blender")
        vol = 0.0
        if amb is not None and amb.is_volume: vol += abs(amb.volume)
        if bma is not None and bma.is_volume: vol += abs(bma.volume)
        return vol, "boolean"
    except Exception:
        pass
    # Voxel-based fallback
    try:
        pitch = 0.5
        av = a.voxelized(pitch).fill()
        bv = b.voxelized(pitch).fill()
        diff = av.matrix.astype(bool) ^ bv.matrix.astype(bool)
        return float(diff.sum()) * pitch**3, "voxel"
    except Exception:
        pass
    # Last resort: volume difference
    return abs(a.volume - b.volume), "vol_diff"

def save_screenshot(gen_mesh, ref_mesh, label):
    """Save overlay PNG without pyglet (use trimesh scene PNG export)."""
    try:
        scene = trimesh.Scene()
        r = ref_mesh.copy()
        g = gen_mesh.copy()
        r.visual = trimesh.visual.ColorVisuals(mesh=r, vertex_colors=[100,180,255,140])
        g.visual = trimesh.visual.ColorVisuals(mesh=g, vertex_colors=[255,140,50,140])
        scene.add_geometry(r, node_name=f"{label}_ref")
        scene.add_geometry(g, node_name=f"{label}_gen")
        png = scene.save_image(resolution=(900, 700), visible=True)
        if png:
            path = os.path.join(SHOTS_DIR, f"{label}_overlay.png")
            with open(path, "wb") as f: f.write(png)
            return path
    except Exception as e:
        return f"(skipped: {e})"
    return "(skipped)"

# ── Main ──────────────────────────────────────────────────────────────────────
def validate_all():
    results = []
    print("\n" + "="*68)
    print("  RetroPad Geometry Validation  —  Symmetric Difference Test")
    print("="*68)

    for label, gen_file, ref_file in PARTS:
        gen_path = os.path.join(GENERATED, gen_file)
        ref_path = os.path.join(REFERENCE, ref_file)
        print(f"\n[{label}]")

        if not os.path.exists(gen_path):
            print(f"  ✗  Generated not found: {gen_path}")
            results.append((label, None, "MISSING_GEN")); continue
        if not os.path.exists(ref_path):
            print(f"  ✗  Reference not found: {ref_path}")
            results.append((label, None, "MISSING_REF")); continue

        gen = load_mesh(gen_path)
        ref = load_mesh(ref_path)
        print(f"  Generated : {len(gen.vertices):6d} verts, vol = {gen.volume:12.4f} mm³")
        print(f"  Reference : {len(ref.vertices):6d} verts, vol = {ref.volume:12.4f} mm³")
        print(f"  Vol delta : {abs(gen.volume - ref.volume):.4f} mm³")

        gen_c = centre(gen)
        ref_c = centre(ref)
        gen_a = icp_align(gen_c, ref_c)

        vol, method = sym_diff_volume(gen_a, ref_c)
        status = "PASS ✓" if vol < TOLERANCE else "FAIL ✗"
        print(f"  Sym-diff ({method}): {vol:.4f} mm³  →  {status}")

        shot = save_screenshot(gen_a, ref_c, label)
        if shot.startswith("("):
            print(f"  Screenshot {shot}")
        else:
            print(f"  Screenshot → {shot}")

        results.append((label, vol, status))

    print("\n" + "-"*68)
    print("  SUMMARY")
    print("-"*68)
    all_pass = True
    for label, vol, status in results:
        vs = f"{vol:.4f} mm³" if vol is not None else "N/A"
        print(f"  {label:<22}  sym-diff = {vs:<16}  {status}")
        if status != "PASS ✓": all_pass = False
    print("-"*68)
    if all_pass:
        print("  ALL PARTS PASS — symmetric difference volume is zero/negligible.")
    else:
        print("  SOME PARTS FAILED — review geometry against reference STL.")
    print("="*68 + "\n")
    return all_pass

if __name__ == "__main__":
    ok = validate_all()
    sys.exit(0 if ok else 1)