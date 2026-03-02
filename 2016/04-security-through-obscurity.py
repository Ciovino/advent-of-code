# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 04 - Security Through Obscurity
# Problem: See ./2016/04-security-through-obscurity-description.md for full details
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
from string import ascii_lowercase

INPUT_FILE = os.path.join('data', '2016-04.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 04/2016 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name) -> list[tuple[str, int, str]]:
    data: list[tuple[str, int, str]] = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            room, checksum = line[:-7], line[-6:-1]
            encrypted_room = room.split('-')
            
            room_name, sector_id = '-'.join(encrypted_room[:-1]), encrypted_room[-1]
            
            data.append((''.join(room_name), int(sector_id), checksum))
    return data

# --- SOLVE ---
def is_valid_room(room: str, checksum: str):
    # Filter out '-'
    room = room.replace('-', '')

    frequencies = list(Counter(room).items())
    # Need to sort the computed_checksum by frequency, then order
    frequencies.sort(key=lambda x: (-x[1], x[0]))

    # Extract checksum and compare
    computed_checksum = ''.join(list(map(lambda x: x[0], frequencies))[:5])
    return computed_checksum == checksum 

def run_ceasar_cipher(original_str: str, rotation: int):
    normalized_rotation = rotation % len(ascii_lowercase) # full rotation does nothing
    if normalized_rotation == 0: return original_str

    new_str = ""
    for c in original_str:
        if c == '-':
            # If '-', replace with space
            new_str += ' '
        else:
            # If letter, rotate it
            letter_idx = ascii_lowercase.find(c)
            new_str += ascii_lowercase[(letter_idx + normalized_rotation) % len(ascii_lowercase)]
    
    log(f"{original_str} +{normalized_rotation} (+{rotation}) -> {new_str}")
    return new_str

def solve_part1(rooms: list[tuple[str, int, str]]):
    """Solution for Part 1."""
    valid_room = list(filter(lambda x: is_valid_room(x[0], x[2]), rooms))
    return sum([r[1] for r in valid_room])

def solve_part2(rooms: list[tuple[str, int, str]]):
    """Solution for Part 2."""
    valid_room = list(filter(lambda x: is_valid_room(x[0], x[2]), rooms))
    decrypted_rooms = list(map(lambda x: (run_ceasar_cipher(x[0], x[1]), x[1]), valid_room))

    # Find room id with northpole object
    for room, sector_id in decrypted_rooms:
        if room.find('north') != -1:
            return sector_id
    else:
        raise ValueError(f"No rooms contains string 'north'")

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
