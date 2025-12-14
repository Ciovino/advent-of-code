# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 01 - No Time For A Taxicab
# Problem: See ./2016/01-no-time-for-a-taxicab-description.md for full details
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

INPUT_FILE = os.path.join('data', '2016-01.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False
DIRECTIONS: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)] # North, East, South, West

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 01/2016 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name) -> list[tuple[str, int]]:
    with open(file_name, 'r') as f:
        data: list[tuple[str, int]] = list(map(lambda x: (x[0], int(x[1:])), f.readline().strip().split(', ')))
    return data

# --- SOLVE ---
def change_direction(current: int, new_direction: str) -> int:    
    global DIRECTIONS
    if new_direction == 'R': move = 1
    elif new_direction == 'L': move = -1
    else: raise ValueError(f"Unknown move: {new_direction}")
    return (current + move) % len(DIRECTIONS)

def solve_part1(moves: list[tuple[str, int]]) -> int:
    """Solution for Part 1."""
    global DIRECTIONS
    
    position: tuple[int, int] = (0, 0)
    current_direction: int = 0 # North
    for new_direction, steps in moves:
        current_direction = change_direction(current_direction, new_direction)
        position = (position[0] + DIRECTIONS[current_direction][0]*steps, position[1] + DIRECTIONS[current_direction][1]*steps)
    return sum(abs(p) for p in position)

def solve_part2(moves: list[tuple[str, int]]) -> int:
    """Solution for Part 2."""
    global DIRECTIONS
    
    position: tuple[int, int] = (0, 0)
    visited_position: set[tuple[int, int]] = {(0, 0)}
    visited_twice: tuple[int, int] = None
    current_direction: int = 0 # North
    for new_direction, steps in moves:
        if visited_twice: break
        current_direction = change_direction(current_direction, new_direction)
        for _ in range(steps):
            position = (position[0] + DIRECTIONS[current_direction][0], position[1] + DIRECTIONS[current_direction][1])
            if position in visited_position:
                visited_twice = position
                break
            else:
                visited_position.add(position)
    return sum(abs(p) for p in visited_twice)

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
