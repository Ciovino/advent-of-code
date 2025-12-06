# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 06 - Trash Compactor
# Problem: See .\2025\06-trash-compactor-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
from math import prod

# Parse the input
number_lines: list[str] = [] # Number lines to be parsed
symbols: list[str] = []
with open(os.path.join('data', '2025-06.in'), 'r') as f:
    for line in f:
        # Check if the line is a symbols or a number line by checking the first element
        check_for_number = line.split()[0]
        
        if check_for_number.isdigit(): # Numbers
            number_lines.append(line)
        else:
            symbols = line.strip().split() # Split and save symbols

# Parse now the number, in order to keep leading/trailing spaces
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

numbers: list[list[str]] = parse_numbers(number_lines)

# --- SOLVE ---
def solve_problem(input: tuple, problem_type: str):
    # Input are strings, convert them in int
    input = tuple(map(int, input))
    
    if problem_type == '+':
        return sum(input)
    elif problem_type == '*':
        return prod(input)
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

def solve_cephalopod_problem(input: tuple, problem_type: str):
    # Zip by columns and join the strings
    new_input = tuple(map(lambda t: ''.join(t), list(zip(*input))))
    return solve_problem(new_input, problem_type)

problem_input = list(zip(*numbers))
problem_solution = [solve_problem(input, problem_type) for input, problem_type in zip(problem_input, symbols)]
cephalopod_solution = [solve_cephalopod_problem(input, problem_type) for input, problem_type in zip(problem_input, symbols)]

# --- PRINT ---
print(f"AOC_SOL_1={sum(problem_solution)}")
print(f"AOC_SOL_2={sum(cephalopod_solution)}")
