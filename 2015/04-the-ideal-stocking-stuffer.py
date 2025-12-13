# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 04 - The Ideal Stocking Stuffer
# Problem: See .\2015\04-the-ideal-stocking-stuffer-description.md for full details
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
from hashlib import md5

INPUT_FILE = os.path.join('data', '2015-04.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 04/2015 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> str:
    with open(file_name, 'r') as f:
        data: str = f.readline().strip()
    return data

# --- SOLVE ---
def solve_part1(key: str) -> int:
    """Solution for Part 1."""
    suffix = 0
    while True:
        complete_key = key + str(suffix)
        md5_hash_hex: str = md5(complete_key.encode('utf-8')).hexdigest()
        if md5_hash_hex[:5] == '00000':
            log(f"Five 0s: Key: {complete_key} | MD5 Hash (hex): {md5_hash_hex}")
            return suffix
        suffix += 1

def solve_part2(key: str) -> int:
    """Solution for Part 2."""
    suffix = 0
    while True:
        complete_key = key + str(suffix)
        md5_hash_hex: str = md5(complete_key.encode('utf-8')).hexdigest()
        if md5_hash_hex[:6] == '000000':
            log(f"Six 0s: Key: {complete_key} | MD5 Hash (hex): {md5_hash_hex}")
            return suffix
        suffix += 1

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
