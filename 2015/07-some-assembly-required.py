# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 07 - Some Assembly Required
# Problem: See .\2015\07-some-assembly-required-description.md for full details
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

INPUT_FILE = os.path.join('data', '2015-07.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False
N_BITS = 16
MASK = (1 << N_BITS) - 1
PART1_SOLUTION = None

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 07/2015 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> dict[str, str]:
    data: dict[str, str] = {}
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip().split('->') # (operation) -> output
            operation, wire = line[0].strip(), line[-1].strip()
            data[wire] = operation
    return data

# --- SOLVE ---
def compute(wire: str, circuit: dict[str, str], cache: dict[str, int]) -> int:
    # Base Case: Raw number, return it
    if wire.isdigit():
        return int(wire)
    
    if wire in cache:
        return cache[wire]

    # Get the operation from the circuit
    operation = circuit.get(wire)
    arguments = operation.split()
    result = 0

    # Perform Logic
    if len(arguments) == 1:
        # Assignment
        result = compute(arguments[0], circuit, cache)
    elif len(arguments) == 2:
        # NOT operation
        result = (~compute(arguments[1], circuit, cache)) & MASK
    elif len(arguments) == 3:
        left = compute(arguments[0], circuit, cache)
        right = compute(arguments[2], circuit, cache)
        op = arguments[1]
        
        if op == "AND":
            result = (left & right) & MASK
        elif op == "OR":
            result = (left | right) & MASK
        elif op == "LSHIFT":
            result = (left << right) & MASK
        elif op == "RSHIFT":
            result = (left >> right) & MASK
    
    cache[wire] = result
    return result

def solve_part1(circuit: dict[str, str]) -> int:
    """Solution for Part 1."""
    global PART1_SOLUTION
    PART1_SOLUTION = compute('a', circuit, {})
    return PART1_SOLUTION

def solve_part2(circuit: dict[str, str]) -> int:
    """Solution for Part 2."""
    global PART1_SOLUTION
    circuit['b'] = str(PART1_SOLUTION)
    return compute('a', circuit, {})

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
