# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 12 - Jsabacusframework.Io
# Problem: See .\2015\12-jsabacusframework-io-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
import json

# Parse the input
with open(os.path.join('data', '2015-12.in'), 'r') as f:
    json_content: dict = json.loads(f.readline())

# --- SOLVE ---
def explore_json(json_content: dict | list | int | str, double_count: bool=False) -> int:
    if isinstance(json_content, dict):
        if double_count and "red" in json_content.values():
            return 0
        iterator = iter(json_content.values())
    elif isinstance(json_content, list):
        iterator = iter(json_content)
    elif isinstance(json_content, (int, str)):
        try:
            return int(json_content)
        except:
            return 0    
    return sum([explore_json(element, double_count=double_count) for element in iterator])

total_numbers = explore_json(json_content)
total_numbers_without_red = explore_json(json_content, double_count=True)

# --- PRINT ---
print(f"AOC_SOL_1={total_numbers}")
print(f"AOC_SOL_2={total_numbers_without_red}")
