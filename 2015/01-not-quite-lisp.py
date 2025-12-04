# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 01 - Not Quite Lisp
# Problem: See .\2015\01-not-quite-lisp-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# Parse the input
with open(os.path.join('data', '2015-01.in'), 'r') as f:
    floor_plan: list[str] = list(f.readline().strip())

def map_step(step: str) -> int:
    """ Convert a step into the appropriate number. """
    if step == '(':
        return 1
    elif step == ')':
        return -1
    else:
        raise ValueError(f"Unknown step {step}.")

# Convert step into a list of numbers (+1; -1)
steps: list[int] = list(map(map_step, floor_plan))

running_total: int = 0
entering_basement: int = -1

for i, step in enumerate(steps):
    running_total += step
    if running_total < 0 and entering_basement < 0:
        # Break early
        entering_basement = i + 1
        break

# --- PRINT ---
print(f"AOC_SOL_1={sum(steps)}")
print(f"AOC_SOL_2={entering_basement}")
