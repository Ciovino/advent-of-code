# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 12 - Jsabacusframework.Io
# Problem: See .\2015\12-jsabacusframework-io-description.md for full details
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
import json

INPUT_FILE = os.path.join('data', '2015-12.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 12/2015 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> dict:
    with open(file_name, 'r') as f:
        data: dict = json.loads(f.readline())
    return data

# --- SOLVE ---
def explore_json(json_content: dict | list | int | str, double_count: bool=False) -> int:
    if isinstance(json_content, dict):
        if double_count and "red" in json_content.values():
            return 0
        iterator = iter(json_content.values())
    elif isinstance(json_content, list):
        iterator = iter(json_content)
    elif isinstance(json_content, (int, str)):
        try:
            return int(json_content)
        except:
            return 0    
    return sum([explore_json(element, double_count=double_count) for element in iterator])

def solve_part1(json_content: dict) -> int:
    """Solution for Part 1."""
    return explore_json(json_content)

def solve_part2(json_content: dict) -> int:
    """Solution for Part 2."""
    return explore_json(json_content, double_count=True)

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
