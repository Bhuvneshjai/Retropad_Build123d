"""
RetroPad Assembly - build123d script
Run all 4 part scripts first, then run this.
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
        sys.exit(f"ERROR: {path} not found - run the part scripts first.")
    shape = import_step(path)
    if isinstance(shape, Compound):
        return shape.solids()[0]
    return shape

print("Loading parts...")
bottom = load("shell_bottom.step")
top    = load("shell_top.step")
dpad   = load("dpad.step")
button = load("action_button.step")

H_BOT     =  8.0
FLOOR_TOP =  2.0
BTN_Z     = H_BOT + FLOOR_TOP

parts = [
    bottom.moved(Location((0, 0, 0))),
    top.moved(Location((0, 0, H_BOT))),
    dpad.moved(Location((-42.0, 0.0, BTN_Z))),
    button.moved(Location((42.0, -6.0, BTN_Z))),
    button.moved(Location((54.0,  6.0, BTN_Z))),
]
assembly = Compound(children=parts)

out_step = os.path.join(ASM_DIR, "retropad_assembly.step")
out_stl  = os.path.join(ASM_DIR, "retropad_assembly.stl")
export_step(assembly, out_step)
export_stl(assembly,  out_stl)
print(f"Assembly exported to {ASM_DIR}")