# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 11 - Radioisotope Thermoelectric Generators
# Problem: See ./2016/11-radioisotope-thermoelectric-generators-description.md for full details
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

INPUT_FILE = os.path.join('data', '2016-11.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 11/2016 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name):
    elements = {} 
    
    with open(file_name, 'r') as f:
        for floor_num, line in enumerate(f):
            matches = re.findall(r'(\w+)(?:-compatible)? (generator|microchip)', line)
            
            for element, item_type in matches:
                if element not in elements:
                    elements[element] = {'generator': -1, 'microchip': -1}
                elements[element][item_type] = floor_num
                
    pairs = []
    for props in elements.values():
        pairs.append((props['generator'], props['microchip']))
        
    initial_state = (0, tuple(sorted(pairs))) # Floor, Elements
    return initial_state

# --- SOLVE ---
def get_object_in_floor(state):
    floor_number, elements = state
    generators, microchips = [], []
    
    for idx, (generator, microchip) in enumerate(elements):
        if generator == floor_number:
            generators.append(idx)
        if microchip == floor_number:
            microchips.append(idx)
    
    return generators, microchips

def get_objects_to_move(generators, microchips):
    moves = []

    # Combinations of two objects
    # Only generators
    if len(generators) > 1:
        for g1 in range(len(generators)-1):
            for g2 in range(g1+1, len(generators)):
                moves.append({0: [generators[g1], generators[g2]]})
    
    # Only microchip
    if len(microchips) > 1:
        for m1 in range(len(microchips)-1):
            for m2 in range(m1+1, len(microchips)):
                moves.append({1: [microchips[m1], microchips[m2]]})

    # One generator and one microchip
    if len(generators) + len(microchips) > 1:
        for g in range(len(generators)):
            for m in range(len(microchips)):
                moves.append({0: [generators[g]], 1: [microchips[m]]})
    
    # Only one object
    for g in generators:
        moves.append({0: [g]})
    for m in microchips:
        moves.append({1: [m]})
    
    return moves

def generate_moves(current_floor, generators, microchips):
    objects_to_move = get_objects_to_move(generators, microchips)
    
    moves = []
    for obj in objects_to_move:
        if current_floor - 1 >= 0:
            moves.append({'floor': current_floor-1, 'objects': obj})
        if current_floor + 1 <= 4:
            moves.append({'floor': current_floor+1, 'objects': obj})
    
    return moves

def generate_new_state(current_state, move):
    _, pairs = current_state
    new_floor = move['floor']
    
    # 1. Convert immutable tuples to mutable lists
    mutable_pairs = [list(p) for p in pairs]
    
    # 2. Apply the move
    for item_type, elem_ids in move['objects'].items():
        for elem in elem_ids:
            mutable_pairs[elem][item_type] = new_floor
        
    # 3. Re-pack into tuples and sort for the visited hash
    new_pairs = tuple(sorted((tuple(p) for p in mutable_pairs)))
    
    return (new_floor, new_pairs)

def is_valid(state):
    _, elements = state

    for chip_idx, (_, chip) in enumerate(elements):
        same_generator = False
        other_generator = False
        
        for generator_idx, (generator, _) in enumerate(elements):
            if generator_idx == chip_idx:
                same_generator = generator == chip
            else:
                other_generator |= generator == chip
        
        if other_generator and not same_generator:
            return False
    
    return True

def ending_state(state):
    # Check if everything is at the last floor
    _, elements = state
    
    for generator, chip in elements:
        if generator != 3 or chip != 3:
            return False
    
    return True

def solve_part1(initial_state):
    """Solution for Part 1."""
    log(initial_state)

    # Setup for BFS
    queue = deque([(initial_state, 0)])
    visited = {initial_state}

    while queue:
        current_state, steps = queue.popleft()
        if ending_state(current_state): return steps

        generators, microchips = get_object_in_floor(current_state)
        moves = generate_moves(current_state[0], generators, microchips)

        for move in moves:
            new_state = generate_new_state(current_state, move)

            if new_state not in visited and is_valid(new_state):
                visited.add(new_state)
                queue.append((new_state, steps + 1))
     
    return -1

def solve_part2(initial_state):
    """Solution for Part 2."""
    # Add two new pairs of Generator-Microchip on first floor
    part_2_state = [list(p) for p in initial_state[1]]
    part_2_state.append([0, 0])
    part_2_state.append([0, 0])
    part_2_state = tuple(sorted((tuple(p) for p in part_2_state)))
    part_2_initial = (0, part_2_state)

    return solve_part1(part_2_initial)

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
