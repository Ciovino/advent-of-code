# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 08 - Playground
# Problem: See .\2025/08-playground-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
import argparse
import time

# Useful imports
import re
from collections import defaultdict, Counter, deque
from itertools import combinations, permutations, product
from math import gcd, lcm, ceil, floor, sqrt, prod

INPUT_FILE = os.path.join('data', '2025-08.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False
PAIR = 1000

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 08/2025 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> tuple[dict[int, tuple[int, int, int]], list[int], list[tuple[tuple, tuple, float]]]:
    data: dict[int, tuple[int, int, int]] = {}
    with open(file_name, 'r') as f:
        for i, line in enumerate(f):
            data[i] = tuple(map(int, line.strip().split(',')))
    return data, list(range(len(data))), compute_all_distances(data)

# --- SOLVE ---
def distance(point_a: tuple, point_b: tuple):
    return sqrt(sum([(a - b)**2 for a, b in zip(point_a, point_b)]))

def compute_all_distances(all_points: dict[int, tuple]) -> list[tuple[int, int, float]]:
    N = len(all_points)
    all_pairs: list[tuple[int, int, float]] = [] # (Point_A, Point_B, distance_A_B)
    for i in range(N-1):
        for j in range(i + 1, N):
            A, B = all_points[i], all_points[j]
            all_pairs.append((i, j, distance(A, B)))
    
    all_pairs.sort(key=lambda x: x[2]) # Sort by distance
    return all_pairs

def find(jbox_A: int, parents: list[int]) -> int:
    if parents[jbox_A] == jbox_A:
        return jbox_A
    parents[jbox_A] = find(parents[jbox_A], parents) # Recursively find the parents of jbox_A
    return parents[jbox_A]

def connect_jboxes(parents: list[int], jbox_A: int, jbox_B: int) -> bool:
    root_A = find(jbox_A, parents) # Find in which group jbox_A and jbox_B are in
    root_B = find(jbox_B, parents)
    
    if root_A != root_B:
        # Connect the two group
        parents[root_B] = root_A
        return True
    return False

def solve_part1(data: tuple[dict[int, tuple[int, int, int]], list[int], list[tuple[tuple, tuple, float]]]) -> int:
    """Solution for Part 1."""
    _, circuits, all_pairs = data # Unpack
    group_sizes: dict[int, int] = {}

    for i, (jbox_A, jbox_B, _) in enumerate(all_pairs):
        if i == PAIR:
            for j in range(len(circuits)):
                root = find(j, circuits)
                size = group_sizes.get(root, 0)
                group_sizes[root] = size + 1
            return prod(sorted(group_sizes.values(), reverse=True)[:3])
        connect_jboxes(circuits, jbox_A, jbox_B)
    return 0

def solve_part2(data: tuple[dict[int, tuple[int, int, int]], list[int], list[tuple[tuple, tuple, float]]]) -> int:
    """Solution for Part 2."""
    jboxes, circuits, all_pairs = data # Unpack
    last_connected: tuple[int, int] = (-1, -1)
    
    for jbox_A, jbox_B, _ in all_pairs:
        if connect_jboxes(circuits, jbox_A, jbox_B):
            last_connected = (jbox_A, jbox_B)
    
    return jboxes[last_connected[0]][0] * jboxes[last_connected[1]][0]

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
