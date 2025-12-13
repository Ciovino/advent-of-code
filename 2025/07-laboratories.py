# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 07 - Laboratories
# Problem: See .\2025/07-laboratories-description.md for full details
# Author: Ciovino
# Template Version: v1.0
# ---------------------------------------------------------------------
import os
import argparse
import time

# Useful imports
import re
from collections import defaultdict, Counter, deque
from itertools import combinations, permutations, product
from math import gcd, lcm, ceil, floor

INPUT_FILE = os.path.join('data', '2025-07.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 07/2025 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> list[list[str]]:
    with open(file_name, 'r') as f:
        data: list[list[str]] = list(map(lambda s: s.strip(), f.readlines()))
    return data

# --- SOLVE ---
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

def solve_part1(tachyon_manifold: list[list[str]]) -> int:
    """Solution for Part 1."""
    split, _ = count_beam_split(tachyon_manifold[0].find('S'), tachyon_manifold)
    return split

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

def solve_part2(tachyon_manifold: list[list[str]]) -> int:
    """Solution for Part 2."""
    _, beam_positions = count_beam_split(tachyon_manifold[0].find('S'), tachyon_manifold)
    timelines_dp = count_timeline_dp(beam_positions, tachyon_manifold)
    return timelines_dp

if __name__ == '__main__':
    args = get_args()
    if args.test:
        if not os.path.exists(TEST_FILE):
            print(f"ERROR: Test file '{TEST_FILE}' not found.")
            exit(1)
        use_file = TEST_FILE
    else:
        use_file = INPUT_FILE
    VERBOSE = args.verbose
    
    # Parsing
    start_time = time.time()
    data = parse_input(use_file)
    log(f"Input parsed in {time.time()-start_time:.4f}s")
    
    # Part 1
    start_time = time.time()
    sol1 = solve_part1(data)
    log(f"Part 1: {sol1}, took {time.time()-start_time:.4f}s")
    
    # Part 2
    start_time = time.time()
    sol2 = solve_part2(data)
    log(f"Part 2: {sol2}, took {time.time()-start_time:.4f}s")

    # --- PRINT SOLUTIONS ---
    print(f"AOC_SOL_1={sol1}")
    print(f"AOC_SOL_2={sol2}")
