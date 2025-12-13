# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 11 - Reactor
# Problem: See .\2025\11-reactor-description.md for full details
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

INPUT_FILE = os.path.join('data', '2025-11.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 11/2025 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> dict[str, list[str]]:
    data: dict[str, list[str]] = {}
    with open(file_name, 'r') as f:
        for line in f:
            connection = line.strip().split(':')
            start, end = connection[0], connection[1].split()
            data[start] = end
    return data

# --- SOLVE ---
def get_paths(start: str, end:str, connections: dict[str, list[str]], required: set[str] = set()) -> int:
    def run_all_path(position: str, required_found: int, cache: dict[tuple[str, int], int]) -> int:
        nonlocal end, required
        if position == end: # Reached the target position
            return int(required_found >= len(required))

        # How many path lead to "end" from "position"
        total_paths = 0
        for out in connections[position]:
            if out in required:
                required_found += 1
            
            if (out, required_found) in cache:
                out_result = cache[(out, required_found)]
            else:
                out_result = run_all_path(out, required_found, cache)
                cache[(out, required_found)] = out_result
            
            total_paths += out_result
            if out in required:
                required_found -= 1
        return total_paths

    return run_all_path(start, 0, {})

def solve_part1(connections: dict[str, list[str]]) -> int:
    """Solution for Part 1."""
    return get_paths("you", "out", connections)

def solve_part2(connections: dict[str, list[str]]) -> int:
    """Solution for Part 2."""
    return get_paths("svr", "out", connections, required={"dac", "fft"})

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
