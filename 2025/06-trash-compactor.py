# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 06 - Trash Compactor
# Problem: See .\2025\06-trash-compactor-description.md for full details
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
from math import gcd, lcm, ceil, floor, prod

INPUT_FILE = os.path.join('data', '2025-06.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 06/2025 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> tuple[list[list[str]], list[str]]:
    number_lines: list[str] = []
    with open(file_name, 'r') as f:
        for line in f:
            if line.split()[0].isdigit():
                number_lines.append(line)
            else:
                symbols: list[str] = line.strip().split()
    return parse_numbers(number_lines), symbols

def parse_numbers(number_lines: list[str]) -> list[list[str]]:
    N = len(number_lines)    
    current_number: list[str] = [''] * N
    result_list: list[list[str]] = [[] for _ in range(N)]
    
    for digit in zip(*number_lines):
        if all([d in [' ', '\n'] for d in digit]): # Save current number
            for i in range(N):
                result_list[i].append(current_number[i])
                current_number[i] = ''
        else:
            for i in range(N):
                current_number[i] += digit[i]
    return result_list

# --- SOLVE ---
def solve_problem(input: tuple[str], problem_type: str):
    # Input are strings, convert them in int
    input: tuple[int] = tuple(map(int, input))
    
    if problem_type == '+':
        return sum(input)
    elif problem_type == '*':
        return prod(input)
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

def solve_cephalopod_problem(input: tuple[str], problem_type: str):
    # Zip by columns and join the strings
    new_input: tuple[str] = tuple(map(lambda t: ''.join(t), list(zip(*input))))
    return solve_problem(new_input, problem_type)

def solve_part1(data: tuple[list[list[str]], list[str]]):
    """Solution for Part 1."""
    numbers, symbols = data
    problem_input = list(zip(*numbers))
    return sum([solve_problem(input, problem) for input, problem in zip(problem_input, symbols)])

def solve_part2(data: tuple[list[list[str]], list[str]]):
    """Solution for Part 2."""
    numbers, symbols = data
    problem_input = list(zip(*numbers))
    return sum(solve_cephalopod_problem(input, problem) for input, problem in zip(problem_input, symbols))

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
