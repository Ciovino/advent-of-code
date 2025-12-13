# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 09 - All In A Single Night
# Problem: See .\2015/09-all-in-a-single-night-description.md for full details
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

INPUT_FILE = os.path.join('data', '2015-09.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 09/2015 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> tuple[list[str], list[tuple[str, str, int]]]:
    locations: list[str] = []
    edges: list[tuple[str, str, int]] = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip().split()
            
            start, end, distance = line[0], line[2], line[-1]
            
            locations.append(start)
            locations.append(end)
            edges.append((start, end, int(distance)))
    return sorted(list(set(locations))), edges # Locations -> Remove duplicate and sort

# --- SOLVE ---
def build_adjacency_matrix(locations: list[str], edges: list[tuple[str, str, int]]):
    N: int = len(locations)
    location_to_index: dict[str, int] = {loc: i for i, loc in enumerate(locations)}
    
    graph = [[float('inf')] * N for _ in range(N)]
    for i in range(N):
        graph[i][i] = 0
    
    for start, end, distance in edges:
        i = location_to_index[start]
        j = location_to_index[end]
        graph[i][j] = min(graph[i][j], distance)
        graph[j][i] = min(graph[j][i], distance)
    
    return graph

def compute_all_paths(locations: set[str], edges: list[tuple[str, str, int]]) -> list:
    N: int = len(locations) # number of nodes
    graph = build_adjacency_matrix(locations, edges)
    
    # Compute complete paths and the total distance
    # variation of the TSP
    indices = list(range(N))
    all_paths = []
    
    for path_indices in permutations(indices): # All possible permutations
        current_distance = 0
        possible = True
        
        for i in range(N - 1):
            start = path_indices[i]
            end = path_indices[i+1]
            segment = graph[start][end]
            
            if segment == float('inf'):
                possible = False
                break
            current_distance += segment
        if possible:
            path_names = [locations[i] for i in path_indices]
            all_paths.append((path_names, current_distance))
    
    all_paths.sort(key=lambda x: x[1])
    return all_paths

def solve_part1(data: tuple[list[str], list[tuple[str, str, int]]]) -> int:
    """Solution for Part 1."""
    locations, edges = data # Unpack
    all_paths = compute_all_paths(locations, edges)
    return all_paths[0][1]

def solve_part2(data: tuple[list[str], list[tuple[str, str, int]]]) -> int:
    """Solution for Part 2."""
    locations, edges = data # Unpack
    all_paths = compute_all_paths(locations, edges)
    return all_paths[-1][1]

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
