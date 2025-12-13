# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 03 - Perfectly Spherical Houses In A Vacuum
# Problem: See .\2015/03-perfectly-spherical-houses-in-a-vacuum-description.md for full details
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

INPUT_FILE = os.path.join('data', '2015-03.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 03/2015 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> list[str]:
    with open(file_name, 'r') as f:
        data: list[str] = list(f.readline().strip())
    return data

# --- SOLVE ---
def convert_move_to_tuple(move: str) -> tuple[int, int]:
    if move == '>': # Right
        return (1, 0)
    elif move == '<': # Left
        return (-1, 0)
    elif move == '^': # Up
        return (0, 1)
    elif move == 'v': # Down
        return (0, -1)
    else:
        raise ValueError(f"Unknown move: {move}")

def solve_part1(moves: list[str]) -> int:
    """Solution for Part 1."""
    santa_position: tuple[int, int] = (0, 0)
    houses: set[tuple[int, int]] = {(0, 0)}
    for move in moves:
        move: tuple[int, int] = convert_move_to_tuple(move)
        santa_position = tuple(s + m for s, m in zip(santa_position, move))
        houses.add(santa_position)
    return len(houses)

def solve_part2(moves: list[str]) -> int:
    """Solution for Part 2."""
    santas_positions: dict[int, tuple[int, int]] = {
        0: (0, 0),  # Normal Santa
        1: (0, 0)   # Robo-Santa
    }
    houses: set[tuple[int, int]] = {(0, 0)}
    for i, move in enumerate(moves):
        move: tuple[int, int] = convert_move_to_tuple(move)
        turn = i % 2
        santas_positions[turn] = tuple(s + m for s, m in zip(santas_positions[turn], move))
        houses.add(santas_positions[turn])
    return len(houses)

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
