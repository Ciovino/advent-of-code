# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 18 - Like A Rogue
# Problem: See ./2016/18-like-a-rogue-description.md for full details
# Author: Ciovino
# Template Version: v2.0
# ---------------------------------------------------------------------
import os
import argparse
import time

# Useful imports
import re
from collections import defaultdict, Counter, deque
from itertools import combinations, permutations, product
from math import gcd, lcm, ceil, floor

INPUT_FILE = os.path.join('data', '2016-18.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 18/2016 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name):
    with open(file_name, 'r') as f:
        data = f.read().strip()
    return data

# --- SOLVE ---
def count_safe_tiles(initial_row: str, total_rows: int) -> int:
    safe_tiles = initial_row.count('.')
    current = initial_row

    for _ in range(total_rows-1):
        padded = f".{current}."

        current = "".join(
            '^' if padded[i-1] != padded[i+1] else '.' 
            for i in range(1, len(padded) - 1)
        )
        safe_tiles += current.count('.')

    return safe_tiles

def solve_part1(tiles: str) -> int:
    """Solution for Part 1."""
    return count_safe_tiles(tiles, 40)

def solve_part2(tiles: str) -> int:
    """Solution for Part 2."""
    return count_safe_tiles(tiles, 400000)

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
