# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 05 - Doesn'T He Have Intern-Elves For This?
# Problem: See .\2015\05-doesn't-he-have-intern-elves-for-this-description.md for full details
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

INPUT_FILE = os.path.join('data', '2015-05.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 05/2015 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> list[str]:
    with open(file_name, 'r') as f:
        data: list[str] = list(map(lambda s: s.strip(), f.readlines()))
    return data

# Parse the input
with open(os.path.join('data', '2015-05.in'), 'r') as f:
    strings_to_check: list[str] = list(map(lambda s: s.strip(), f.readlines()))

# --- SOLVE ---
def three_vowels(S: str) -> bool:
    return sum([S.count(vowel) for vowel in 'aeiou']) >= 3

def double_letter(S: str) -> bool:
    for i in range(len(S) - 1):
        if S[i] == S[i+1]:
            return True
    return False

def avoid_naughty(S: str) -> bool:
    naughty = ['ab', 'cd', 'pq', 'xy']
    return max([S.find(n) for n in naughty]) < 0

def solve_part1(strings_to_check: list[str]) -> int:
    """Solution for Part 1."""
    return len(list(filter(lambda s: all([three_vowels(s), double_letter(s), avoid_naughty(s)]), strings_to_check)))

def double_substring(S: str) -> bool:
    for i in range(len(S) - 1):
        if S.count(S[i:i+2]) > 1:
            return True
    return False

def repeated_letter_with_step(S: str) -> bool:
    for i in range(len(S) - 2):
        if S[i] == S[i+2]:
            return True
    return False

def solve_part2(strings_to_check: list[str]) -> int:
    """Solution for Part 2."""
    return len(list(filter(lambda s: all([double_substring(s), repeated_letter_with_step(s)]), strings_to_check)))

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
