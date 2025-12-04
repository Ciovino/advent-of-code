# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 03 - Lobby
# Problem: See ./03-lobby-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------

# Read the input file
INPUT_FILE = "data/2025-03.in"

battery_banks: list[list] = []
with open(INPUT_FILE, "r") as f:
    for line in f.readlines():
        battery_banks.append(list(line.strip()))

def max_joltage(bank: list[str], N: int) -> int:
    # Compute the max joltage with N battery
    # Sanity check
    if N > len(bank):
        raise ValueError(f"Can't compute joltage with {N} batteries from a bank with {len(bank)} batteries.")
    
    # Idea: Grab the max battery from a section of the bank.
    #   The section starts from the position next to the last
    #   chosen battery and ends at the position that allows
    #   to still collect N batteries.
    
    max_joltage = '' # Accumulate chosen batteries
    start_position = 0
    
    for i in range(N):
        end_position = -N + i + 1
        if end_position != 0:
            bank_current_section = bank[start_position:(-N + i + 1)]
        else:
            bank_current_section = bank[start_position:]
        
        # Grab the max battery present
        chosen_battery = max(bank_current_section)
        
        # Update the starting position
        start_position += 1 + bank_current_section.index(chosen_battery)
        
        # Append battery
        max_joltage += chosen_battery
    
    # Convert result and return
    return int(max_joltage)

print(f"(Part One) Max joltage with 2 batteries per bank:  {sum(list(map(lambda bank: max_joltage(bank, 2), battery_banks)))}")
print(f"(Part Two) Max joltage with 12 batteries per bank: {sum(list(map(lambda bank: max_joltage(bank, 12), battery_banks)))}")
