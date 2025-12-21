# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 02 - Bathroom Security
# Problem: See ./2016/02-bathroom-security-description.md for full details
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

INPUT_FILE = os.path.join('data', '2016-02.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 02/2016 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name) -> list[list[str]]:
    with open(file_name, 'r') as f:
        data: list[list[str]] = [list(line.strip()) for line in f]
    return data

# --- SOLVE ---
def apply_move(keypad: set[tuple[int, int]], move: str, current_position = tuple[int, int]) -> tuple[int, int]:
    match move:
        case 'R':
            new_position = (current_position[0], current_position[1] + 1)
        case 'L':
            new_position = (current_position[0], current_position[1] - 1)
        case 'U':
            new_position = (current_position[0] - 1, current_position[1])
        case 'D':
            new_position = (current_position[0] + 1, current_position[1])
        case _:
            raise ValueError(f"Unknown move {move}")
    
    return new_position if new_position in keypad else current_position

def get_password(keypad: dict[tuple[int, int], str], all_istructions: list[list[str]], starting_position: tuple[int, int]) -> str:
    keypad_positions = set(keypad.keys())
    password = ''
    current_position = starting_position
    
    for istructions in all_istructions:
        for move in istructions:
            current_position = apply_move(keypad_positions, move, current_position)
        password += keypad[current_position]
    
    return password

def solve_part1(all_istructions: list[list[str]]) -> str:
    """Solution for Part 1."""
    keypad = {
        (0, 0): '1', (0, 1): '2', (0, 2): '3',
        (1, 0): '4', (1, 1): '5', (1, 2): '6',
        (2, 0): '7', (2, 1): '8', (2, 2): '9',
    }
    return get_password(keypad, all_istructions, (1, 1)) # start on 5

def solve_part2(all_istructions: list[list[str]]) -> str:
    """Solution for Part 2."""
    keypad = {
        (0, 2): '1', 
        (1, 1): '2', (1, 2): '3', (1, 3): '4', 
        (2, 0): '5', (2, 1): '6', (2, 2): '7', (2, 3): '8', (2, 4): '9',
        (3, 1): 'A', (3, 2): 'B', (3, 3): 'C', 
        (4, 2): 'D',
    }
    return get_password(keypad, all_istructions, (2, 0)) # start on 5

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
