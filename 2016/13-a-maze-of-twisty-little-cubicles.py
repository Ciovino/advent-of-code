# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 13 - A Maze Of Twisty Little Cubicles
# Problem: See ./2016/13-a-maze-of-twisty-little-cubicles-description.md for full details
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

INPUT_FILE = os.path.join('data', '2016-13.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 13/2016 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name):
    with open(file_name, 'r') as f:
        data = find_numbers(f.read())
    return data[0]

# --- SOLVE ---
def is_wall(x, y, office_number):
    if x < 0 or y < 0: return True
    return bin(x*x + 3*x + 2*x*y + y + y*y + office_number).count('1') & 1

def solve_bfs(start, office_number, end_condition):
    queue = deque([(start, 0)])
    visited = {start}
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    final_steps = -1

    while queue:
        current_pos, step = queue.popleft()
        log(current_pos, step)
        
        for d in directions:
            new_pos = (current_pos[0] + d[0], current_pos[1] + d[1])
            log(new_pos)

            if new_pos in visited: continue
            if is_wall(*new_pos, office_number): continue
            if end_condition(new_pos, step):
                final_steps = step + 1 
                break
            
            visited.add(new_pos)
            queue.append((new_pos, step + 1))
        
        if final_steps > 0:
            break
    
    return len(visited), final_steps

def solve_part1(office_number: int):
    """Solution for Part 1."""
    return solve_bfs((1, 1), office_number, end_condition=lambda pos, step: pos == (31, 39))[1]

def solve_part2(office_number: int):
    """Solution for Part 2."""
    return solve_bfs((1, 1), office_number, end_condition=lambda pos, step: step >= 50)[0]

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
