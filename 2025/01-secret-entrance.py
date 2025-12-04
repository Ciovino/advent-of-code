# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 01 - Secret Entrance
# Problem: See ./01-secret-entrance-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------

# Read the input file
INPUT_FILE = "data/2025-01.in"

# move: (direction, amount)
# direction => +1 if R, -1 if L
# e.g: R10 -> (+1, 10); L60 -> (-1, 60)
moves: list[tuple[str, int]] = []
with open(INPUT_FILE, 'r') as f:
    for line in f:
        direction, distance = line[0], int(line[1:])
        
        if direction != 'R' and direction != 'L':
            raise ValueError(f"Unknown operation. Received {line.strip()}")
        
        moves.append((direction, distance))

dial = 50 # Starting position
land_on_zero, total_zero_clicks = 0, 0 # Part One, Part Two

# Simulate the dial movement
for direction, distance in moves:
    step = 1 if direction == 'R' else -1
    
    for _ in range(distance):
        # Update dial
        dial = (dial + step) % 100
        if dial == 0:
            total_zero_clicks += 1
    
    # Check if lands on 0
    if dial == 0:
        land_on_zero += 1

print(f"(Part One) Landed on zero {land_on_zero} times")
print(f"(Part Two) Total clicks on zero: {total_zero_clicks}")

# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 01 - Secret Entrance
# Problem: See ./01-secret-entrance-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# move: (direction, amount)
# direction => +1 if R, -1 if L
# e.g: R10 -> (+1, 10); L60 -> (-1, 60)
moves: list[tuple[str, int]] = []
# Parse the input
with open(os.path.join('data', '2025-01.in'), 'r') as f:
    for line in f:
        direction, distance = line[0], int(line[1:])
        
        if direction != 'R' and direction != 'L':
            raise ValueError(f"Unknown operation. Received {line.strip()}")
        
        moves.append((direction, distance))

dial = 50 # Starting position
land_on_zero, total_zero_clicks = 0, 0 # Part One, Part Two

# Simulate the dial movement
for direction, distance in moves:
    step = 1 if direction == 'R' else -1
    
    for _ in range(distance):
        # Update dial
        dial = (dial + step) % 100
        if dial == 0:
            total_zero_clicks += 1
    
    # Check if lands on 0
    if dial == 0:
        land_on_zero += 1

# --- PRINT ---
print(f"AOC_SOL_1={land_on_zero}")
print(f"AOC_SOL_2={total_zero_clicks}")
