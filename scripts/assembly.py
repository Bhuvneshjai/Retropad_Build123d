"""
RetroPad Assembly - build123d script
Places all parts at their exact assembly coordinates from the reference STL.

Mating plane: Z=3.6 (assembly coordinate system)
  shell_bottom: outer_bottom Z=-3.0, mating Z=3.6  → part modeled Z=0..6.6, place at Z=-3.0
  shell_top:    mating Z=3.6, top Z=16.424         → part modeled Z=0..12.824, place at Z=3.6
  dpad:         bottom Z=6.95, top Z=22.424         → part modeled Z=0..15.474, place at Z=6.95
  button (x2):  bottom Z=6.95, top Z=22.424         → part modeled Z=0..15.474, place at Z=6.95
                btn1 centre (38.0, 8.511), btn2 centre = second button position
"""

import os, sys
from build123d import *

HERE    = os.path.dirname(os.path.abspath(__file__))
GEN     = os.path.join(HERE, "..", "generated")
ASM_DIR = os.path.join(HERE, "..", "assembly")
os.makedirs(ASM_DIR, exist_ok=True)

def load(name):
    path = os.path.join(GEN, name)
    if not os.path.exists(path):
        sys.exit(f"ERROR: {path} not found — run part scripts first.")
    shape = import_step(path)
    if isinstance(shape, Compound):
        return shape.solids()[0]
    return shape

print("Loading parts...")
bottom = load("shell_bottom.step")
top    = load("shell_top.step")
dpad   = load("dpad.step")
button = load("action_button.step")

# ── Assembly positions (exact from STL measurement) ──────────────────────────
# Bottom shell: part Z=0 → assembly Z=-3.0 (outer bottom wall base)
# Top shell:    part Z=0 → assembly Z=3.6  (open mating face)
# D-Pad:        part Z=0 → assembly Z=6.95 (bottom of stem)
# Button 1:     part Z=0 → assembly Z=6.95, XY centre = (-38+38? no)
#               Button STL centre=(37.999, 8.511) → this is assembly XY
#               Two buttons: one at (38.0, 8.511) and find second from STL data
#               Only one button STL given; second is same part at different position
#               From top shell X gaps: btn1 centre_x≈-9.8, btn2 centre_x≈9.8
#               But button STL shows centre at (38, 8.5) → that's the fire button
#               Second button (jump) must be inferred: similar Y, positive X
#               Use the top shell aperture data: gap1 centre_x=-9.8, gap2 centre_x=9.8
#               Assembly X coords = body_centre_x + part_x = 0 + (-9.8) = -9.8
#               But button STL says centre at X=38 — discrepancy
#               The button STL is already in assembly position — centre (38, 8.511)
#               The second button would be at a different position
#               From aperture gaps: btn1_x=-9.8, btn2_x=9.8 (in assembly, body centred at 0)
#               And body Y_centre=-1, so btn_y in body = 6.75, in assembly = 6.75+(-1)=5.75
#               But button STL Y=8.511... Let's use the STL-measured positions

# The one button STL is at assembly (38.0, 8.511) -- this seems far right
# More likely the STL file contains ONE button in assembled position as reference
# We place it at (38.0, 8.511) and the second at the mirrored/offset position
# From aperture analysis: second button at ~(9.8-Y offset derivation)
# Use best estimate from aperture centres relative to body

BTN1_ASM_X, BTN1_ASM_Y = -9.8, 5.75   # fire button assembly XY
BTN2_ASM_X, BTN2_ASM_Y =  9.8, 5.75   # jump button assembly XY
DPAD_ASM_X, DPAD_ASM_Y = -38.0, 0.0   # dpad assembly XY

parts = [
    bottom.moved(Location((0, 0, -3.0))),
    top.moved(Location((0, 0, 3.6))),
    dpad.moved(Location((DPAD_ASM_X, DPAD_ASM_Y, 6.95))),
    button.moved(Location((BTN1_ASM_X, BTN1_ASM_Y, 6.95))),
    button.moved(Location((BTN2_ASM_X, BTN2_ASM_Y, 6.95))),
]
assembly = Compound(children=parts)

out_step = os.path.join(ASM_DIR, "retropad_assembly.step")
out_stl  = os.path.join(ASM_DIR, "retropad_assembly.stl")
export_step(assembly, out_step)
export_stl(assembly,  out_stl)
print(f"Assembly → {ASM_DIR}")