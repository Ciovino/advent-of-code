# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 05 - Cafeteria
# Problem: See .\2025/05-cafeteria-description.md for full details
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

INPUT_FILE = os.path.join('data', '2025-05.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 05/2025 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> tuple[list[tuple[int, int]], list[int]]:
    fresh_ingredient_ids: list[tuple[int, int]] = []
    ingredients: list[int] = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            if line.find('-') != -1: # Ranges
                fresh_ingredient_ids.append(tuple(map(int, line.split('-'))))
            else: # Ingredients
                ingredients.append(int(line))
    return compact_list(fresh_ingredient_ids), ingredients

def compact_list(tuple_list: list[tuple[int, int]]) -> list[tuple[int, int]]:
    tuple_list.sort(key=lambda range_: range_[0])
    
    compact_list: list[tuple[int, int]] = []
    current_range = (-1, -1)
    for range_ in tuple_list:
        if current_range == (-1, -1): # Initialization
            current_range = range_
            continue
        
        if current_range[1] < range_[0]:
            # No overlap. Save the current range and update it
            compact_list.append(current_range)
            current_range = range_
        else:
            # Overlap. Compact ranges
            current_range = (current_range[0], max(current_range[1], range_[1]))
    # Append last element
    compact_list.append(current_range)
    return compact_list.copy()

# --- SOLVE ---
def solve_part1(data: tuple[list[tuple[int, int]], list[int]]) -> int:
    """Solution for Part 1."""
    fresh_ingredient_ids, ingredients = data # Unpack
    def is_fresh(ingredient: int) -> bool:
        nonlocal fresh_ingredient_ids
        
        for range_ in fresh_ingredient_ids:
            if range_[1] < ingredient: continue # Skip
            if range_[0] > ingredient: return False
            if range_[0] < ingredient < range_[1]: return True
        return False # Fallback
    
    return len(list(filter(is_fresh, ingredients)))

def solve_part2(data):
    """Solution for Part 2."""
    fresh_ingredient_ids, _ = data # Unpack
    return sum(list(map(lambda range_: range_[1] - range_[0] + 1, fresh_ingredient_ids)))

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
