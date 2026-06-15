# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 07 - Internet Protocol Version 7
# Problem: See ./2016/07-internet-protocol-version-7-description.md for full details
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

INPUT_FILE = os.path.join('data', '2016-07.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 07/2016 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name) -> list[dict[str, list[str]]]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            splitted_line = line.strip().replace('[', ']').split(']')
            data.append({
                'original': line.strip(),
                'normal': splitted_line[::2],
                'hypernet': splitted_line[1::2]
            })
    return data

# --- SOLVE ---
def is_abba(address: dict[str, list[str]]):
    def check_abba_on_string(s: str): 
        for i in range(0, len(s)-3):
            sub = s[i:i+4]
            if len(set(sub)) != 2: continue
            if sub[:2] == sub[2:][::-1]: return True
        return False
    
    return any(list(map(lambda s: check_abba_on_string(s), address['normal']))) and (not any(list(map(lambda s: check_abba_on_string(s), address['hypernet']))))

def is_aba(address: dict[str, list[str]]):
    def get_aba_candidate(s: str):
        candidate = []
        for i in range(0, len(s)-2):
            sub = s[i:i+3]
            if len(set(sub)) != 2: continue
            if sub[0] == sub[-1]: candidate.append(sub)
        return candidate
    
    def convert_aba_to_bab(candidate_aba: list[str]):
        converted = []
        for s in candidate_aba:
            converted.append(f"{s[1]}{s[0]}{s[1]}")
        return converted
    
    def check_bab(s: str, candidate_bab: list[str]):
        for bab in candidate_bab:
            if bab in s: return True
        return False

    all_candidates = []
    for normal in address['normal']:
        all_candidates += get_aba_candidate(normal)
    if len(all_candidates) == 0: return False # Not possible ABA strings to start with
    
    converted_bab = convert_aba_to_bab(all_candidates)
    return any(list(map(lambda s: check_bab(s, converted_bab), address['hypernet'])))

def solve_part1(data: list[dict[str, list[str]]]):
    """Solution for Part 1."""
    return len(list(filter(lambda d: is_abba(d), data)))

def solve_part2(data: list[dict[str, list[str]]]):
    """Solution for Part 2."""
    return len(list(filter(lambda d: is_aba(d), data)))

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
