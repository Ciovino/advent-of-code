# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 09 - Explosives In Cyberspace
# Problem: See ./2016/09-explosives-in-cyberspace-description.md for full details
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

INPUT_FILE = os.path.join('data', '2016-09.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 09/2016 Advent of Code.")
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
def decompressed_len(data: str, depth = 1):
    if depth == 0: return len(data)

    idx, result = 0, 0
    while idx < len(data):
        if data[idx] != '(':
            result += 1
        else:
            repeat = ""
            while data[idx] != ')':
                repeat += data[idx]
                idx += 1
            # Also count ')'
            repeat += data[idx]
            idx += 1

            nums = find_numbers(repeat)
            substring = data[idx: idx+nums[0]]

            result += nums[1] * decompressed_len(substring, depth-1)
            idx += nums[0] - 1
        idx += 1
    return result

def solve_part1(data: str):
    """Solution for Part 1."""
    return decompressed_len(data)

def solve_part2(data: str):
    """Solution for Part 2."""
    return decompressed_len(data, depth=-1) # -1 run full decompression

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
