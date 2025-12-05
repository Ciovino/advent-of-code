# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 05 - Cafeteria
# Problem: See .\2025/05-cafeteria-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# Parse the input
fresh_ingredient_ids: list[tuple[int, int]] = []
ingredients: list[int] = []
with open(os.path.join('data', '2025-05.in'), 'r') as f:
    reading_ranges = True # Did not encounter the empty separator line
    for line in f:
        if reading_ranges:
            if line.strip() == "":
                reading_ranges = False
                continue
            
            fresh_ingredient_ids.append(tuple(map(int, line.strip().split('-'))))
        else:
            # Reading the ingredients list
            ingredients.append(int(line.strip()))

# --- SOLVE ---
def is_fresh(ingredient: int, fresh_ingredient_ids: list[tuple[int, int]]) -> bool:
    for range_ in fresh_ingredient_ids:
        if range_[1] < ingredient:
            # Skip range
            continue
        if range_[0] > ingredient:
            # Ingredient definetly spoiled
            return False
        if range_[0] < ingredient < range_[1]:
            # Ingredient is fresh
            return True
    return False # Fallback

def compact_list(tuple_list: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # Sort the list by the first element of the tuple
    tuple_list.sort(key=lambda range_: range_[0])
    
    # Create a compact version
    compact_list: list[tuple[int, int]] = []
    current_range = (-1, -1)
    for range_ in tuple_list:
        if current_range == (-1, -1): # Initialization
            current_range = range_
            continue
        
        if current_range[1] < range_[0]:
            # No overlap. Save the current range and update it
            compact_list.append(current_range)
            current_range = range_
        else:
            # Overlap. Compact ranges
            current_range = (current_range[0], max(current_range[1], range_[1]))
    # Append last element
    compact_list.append(current_range)
    return compact_list.copy()

# Compact the fresh ingredients list
compacted_ingredients_ids: list[tuple[int, int]] = compact_list(fresh_ingredient_ids)

# Loop the ingredients
fresh_ingredients: list[int] = list(filter(lambda ing: is_fresh(ing, compacted_ingredients_ids), ingredients))

# --- PRINT ---
print(f"AOC_SOL_1={len(fresh_ingredients)}")
print(f"AOC_SOL_2={sum(list(map(lambda range_: range_[1] - range_[0] + 1, compacted_ingredients_ids)))}")
