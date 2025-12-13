# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 03 - Lobby
# Problem: See .\2025\03-lobby-description.md for full details
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

INPUT_FILE = os.path.join('data', '2025-03.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 03/2025 Advent of Code.")
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
def compute_max_joltage(bank: list[str], N: int) -> int:
    if N > len(bank):
        raise ValueError(f"Can't compute joltage with {N} batteries from a bank with {len(bank)} batteries. Battery bank: {bank}")
    
    max_joltage = ''
    start_position = 0
    
    for i in range(N):
        end_position = -N + i + 1
        if end_position != 0:
            bank_current_section = bank[start_position:(-N+i+1)]
        else:
            bank_current_section = bank[start_position:]
        chosen_battery = max(bank_current_section)
        start_position += 1 + bank_current_section.index(chosen_battery)
        max_joltage += chosen_battery
    return int(max_joltage)

def solve_part1(battery_banks: list[list[str]]) -> int:
    """Solution for Part 1."""
    return sum(list(map(lambda bank: compute_max_joltage(bank, 2), battery_banks)))

def solve_part2(battery_banks: list[list[str]]) -> int:
    """Solution for Part 2."""
    return sum(list(map(lambda bank: compute_max_joltage(bank, 12), battery_banks)))

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
