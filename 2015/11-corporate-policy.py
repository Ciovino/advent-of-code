# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 11 - Corporate Policy
# Problem: See .\2015/11-corporate-policy-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
from string import ascii_lowercase
CHAR_LIMIT = (ord('a'), ord('z'))

# Parse the input
with open(os.path.join('data', '2015-11.in'), 'r') as f:
    password: str = f.readline().strip()

# --- SOLVE ---
def check_password(password: list[int]) -> bool:
    # One increasing sequence of at least 3 element
    triple_increasing_sequence: bool = False
    for i in range(0, len(password) - 2):
        if password[i+2] - password[i+1] == 1 and password[i+1] - password[i] == 1:
            triple_increasing_sequence = True
            break
    if not triple_increasing_sequence:
        return False
    
    # Must not contains ['i', 'o', 'l']
    confusing_letters = list(map(ord, ['i', 'o', 'l']))
    if any([l in password for l in confusing_letters]):
        return False
    
    # Two different non-overlapping pair of letters, eg. 'aa' or 'bb'
    non_overlapping_double_sequence = 0
    password_str: str = ''.join(list(map(chr, password)))
    for i in ascii_lowercase:
        non_overlapping_double_sequence += password_str.find(f'{i}{i}') != -1
    
    if non_overlapping_double_sequence < 2:
        return False

    # All check passed
    return True
    
def increment_password(password: list[int], position: int | None = None):
    if position == None:
        position = len(password)-1    
    if position < 0:
        return
    
    password[position] += 1
    if password[position] > CHAR_LIMIT[1]:
        password[position] = CHAR_LIMIT[0]
        increment_password(password, position=position-1)

def get_next_password(old_password: str) -> str:
    # Convert password into a list of integer using the ascii code for better handling
    password: list[int] = list(map(ord, list(old_password)))
    
    increment_password(password)
    while not check_password(password):
        increment_password(password)
    
    return ''.join(list(map(chr, password)))

first_password = get_next_password(password)
second_password = get_next_password(first_password)

# --- PRINT ---
print(f"AOC_SOL_1={first_password}")
print(f"AOC_SOL_2={second_password}")
