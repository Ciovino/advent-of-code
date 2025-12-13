# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 04 - Printing Department
# Problem: See .\2025\04-printing-department-description.md for full details
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

INPUT_FILE = os.path.join('data', '2025-04.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 04/2025 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> list[list[str]]:
    data: list[list[str]] = []
    with open(file_name, 'r') as f:
        for line in f:
            data.append(list(line.strip()))
    return data

# --- SOLVE ---
def can_be_accessed(paper_rolls: list[list[str]], r: int, c: int) -> bool:
    neighbors_paper_rolls = 0
    for i in [-1, 0, 1]: # [Previous, Same, Next] Row
        row_index = r + i
        if row_index < 0 or row_index >= len(paper_rolls):
            continue
        
        for j in [-1, 0, 1]: # [Previous, Same, Next] Column
            col_index = c + j
            if col_index < 0 or col_index >= len(paper_rolls[0]):
                continue
            if row_index == r and col_index == c:
                continue
            
            if paper_rolls[row_index][col_index] == '@':
                neighbors_paper_rolls += 1
    
    return neighbors_paper_rolls < 4 # Remove if it has less than 4 roll neighbors

def solve_part1(paper_rolls: list[list[str]]) -> int:
    """Solution for Part 1."""
    ROWS, COLUMNS = len(paper_rolls), len(paper_rolls[0])
    
    removed: int = 0
    for r in range(ROWS):
        for c in range(COLUMNS):
            if paper_rolls[r][c] == '@':
                removed += can_be_accessed(paper_rolls, r, c)

    return removed

def solve_part2(paper_rolls: list[list[str]]) -> int:
    """Solution for Part 2."""
    ROWS, COLUMNS = len(paper_rolls), len(paper_rolls[0])
    
    removed: int = 0
    while True:
        to_be_removed: list[tuple[int]] = [] # Coords of rolls to remove at the end
        for r in range(ROWS):
            for c in range(COLUMNS):
                if paper_rolls[r][c] == '@' and can_be_accessed(paper_rolls, r, c):
                    removed += 1
                    to_be_removed.append((r, c))
        
        if len(to_be_removed) == 0:
            break
        
        for r, c in to_be_removed:
            paper_rolls[r][c] = '.'

    return removed

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
