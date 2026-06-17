# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 15 - Timing Is Everything
# Problem: See ./2016/15-timing-is-everything-description.md for full details
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
from copy import deepcopy

INPUT_FILE = os.path.join('data', '2016-15.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 15/2016 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name):
    data: list[list[int, int]] = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            numbers = find_numbers(line)

            data.append([numbers[1], numbers[3]])
    return data

# --- SOLVE ---
def solve_part1(disks: list[list[int, int]]) -> int:
    """Solution for Part 1."""
    time = 0
    step = 1
    
    for i, (positions, start_pos) in enumerate(disks, start=1):
        disk_offset = i
        
        # Keep stepping forward until the current disk aligns
        while (time + start_pos + disk_offset) % positions != 0:
            time += step
            
        # Once aligned, multiply the step size by this disk's positions
        step *= positions
        
    return time

def solve_part2(disks: list[list[int, int]]) -> int:
    """Solution for Part 2."""
    disks.append([11, 0])
    
    time = 0
    step = 1
    
    for i, (positions, start_pos) in enumerate(disks, start=1):
        disk_offset = i
        
        while (time + start_pos + disk_offset) % positions != 0:
            time += step
            
        step *= positions
        
    return time

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
