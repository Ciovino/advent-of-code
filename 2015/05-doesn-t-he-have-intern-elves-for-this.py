# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 05 - Doesn'T He Have Intern-Elves For This?
# Problem: See .\2015\05-doesn't-he-have-intern-elves-for-this-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# Parse the input
with open(os.path.join('data', '2015-05.in'), 'r') as f:
    strings_to_check: list[str] = list(map(lambda s: s.strip(), f.readlines()))

# --- SOLVE ---
# Define each condition as a function
# Part 1
def three_vowels(S: str) -> bool:
    return sum([S.count(vowel) for vowel in 'aeiou']) >= 3

def double_letter(S: str) -> bool:
    for i in range(len(S) - 1):
        if S[i] == S[i+1]:
            return True
    return False

def avoid_naughty(S: str) -> bool:
    naughty = ['ab', 'cd', 'pq', 'xy']
    return max([S.find(n) for n in naughty]) < 0

# Part 2
def double_substring(S: str) -> bool:
    for i in range(len(S) - 1):
        if S.count(S[i:i+2]) > 1:
            return True
    return False

def repeated_letter_with_step(S: str) -> bool:
    for i in range(len(S) - 2):
        if S[i] == S[i+2]:
            return True
    return False

# Filter strings
nice_strings_part1 = list(filter(lambda S: all([three_vowels(S), double_letter(S), avoid_naughty(S)]), strings_to_check))
nice_strings_part2 = list(filter(lambda S: all([double_substring(S), repeated_letter_with_step(S)]), strings_to_check))

# --- PRINT ---
print(f"AOC_SOL_1={len(nice_strings_part1)}")
print(f"AOC_SOL_2={len(nice_strings_part2)}")
