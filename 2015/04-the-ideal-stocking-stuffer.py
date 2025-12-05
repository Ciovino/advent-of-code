# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 04 - The Ideal Stocking Stuffer
# Problem: See .\2015\04-the-ideal-stocking-stuffer-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
import hashlib

# Parse the input
with open(os.path.join('data', '2015-04.in'), 'r') as f:
    key = f.readline().strip()

# --- SOLVE ---
solutions = {
    'five 0s': -1,
    'six 0s': -1,
}
suffix = 0
while True:
    complete_key = key + str(suffix) # Append number
    md5_hash = hashlib.md5(complete_key.encode('utf-8')) # Compute hash
    hash_hex = md5_hash.hexdigest()
    
    # Check if digest matches the requirements: 5 leading 0s
    if solutions['five 0s'] == -1 and hash_hex[:5] == '00000':
        print(f"Five 0s: Key: {complete_key} | MD5 Hash (hex): {hash_hex}")
        solutions['five 0s'] = suffix
        if solutions['six 0s'] != -1: # All solutions found
            break
    if solutions['six 0s'] == -1 and hash_hex[:6] == '000000':
        print(f"Six 0s:  Key: {complete_key} | MD5 Hash (hex): {hash_hex}")
        solutions['six 0s'] = suffix
        if solutions['five 0s'] != -1: # All solutions found
            break
    suffix += 1

# --- PRINT ---
print(f"AOC_SOL_1={solutions['five 0s']}")
print(f"AOC_SOL_2={solutions['six 0s']}")
