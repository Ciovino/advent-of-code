# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 17 - Two Steps Forward
# Problem: See ./2016/17-two-steps-forward-description.md for full details
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
from hashlib import md5

INPUT_FILE = os.path.join('data', '2016-17.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

DIRECTIONS = (('U', 0, -1), ('D', 0, 1), ('L', -1, 0), ('R', 1, 0))
OPEN_DOORS = set("bcdef")

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 17/2016 Advent of Code.")
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
def get_open_doors(path: str):
    hash_val = md5(path.encode()).hexdigest()
    for i, (char, dx, dy) in enumerate(DIRECTIONS):
        if hash_val[i] in OPEN_DOORS:
            yield char, dx, dy

def solve_part1(passcode: str) -> str:
    """Solution for Part 1."""
    queue = deque([((0, 0), passcode)])
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == (3, 3):
            return path[len(passcode):]
            
        for char, dx, dy in get_open_doors(path):
            nx, ny = x + dx, y + dy
            if 0 <= nx <= 3 and 0 <= ny <= 3:
                queue.append(((nx, ny), path + char))
                
    return "nothing"

def solve_part2(passcode: str) -> int:
    """Solution for Part 2."""
    queue = deque([((0, 0), passcode)])
    max_path = 0
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == (3, 3):
            max_path = max(max_path, len(path) - len(passcode))
            continue
            
        for char, dx, dy in get_open_doors(path):
            nx, ny = x + dx, y + dy
            if 0 <= nx <= 3 and 0 <= ny <= 3:
                queue.append(((nx, ny), path + char))
                
    return max_path

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
