# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 10 - Factory
# Problem: See .\2025/10-factory-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
from collections import deque
from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np

# Parse the input
machines: list[tuple[str, dict[int, tuple], list[int]]] = []
with open(os.path.join('data', '2025-10.in'), 'r') as f:
    for line in f:
        line_splitted = line.strip().split()
        target, buttons, joltage = line_splitted[0], line_splitted[1:-1], line_splitted[-1]
        parsed_target = target[1:-1]
        
        parsed_joltage = list(map(int, joltage[1:-1].split(',')))
        parsed_buttons: dict[int, tuple] = {i: tuple(map(int, b[1:-1].split(','))) for i, b in enumerate(buttons)}
        
        machines.append((parsed_target, parsed_buttons, parsed_joltage))

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

machine_solutions: list[tuple[int, list[int]]] = []
joltage_solutions: list[int] = []
for machine in machines:
    machine_solutions.append(solve_lights(machine))
    joltage_solutions.append(solve_joltage(machine))

# --- PRINT ---
print(f"AOC_SOL_1={sum([ms[0] for ms in machine_solutions])}")
print(f"AOC_SOL_2={sum(joltage_solutions)}")
