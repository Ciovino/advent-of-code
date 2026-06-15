# ---------------------------------------------------------------------
# Advent of Code 2016 - Day 10 - Balance Bots
# Problem: See ./2016/10-balance-bots-description.md for full details
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
import copy

INPUT_FILE = os.path.join('data', '2016-10.in')
TEST_FILE = os.path.join('data', 'test.in')
VERBOSE = False

def log(*args, **kwargs):
    if VERBOSE: # Print only if VERBOSE is enabled
        print(*args, **kwargs)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Solution script for 10/2016 Advent of Code.")
    parser.add_argument('-t', '--test', action='store_true',  help=f"Run the script using the test file ({TEST_FILE})")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    return parser.parse_args()

def find_numbers(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

def parse_input(file_name):
    initial_state: defaultdict[int, list[int]] = defaultdict(list)
    rules: defaultdict[int, dict[str, tuple[str, int]]] = defaultdict(lambda: {"low": ("AAAA", -1), "high": ("BBBB", -1)})

    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()

            if line.startswith('value'):
                nums = find_numbers(line)
                value, bot = nums[0], nums[1]

                initial_state[bot].append(value)
                initial_state[bot].sort()
                assert len(initial_state[bot]) < 3, f"Bot cannot have more then two microchip. '{line}'"
            elif line.startswith('bot'):
                nums = find_numbers(line)
                to_who = line.split('to')

                low = to_who[1].strip().split()[0]
                high = to_who[2].strip().split()[0]

                rules[nums[0]]['low'] = (low, nums[1])
                rules[nums[0]]['high'] = (high, nums[2])
    
    return initial_state, rules

# --- SOLVE ---
def run_step(state: dict[int, list[int]], rules, outputs: dict[int, list[int]]={}) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    # Find bot with both hands occupied
    bot_this_step = -1
    for bot, hands in state.items():
        if len(hands) == 2:
            bot_this_step = bot
            break
    else:
        log("No bots can move")
        return None, outputs
    
    # Get the rule
    rule_this_step = rules[bot_this_step]

    # Apply rule
    def apply(to_who, num, from_bot):
        if to_who == 'output': return from_bot
        new = state[num]
        new.append(from_bot)
        new.sort()
        return new

    low = apply(*rule_this_step['low'], state[bot_this_step][0])
    high = apply(*rule_this_step['high'], state[bot_this_step][1])

    # Update state
    new_state = state.copy()
    if rule_this_step['low'][0] == 'output':
        outputs[rule_this_step['low'][1]] = low
    elif rule_this_step['low'][0] == 'bot':
        new_state[rule_this_step['low'][1]] = low

    if rule_this_step['high'][0] == 'output':
        outputs[rule_this_step['high'][1]] = high
    elif rule_this_step['high'][0] == 'bot':
        new_state[rule_this_step['high'][1]] = high
    new_state.pop(bot_this_step)

    return new_state, outputs

def solve_part1(data: tuple[dict, dict]) -> int:
    """Solution for Part 1."""
    initial_state, rules = data
    current_state, _ = run_step(initial_state, rules)
    result_bot = -1

    while current_state:
        # Check the current state for the win condition
        for bot, hands in current_state.items():
            if hands == [17, 61]: return bot

        current_state, _ = run_step(current_state, rules)
    
    return -1

def solve_part2(data):
    """Solution for Part 2."""
    initial_state, rules = data
    current_state, outputs = run_step(initial_state, rules)

    while current_state:
        current_state, outputs = run_step(current_state, rules, outputs)

    return outputs[0] * outputs[1] * outputs[2]

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
    sol1 = solve_part1(copy.deepcopy(data))
    log(f"Part 1: {sol1}, took {time.time()-start_time:.4f}s")
    
    # Part 2
    start_time = time.time()
    sol2 = solve_part2(copy.deepcopy(data))
    log(f"Part 2: {sol2}, took {time.time()-start_time:.4f}s")

    # --- PRINT SOLUTIONS ---
    print(f"AOC_SOL_1={sol1}")
    print(f"AOC_SOL_2={sol2}")
