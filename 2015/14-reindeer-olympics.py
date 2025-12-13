# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 14 - Reindeer Olympics
# Problem: See ./2015\14-reindeer-olympics-description.md for full details
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

INPUT_FILE = os.path.join('data', '2015-14.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False
SIMULATION_TIME = 2503

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 14/2015 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name) -> dict[str, tuple[int, int, int]]:
    data: dict[str, tuple[int, int, int]] = {}
    with open(file_name, 'r') as f:
        for line in f:
            # Vixen can fly 18 km/s for 5 seconds, but then must rest for 84 seconds.
            name, stats = line.split()[0], tuple(find_numbers(line))
            data[name] = stats
    return data

# --- SOLVE ---
def update_reindeer(time: int, current_position: tuple[int, int, int], stats: tuple[int, int, int]) -> tuple[int, int, int]:
    if current_position[1] >= 0: # Currently flying
        if time - current_position[1] >= stats[1]: # Stop and start resting
            return (current_position[0], -1, time)
        return (current_position[0] + stats[0], current_position[1], current_position[2])
    elif current_position[2] >= 0: # Currently resting
        if time - current_position[2] >= stats[2]: # Start flying again
            return (current_position[0] + stats[0], time, -1)
        return current_position # Nothing changes

def solve_part1(reindeers_stats: dict[str, tuple[int, int, int]]) -> int:
    """Solution for Part 1."""
    global SIMULATION_TIME
    
    reindeers_name: set[str] = set(reindeers_stats.keys())
    reindeers: dict[str, tuple[int, int, int]] = {name: (0, 0, -1) for name in reindeers_name}
    for i in range(SIMULATION_TIME):
        for reindeer in reindeers_name:
            reindeers[reindeer] = update_reindeer(i, reindeers[reindeer], reindeers_stats[reindeer])
    
    return max(list(map(lambda r: r[0], reindeers.values())))

def solve_part2(reindeers_stats: dict[str, tuple[int, int, int]]) -> int:
    """Solution for Part 2."""
    global SIMULATION_TIME
    
    reindeers_name: set[str] = set(reindeers_stats.keys())
    reindeers: dict[str, tuple[int, int, int]] = {name: (0, 0, -1) for name in reindeers_name}
    points: dict[str, int] = {name: 0 for name in reindeers_name}
    
    for i in range(SIMULATION_TIME):
        for reindeer in reindeers_name:
            reindeers[reindeer] = update_reindeer(i, reindeers[reindeer], reindeers_stats[reindeer])
        
        max_distance = max(list(map(lambda r: r[0], reindeers.values())))
        for reindeer in reindeers_name:
            if reindeers[reindeer][0] == max_distance:
                points[reindeer] += 1
    
    return max(points.values())

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
