# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 01 - Not Quite Lisp
# Problem: See .\2015\01-not-quite-lisp-description.md for full details
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

INPUT_FILE = os.path.join('data', '2015-01.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 01/2015 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> list[str]:
    with open(file_name, 'r') as f:
        data: list[str] = list(f.readline().strip())
    return data

def map_step(step: str) -> int:
    """ Convert a step into the appropriate number. """
    if step == '(':
        return 1
    elif step == ')':
        return -1
    else:
        raise ValueError(f"Unknown step {step}.")

def solve_part1(floor_plan: list[str]) -> int:
    """Solution for Part 1."""
    return sum(list(map(map_step, floor_plan)))

def solve_part2(floor_plan: list[str]) -> int:
    """Solution for Part 2."""
    steps: list[int] = list(map(map_step, floor_plan))
    total = 0
    for i, step in enumerate(steps, start=1):
        total += step
        if total < 0:
            return i
    return len(steps)

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
