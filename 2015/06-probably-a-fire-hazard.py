# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 06 - Probably A Fire Hazard
# Problem: See .\2015\06-probably-a-fire-hazard-description.md for full details
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

INPUT_FILE = os.path.join('data', '2015-06.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False
GRID_DIM = 1000

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 06/2015 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> list[tuple[str, tuple[int, int], tuple[int, int]]]:
    data: list[tuple[str, tuple[int, int], tuple[int, int]]] = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip().split()
            
            command = ' '.join(line[0: -3])
            start = tuple(map(int, line[-3].split(',')))
            end = tuple(map(int, line[-1].split(',')))
            data.append((command, start, end))
    return data

# --- SOLVE ---
def solve_part1(instructions: list[tuple[str, tuple[int, int], tuple[int, int]]]) -> int:
    """Solution for Part 1."""
    def translate_command(command: str):
        if command == 'turn on':
            operation: function = lambda light: 1
        elif command == 'turn off':
            operation: function = lambda light: 0
        elif command == 'toggle':
            operation: function = lambda light: (light + 1) % 2
        return operation
    
    grid: list[list[int]] = [[0]*GRID_DIM for _ in range(GRID_DIM)]
    for command, start, end in instructions:
        operation = translate_command(command)
        for r in range(start[0], end[0] + 1): # end is included
            for c in range(start[1], end[1] + 1):
                grid[r][c] = operation(grid[r][c])

    return sum([sum(row) for row in grid])

def solve_part2(instructions: list[tuple[str, tuple[int, int], tuple[int, int]]]) -> int:
    """Solution for Part 2."""
    def translate_command(command: str):
        if command == 'turn on':
            operation: function = lambda light: light + 1
        elif command == 'turn off':
            operation: function = lambda light: max(light - 1, 0)
        elif command == 'toggle':
            operation: function = lambda light: light + 2
        return operation
    
    grid: list[list[int]] = [[0]*GRID_DIM for _ in range(GRID_DIM)]
    for command, start, end in instructions:
        operation = translate_command(command)
        for r in range(start[0], end[0] + 1): # end is included
            for c in range(start[1], end[1] + 1):
                grid[r][c] = operation(grid[r][c])

    return sum([sum(row) for row in grid])

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
