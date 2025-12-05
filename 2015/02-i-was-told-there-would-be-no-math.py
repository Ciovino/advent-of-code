# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 02 - I Was Told There Would Be No Math
# Problem: See .\2015\02-i-was-told-there-would-be-no-math-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# Parse the input
presents: list[int] = [] # present format: length x width x height
with open(os.path.join('data', '2015-02.in'), 'r') as f:
    for line in f:
        presents.append(tuple(map(int, line.strip().split('x'))))

# --- SOLVE ---
def amount_paper(length: int, width: int, height: int) -> int:
    # A box as 6 total faces. Opposite sides are equals
    area_faces: tuple[int, int, int] = (
        length * width, 
        width * height, 
        height * length
    )
    
    # Total area is double the sum of the area of the faces
    total_area: int = 2 * sum(area_faces)

    # Total amount of wrapping paper is then the area plus and extra
    #   equal to the minimum area between the faces
    return total_area + min(area_faces)

def amount_ribbon(length: int, width: int, height: int) -> int:
    perimeter_faces: tuple[int, int, int] = (
        2*(length + width),
        2*(width + height),
        2*(height + length)
    )
    
    # Base for the ribbon is the minimun perimeter
    ribbon_base: int = min(perimeter_faces)
    
    # For the bow we compute the cubic volume
    bow: int = length * width * height
    
    return ribbon_base + bow

# Map each present to the amount of wrapping paper needed
wrapping_paper_per_present: list[int] = list(map(lambda present: amount_paper(*present), presents))
ribbon_per_present: list[int] = list(map(lambda present: amount_ribbon(*present), presents))

# --- PRINT ---
print(f"AOC_SOL_1={sum(wrapping_paper_per_present)}")
print(f"AOC_SOL_2={sum(ribbon_per_present)}")
