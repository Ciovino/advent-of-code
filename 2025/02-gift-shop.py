# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 02 - Gift shop
# Problem: See ./02-gift-shop-description.md for full details
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

INPUT_FILE = os.path.join('data', '2025-02.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 02/2025 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> list[str]:
    with open(file_name, 'r') as f:
        data = f.readline().strip()
    return data.split(',')

# --- SOLVE ---
def solve_part1(id_ranges: list[str]):
    """Solution for Part 1."""
    def double_sequence(id: int) -> int:
        id_str = str(id)
        if len(id_str) % 2 != 0:
            return False
        
        mid_point = len(id_str) // 2
        first_half, second_half = id_str[:mid_point], id_str[mid_point:]
        return id if first_half == second_half else 0
    
    invalid_ids: int = 0
    for id_range in id_ranges:
        first_id, last_id = tuple(map(int, id_range.split('-')))
        for id in range(first_id, last_id + 1):
            invalid_ids += double_sequence(id)

    return invalid_ids

def solve_part2(id_ranges: list[str]):
    """Solution for Part 2."""
    def repeated_sequence(id: int) -> int:
        id_str = str(id)
        len_id = len(id_str)
        
        for sequence_length in range(1, len_id//2 + 1):
            if len_id % sequence_length != 0: continue
            sequence = id_str[:sequence_length]
            if id_str.count(sequence) * sequence_length == len_id:
                return id
        return 0
    
    invalid_ids: int = 0
    for id_range in id_ranges:
        first_id, last_id = tuple(map(int, id_range.split('-')))
        for id in range(first_id, last_id + 1):
            invalid_ids += repeated_sequence(id)

    return invalid_ids

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
