# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 10 - Elves Look, Elves Say
# Problem: See .\2015/10-elves-look,-elves-say-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# Parse the input
with open(os.path.join('data', '2015-10.in'), 'r') as f:
    digit: list[str] = list(f.readline().strip())

# --- SOLVE ---
def look_and_say_single(digits: list[str]) -> list[str]:
    start_idx = 0
    new_digit: list[str] = []
    
    while start_idx < len(digits):
        current_digit = digits[start_idx]
        end_idx = start_idx + 1
        while end_idx < len(digits) and digits[end_idx] == current_digit:
            end_idx += 1
        new_digit += [str(end_idx - start_idx), current_digit]
        start_idx = end_idx
    return new_digit

def look_and_say(digit: list[str], steps: int) -> list[str]:
    new_digit = digit
    for _ in range(steps):
        new_digit = look_and_say_single(new_digit)
            
    return new_digit

final_digit_p1 = look_and_say(digit, 40)
final_digit_p2 = look_and_say(final_digit_p1, 50 - 40)

# --- PRINT ---
print(f"AOC_SOL_1={len(final_digit_p1)}")
print(f"AOC_SOL_2={len(final_digit_p2)}")
