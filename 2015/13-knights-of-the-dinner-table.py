# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 13 - Knights Of The Dinner Table
# Problem: See .\2015\13-knights-of-the-dinner-table-description.md for full details
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

INPUT_FILE = os.path.join('data', '2015-13.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 13/2015 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> dict[tuple[str, str], int]:
    data: dict[tuple[str, str], int] = {}
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip().split()
            
            who, potentially, amount, next_to = line[0], line[2], line[3], line[-1][:-1]
            happiness = int(amount) * (1 if potentially == 'gain' else -1)
            
            data[(who, next_to)] = happiness
    return data

# --- SOLVE ---
def get_people(scores) -> list[str]:
    people = set(p1 for (p1, _), _ in scores.items())
    people.update(p2 for (_, p2), _ in scores.items())
    return sorted(list(people))

def get_best_arrangement(scores: dict[tuple[str, str], int]) -> int:
    def calculate_score(arrangement: list[str], scores_dict: dict[tuple[str, str], int]) -> int:
        total_score = 0
        num_people = len(arrangement)
        for i in range(num_people):
            p1, p2 = arrangement[i], arrangement[(i + 1) % num_people] # Wrap around
            total_score += scores_dict.get((p1, p2), 0) + scores_dict.get((p2, p1), 0) # Get score, check for both pair
        return total_score
    return max([calculate_score(arrangement, scores) for arrangement in permutations(get_people(scores))])

def solve_part1(happiness_points: dict[tuple[str, str], int]) -> int:
    """Solution for Part 1."""
    scores: dict[tuple[str, str], int] = {pair: score for pair, score in happiness_points.items()}
    return get_best_arrangement(scores)

def solve_part2(happiness_points: dict[tuple[str, str], int]) -> int:
    """Solution for Part 2."""
    scores: dict[tuple[str, str], int] = {pair: score for pair, score in happiness_points.items()}
    for p in get_people(scores):
        scores[("Me", p)] = 0
    return get_best_arrangement(scores)

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
