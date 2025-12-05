# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 02 - Gift shop
# Problem: See ./02-gift-shop-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# Parse the input
with open(os.path.join('data', '2025-02.in'), 'r') as f:
    line = f.readline().strip()
    
    id_ranges: list[str] = line.split(',')

def double_sequence(id: int) -> bool:
    # Part One
    # Check if an id is made up by a sequence repeated twice
    
    id_str = str(id)
    
    # If a sequence is repeated twice, the id must have an even length
    if len(id_str) % 2 != 0:
        return False
    
    # Divide the string in two parts and compare
    midpoint = len(id_str) // 2
    first_half, second_half = id_str[:midpoint], id_str[midpoint:]
    
    return first_half == second_half

def repeated_sequence(id: int) -> bool:
    # Part Two
    # Check if an id is made up of a sequence repeated N times
    
    id_str = str(id)
    
    for sequence_length in range(1, len(id_str) // 2 + 1):
        # Repeat for each possible sequence
        # The length of the string must be a multiple of the length of the sequence
        if len(id_str) % sequence_length != 0: continue # Skip this one
        
        sequence = id_str[:sequence_length]
        if id_str.count(sequence) * sequence_length == len(id_str):
            return True
    
    return False # All possible checks failed

# Collect all the invalid ids, separating for each part
invalid_ids: dict[str, list[int]] = {
    "part-one": [],
    "part-two": []
} 
for id_range in id_ranges:
    # Extract first and last id
    first_id, last_id = tuple(map(int, id_range.split('-')))
    
    # Loop for each id in the range, including the extremes
    for id in range(first_id, last_id + 1):
        if double_sequence(id):
            invalid_ids['part-one'].append(id)
            # A invalid id for part one is also invalid for part tow
            invalid_ids['part-two'].append(id)
        elif repeated_sequence(id):
            # Check with the more general function
            invalid_ids['part-two'].append(id)

# --- PRINT ---
print(f"AOC_SOL_1={sum(invalid_ids['part-one'])}")
print(f"AOC_SOL_2={sum(invalid_ids['part-two'])}")
