# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 07 - Some Assembly Required
# Problem: See .\2015\07-some-assembly-required-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

N_BITS = 16
MASK = (1 << N_BITS) - 1

# Parse the input
circuit: dict[str, str] = dict()
with open(os.path.join('data', '2015-07.in'), 'r') as f:
    for line in f:
        signal = line.strip().split('->') # (operation) -> output
        operation, wire = signal[0].strip(), signal[-1].strip()
        
        circuit[wire] = operation

# --- SOLVE ---
def compute(wire: str, circuit: dict[str, str], cache: dict[str, int]) -> int:
    # Base Case: Raw number, return it
    if wire.isdigit():
        return int(wire)
    
    # Check Cache
    if wire in cache:
        return cache[wire]

    # Get the operation from the circuit
    operation = circuit.get(wire)
    if not operation:
        raise ValueError(f"No known operation for wire {wire}")

    arguments = operation.split()
    result = 0

    # Perform Logic
    if len(arguments) == 1:
        # Assignment
        result = compute(arguments[0], circuit, cache)
    elif len(arguments) == 2:
        # NOT operation
        result = (~compute(arguments[1], circuit, cache)) & MASK
    elif len(arguments) == 3:
        left = compute(arguments[0], circuit, cache)
        right = compute(arguments[2], circuit, cache)
        op = arguments[1]
        
        if op == "AND":
            result = (left & right) & MASK
        elif op == "OR":
            result = (left | right) & MASK
        elif op == "LSHIFT":
            result = (left << right) & MASK
        elif op == "RSHIFT":
            result = (left >> right) & MASK
            
    # Save result to cache
    cache[wire] = result
    return result

cache_1: dict[str, int] = {}
wire_a_part1 = compute('a', circuit, cache_1)

# Part 2
# Override b with the value of a
circuit['b'] = str(wire_a_part1)
cache_2: dict[str, int] = {}
wire_a_part2 = compute('a', circuit, cache_2)

# --- PRINT ---
print(f"AOC_SOL_1={wire_a_part1}")
print(f"AOC_SOL_2={wire_a_part2}")
