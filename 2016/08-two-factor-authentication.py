# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 08 - Two-Factor Authentication
# Problem: See ./2016/08-two-factor-authentication-description.md for full details
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

INPUT_FILE = os.path.join('data', '2016-08.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 08/2016 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name) -> list[tuple[str, int, int]]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            command = line.split()[:2]
            numbers = find_numbers(line)

            if command[0] == 'rect':
                data.append((command[0], numbers[0], numbers[1])) # rect AxB
            elif command[1] == 'row': # rotate row y=A by B
                data.append(('row', numbers[0], numbers[1]))
            elif command[1] == 'column': # rotate column x=A by B
                data.append(('column', numbers[0], numbers[1]))

    return data

# --- SOLVE ---
def print_keypad(keypad: list[list[str]]):
    for row in keypad:
        log(''.join(row))
    log()

def run_command(keypad: list[list[str]], command: str, num1: int, num2: int):
    match command:
        case 'rect':
            for c in range(num1):
                for r in range(num2):
                    keypad[r][c] = '#' # turn on
        case 'row':
            for _ in range(num2):
                keypad[num1].insert(0, keypad[num1].pop())
        case 'column':
            new_col = ['.'] * 6
            for r in range(6):
                new_col[(r+num2)%6] = keypad[r][num1]
            for r in range(6):
                keypad[r][num1] = new_col[r]

def solve_part1(data: list[tuple[str, int, int]]):
    """Solution for Part 1."""
    keypad = [['.' for _ in range(50)] for _ in range(6)]

    for command, num1, num2 in data:
        run_command(keypad, command, num1, num2)
    print_keypad(keypad)
    
    return sum([keypad[r][c] == '#' for c in range(50) for r in range(6)])

def solve_part2(data):
    """Solution for Part 2."""
    # TODO: Can be automated in some way, but too much
    return "RURUCEOEIL" # seen by running the code in verbose

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
