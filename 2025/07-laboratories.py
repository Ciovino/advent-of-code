# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 07 - Laboratories
# Problem: See .\2025/07-laboratories-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# Parse the input
with open(os.path.join('data', '2025-07.in'), 'r') as f:
    tachyon_manifold: list[list[str]] = list(map(lambda s: s.strip(), f.readlines()))

# --- SOLVE ---
# Locate beam source
def count_beam_split(beam_source: int, tachyon: list[list[str]]) -> tuple[int, dict[int, set[int]]]:
    total_splits = 0
    beam_positions: dict[int, set[int]] = { 0: {beam_source} }
    for i, line in enumerate(tachyon[1:], start=1): # Skip first line
        # Check if the beam will be splitted
        new_beam_positions: set[int] = set()
        for pos in beam_positions[i - 1]:
            if line[pos] == '^': # Split the beam -> Add one to the right and to the left
                new_beam_positions.add(pos - 1)
                new_beam_positions.add(pos + 1)
                # Add a split
                total_splits += 1
            elif line[pos] == '.': # Pass the beam down
                new_beam_positions.add(pos)
            else:
                raise ValueError(f"Unknown character at position ({i}, {pos}): {line[pos]}")
        # Add beam for next iterations
        beam_positions[i] = new_beam_positions
    return total_splits, beam_positions

def count_timeline_dp(all_beam_positions: dict[int, set[int]], tachyon: list[list[str]]) -> int:
    N: int = len(tachyon) # Number of rows
    dynamic_programming: dict[tuple[int, int], int] = {}
    
    # Initialize Dynamic Programming value from the bottom row
    last_row = N - 1
    for pos in all_beam_positions[last_row]:
        dynamic_programming[(last_row, pos)] = 1
    
    # Start from the N-2
    for row in range(N-2, 0, -1): # Avoid first row (the one with the 'S')
        for pos in all_beam_positions[row]:
            if tachyon[row + 1][pos] == '^': # Beam splitted
                dynamic_programming[(row, pos)] = dynamic_programming[(row+1, pos-1)] + dynamic_programming[(row+1, pos+1)]
            elif tachyon[row + 1][pos] == '.': # Straight beam
                dynamic_programming[(row, pos)] = dynamic_programming[(row+1, pos)]
            else:
                raise ValueError(f"Unknown character at position ({row}, {pos}): {tachyon[row][pos]}")
    
    starting_row = 1 # Get the total beam path from column 1
    starting_col = next(iter(all_beam_positions[starting_row]))
    return dynamic_programming[(starting_row, starting_col)]

split, beam_positions = count_beam_split(tachyon_manifold[0].find('S'), tachyon_manifold)
timelines_dp = count_timeline_dp(beam_positions, tachyon_manifold)

# --- PRINT ---
print(f"AOC_SOL_1={split}")
print(f"AOC_SOL_2={timelines_dp}")
