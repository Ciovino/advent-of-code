# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 03 - Perfectly Spherical Houses In A Vacuum
# Problem: See .\2015/03-perfectly-spherical-houses-in-a-vacuum-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# Parse the input
with open(os.path.join('data', '2015-03.in'), 'r') as f:
    moves: list[str] = list(f.readline().strip())

# --- SOLVE ---
def convert_move_to_tuple(move: str) -> tuple[int, int]:
    # Using standard (x, y)
    if move == '>': # Right
        return (1, 0)
    elif move == '<': # Left
        return (-1, 0)
    elif move == '^': # Up
        return (0, 1)
    elif move == 'v': # Down
        return (0, -1)
    else:
        raise ValueError(f"Unknown move: {move}")

single: tuple[int, int] = (0, 0)
double: dict[int, tuple[int, int]] = {
    0: (0, 0),
    1: (0, 0),
}
unique_houses: dict[str, set[tuple[int, int]]] = {
    'single': {(0, 0)},
    'double': {(0, 0)},
}
for i, move in enumerate(moves):
    movement = convert_move_to_tuple(move)
    # Update position
    # Single (only Santa)
    single = (single[0] + movement[0], single[1] + movement[1])
    # Double (Santa + Robo-Santa)
    turn = i % 2
    double[turn] = (double[turn][0] + movement[0], double[turn][1] + movement[1])
    
    # Add to set. Will be ignored if already present
    unique_houses['single'].add(single)
    unique_houses['double'].add(double[turn])

# --- PRINT ---
print(f"AOC_SOL_1={len(unique_houses['single'])}")
print(f"AOC_SOL_2={len(unique_houses['double'])}")
