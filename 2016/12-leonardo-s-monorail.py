# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 12 - Leonardo'S Monorail
# Problem: See ./2016/12-leonardo-s-monorail-description.md for full details
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

INPUT_FILE = os.path.join('data', '2016-12.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 12/2016 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name):
    data: list[str] = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            data.append(line)
    return data

# --- SOLVE ---
def run_program(vm: dict[str, int], program: list[str]):
    while vm['ip'] < len(program):
        istruction = program[vm['ip']].split()
        log(program[vm['ip']], vm)
        command, parameters = istruction[0], istruction[1:]

        match command:
            case "cpy":
                source, destination = parameters[0], parameters[1]
                try:
                    source = int(source)
                    vm[destination] = source
                except:
                    vm[destination] = vm[source]
            
            case "inc":
                vm[parameters[0]] += 1
            
            case "dec":
                vm[parameters[0]] -= 1
            
            case "jnz":
                check, offset = parameters[0], parameters[1]

                try:
                    check = int(check)
                except:
                    check = vm[check]

                if check != 0:
                    vm['ip'] += int(offset)
                    continue
        
        vm['ip'] += 1 # Next istruction
    
    return vm

def solve_part1(program: list[str]):
    """Solution for Part 1."""
    log(program)

    vm = {
        'a': 0,
        'b': 0,
        'c': 0,
        'd': 0,
        'ip': 0 # Istruction pointer
    }

    vm = run_program(vm, program)
    return vm['a']

def solve_part2(program: list[str]):
    """Solution for Part 2."""
    log(program)

    vm = {
        'a': 0,
        'b': 0,
        'c': 1,
        'd': 0,
        'ip': 0 # Istruction pointer
    }

    vm = run_program(vm, program)
    return vm['a']

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
