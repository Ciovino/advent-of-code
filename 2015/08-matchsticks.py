# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 08 - Matchsticks
# Problem: See .\2015\08-matchsticks-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
import json

# Parse the input
with open(os.path.join('data', '2015-08.in'), 'r') as f:
    strings_literal: list[str] = list(map(lambda s: s.strip(), f.readlines()))

# --- SOLVE ---
code_characters = sum(list(map(len, strings_literal)))
in_memory_characters = sum(list(map(lambda s: len(eval(s)), strings_literal)))
encoded_characters = sum(list(map(lambda s: len(json.dumps(s)), strings_literal)))

# --- PRINT ---
print(f"AOC_SOL_1={code_characters - in_memory_characters}")
print(f"AOC_SOL_2={encoded_characters - code_characters}")
