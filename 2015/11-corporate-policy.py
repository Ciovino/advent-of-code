# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 11 - Corporate Policy
# Problem: See .\2015/11-corporate-policy-description.md for full details
# Author: Ciovino
# Template Version: v1.0
# ---------------------------------------------------------------------
import os
import os
import argparse
import time

# Useful imports
import re
from collections import defaultdict, Counter, deque
from itertools import combinations, permutations, product
from math import gcd, lcm, ceil, floor
from string import ascii_lowercase

INPUT_FILE = os.path.join('data', '2015-11.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False
PART1_SOLUTION = None
CHAR_LIMIT = (ord('a'), ord('z'))

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 11/2015 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> str:
    with open(file_name, 'r') as f:
        data: str = f.readline().strip()
    return data

# --- SOLVE ---
def check_password(password: list[int]) -> bool:
    # One increasing sequence of at least 3 element
    triple_increasing_sequence: bool = False
    for i in range(0, len(password) - 2):
        if password[i+2] - password[i+1] == 1 and password[i+1] - password[i] == 1:
            triple_increasing_sequence = True
            break
    if not triple_increasing_sequence:
        return False
    
    # Must not contains ['i', 'o', 'l']
    confusing_letters = list(map(ord, ['i', 'o', 'l']))
    if any([l in password for l in confusing_letters]):
        return False
    
    # Two different non-overlapping pair of letters, eg. 'aa' or 'bb'
    non_overlapping_double_sequence = 0
    password_str: str = ''.join(list(map(chr, password)))
    for i in ascii_lowercase:
        non_overlapping_double_sequence += password_str.find(f'{i}{i}') != -1
    
    if non_overlapping_double_sequence < 2:
        return False

    # All check passed
    return True
    
def increment_password(password: list[int], position: int | None = None):
    if position == None:
        position = len(password)-1    
    if position < 0:
        return
    
    password[position] += 1
    if password[position] > CHAR_LIMIT[1]:
        password[position] = CHAR_LIMIT[0]
        increment_password(password, position=position-1)

def get_next_password(old_password: str) -> str:
    # Convert password into a list of integer using the ascii code for better handling
    password: list[int] = list(map(ord, list(old_password)))
    
    increment_password(password)
    while not check_password(password):
        increment_password(password)
    
    return ''.join(list(map(chr, password)))

def solve_part1(password: str) -> str:
    """Solution for Part 1."""
    global PART1_SOLUTION
    PART1_SOLUTION = get_next_password(password)
    return PART1_SOLUTION

def solve_part2(password: str) -> str:
    """Solution for Part 2."""
    global PART1_SOLUTION
    return get_next_password(PART1_SOLUTION)

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
