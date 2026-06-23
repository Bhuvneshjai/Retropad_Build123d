"""
RetroPad Full Assembly - build123d script
Combines all 4 parts into a positioned assembly and exports it.

Part list:
  1. shell_bottom  – at Z=0
  2. shell_top     – stacked on top of shell_bottom (Z = 8.0)
  3. dpad          – seated in shell_top D-Pad aperture
  4. action_button – two instances (Fire + Jump) in shell_top apertures

Run this script AFTER the individual part scripts have been executed so that
the generated/*.step files exist. Alternatively it can import the part modules
directly.
"""

from build123d import *
import os, sys

# ── Locate generated files (adjust path if running from repo root) ──────────────
BASE = os.path.dirname(__file__)
GEN  = os.path.join(BASE, "..", "generated")

def load_step(name: str) -> Solid:
    path = os.path.join(GEN, name)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing: {path}\nRun the individual part scripts first."
        )
    shapes = import_step(path)
    # import_step may return Compound; extract first Solid
    if isinstance(shapes, Compound):
        return shapes.solids()[0]
    return shapes

# ─── Load parts ────────────────────────────────────────────────────────────────
print("Loading parts…")
bottom  = load_step("shell_bottom.step")
top     = load_step("shell_top.step")
dpad    = load_step("dpad.step")
button  = load_step("action_button.step")

# ─── Position parameters (must match shell_top.py) ─────────────────────────────
H_BOT   = 8.0     # shell_bottom height
H_TOP   = 12.0    # shell_top height (from its own Z=0)

# D-Pad centre in shell_top local coords
DPAD_CX = -42.0
DPAD_CY =  0.0
DPAD_Z  =  H_BOT + 2.0   # floor thickness of shell_top = 2 mm

# Action button centres
BTN_FIRE  = ( 42.0, -6.0)
BTN_JUMP  = ( 54.0,  6.0)
BTN_Z     =  H_BOT + 2.0

# ─── Assemble ──────────────────────────────────────────────────────────────────
# Shell bottom sits at Z=0
bottom_placed  = bottom.moved(Location((0, 0, 0)))

# Shell top sits directly on top of bottom (friction fit)
top_placed     = top.moved(Location((0, 0, H_BOT)))

# D-Pad: the part's Z=0 is its bottom face; place it at the aperture centre
dpad_placed    = dpad.moved(Location((DPAD_CX, DPAD_CY, DPAD_Z)))

# Fire button
fire_placed    = button.moved(Location((BTN_FIRE[0], BTN_FIRE[1], BTN_Z)))

# Jump button
jump_placed    = button.moved(Location((BTN_JUMP[0], BTN_JUMP[1], BTN_Z)))

# ─── Build Compound ────────────────────────────────────────────────────────────
assembly = Compound(
    label="RetroPad_Assembly",
    children=[
        bottom_placed.label_("shell_bottom"),
        top_placed.label_("shell_top"),
        dpad_placed.label_("dpad"),
        fire_placed.label_("fire_button"),
        jump_placed.label_("jump_button"),
    ]
)

# ─── Export ────────────────────────────────────────────────────────────────────
out_step = os.path.join(GEN, "..", "assembly", "retropad_assembly.step")
out_stl  = os.path.join(GEN, "..", "assembly", "retropad_assembly.stl")

os.makedirs(os.path.dirname(out_step), exist_ok=True)

export_step(assembly, out_step)
export_stl(assembly,  out_stl)

print(f"Assembly saved:\n  {out_step}\n  {out_stl}")
print(f"Children: {[c.label for c in assembly.children]}")
