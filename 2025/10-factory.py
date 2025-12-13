# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 10 - Factory
# Problem: See .\2025/10-factory-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
import argparse
import time

# Useful imports
import re
from collections import defaultdict, Counter, deque
from itertools import combinations, permutations, product
from math import gcd, lcm, ceil, floor
from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np

INPUT_FILE = os.path.join('data', '2025-10.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 10/2025 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def parse_input(file_name) -> list[tuple[str, dict[int, tuple[int]], list[int]]]:
    data: list[tuple[str, dict[int, tuple[int]], list[int]]] = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip().split()
            target, buttons, joltage = line[0], line[1:-1], line[-1]
            
            parsed_target = target[1:-1]
            parsed_buttons: dict[int, tuple[int]] = {i: tuple(map(int, b[1:-1].split(','))) for i, b in enumerate(buttons)}
            parsed_joltage: list[int] = list(map(int, joltage[1:-1].split(',')))
            
            data.append((parsed_target, parsed_buttons, parsed_joltage))
    return data

# --- SOLVE ---
def press_button(machine_state: str, button: tuple) -> str:
    new_state = list(machine_state)
    for b in button:
        new_state[b] = '.' if new_state[b] == '#' else '#' # Toggle
    return ''.join(new_state)

def solve_lights(machine: tuple[str, dict[int, tuple], list[int]]) -> tuple[int, list[int]]:
    target_state, buttons, _ = machine
    initial_state = '.' * len(target_state)
    
    queue = deque([initial_state]) # Store the state to explore
    visited = {initial_state: (None, None)} # Store {current_state: (parent_state, button_id_used_to_get_here)
    
    while queue: # While queue not empty
        current_state = queue.popleft()
        
        if current_state == target_state: # Done, get the button pressed
            path = [] # Backtrack for target to start
            curr = target_state
            while curr != initial_state:
                parent, button_id = visited[curr]
                path.append(button_id)
                curr = parent
            return len(path), path[::-1] # button needed, button used (need to be reversed)

        # Try pressing every button
        for button_id, button in buttons.items():
            next_state = press_button(current_state, button)
            if next_state not in visited:
                visited[next_state] = (current_state, button_id)
                queue.append(next_state)
    
    return -1, [] # If queue empties before reaching the target, impossible task

def solve_joltage(machine: tuple[str, dict[int, tuple], list[int]]) -> int:
    _, buttons, joltage_targets = machine
    
    # Integer Linear Programming
    num_targets = len(joltage_targets)
    num_buttons = len(buttons)
    
    # Matrix A: row -> counter; columns -> buttuns
    A = np.zeros((num_targets, num_buttons))
    for b_id, affected_indices in buttons.items():
        for t in affected_indices:
            A[t, b_id] = 1
    
    # Known vector b: joltage targets
    b = np.array(joltage_targets)
    
    # -- Solve the ILP --
    c = np.ones(num_buttons) # Minimaze c @ x (x solution) (c = [1, ..., 1])
    constraints = LinearConstraint(A, lb=b, ub=b) # Constraint A@x = b
    integrality = np.ones(num_buttons) # Array of 1 means that x must contain integers
    bounds = Bounds(lb=0, ub=np.inf) # 0 <= x <= +inf

    # Solve
    solution = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)
    if solution.success:
        return int(np.round(solution.x).sum()) # Round to avoid weird floating point numbers (3.9999...)
    else:
        raise ValueError(f"No valid solution for machine: {machine}")

def solve_part1(machines: list[tuple[str, dict[int, tuple[int]], list[int]]]) -> int:
    """Solution for Part 1."""
    return sum(solve_lights(machine)[0] for machine in machines)

def solve_part2(machines: list[tuple[str, dict[int, tuple[int]], list[int]]]) -> int:
    """Solution for Part 2."""
    return sum(solve_joltage(machine) for machine in machines)

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
