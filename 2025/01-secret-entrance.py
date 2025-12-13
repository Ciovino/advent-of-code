# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 01 - Secret Entrance
# Problem: See ./01-secret-entrance-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
import argparse
import time

# Useful imports
import re
from collections import defaultdict, Counter, deque
from itertools import combinations, permutations, product
from math import gcd, lcm, ceil, floor

INPUT_FILE = os.path.join('data', '2025-01.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False
DIAL_START = 50
DIAL_DIM = 100

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 01/2025 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> list[tuple[str, int]]:
    moves: list[tuple[str, int]] = []
    with open(file_name, 'r') as f:
        for line in f:
            direction, distance = line[0], int(line[1:])
            moves.append((direction, distance))
    return moves

# --- SOLVE ---
def solve_part1(moves: list[tuple[str, int]]) -> int:
    """Solution for Part 1."""
    dial, land_on_zero = DIAL_START, 0
    
    for direction, distance in moves:
        step = 1 if direction == 'R' else -1
        dial = (dial + step * distance) % DIAL_DIM
        land_on_zero += dial == 0
    
    return land_on_zero

def solve_part2(moves: list[tuple[str, int]]) -> int:
    """Solution for Part 2."""
    dial, zero_clicks = DIAL_START, 0
    
    for direction, distance in moves:
        step = 1 if direction == 'R' else -1        
        
        for _ in range(distance):
            dial = (dial + step) % DIAL_DIM
            if dial == 0:
                zero_clicks += 1
    
    return zero_clicks

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
