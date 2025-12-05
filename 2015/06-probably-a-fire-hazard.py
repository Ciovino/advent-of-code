# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 06 - Probably A Fire Hazard
# Problem: See .\2015\06-probably-a-fire-hazard-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
GRID_DIM = 1000

# Parse the input
# Command, starting position (x, y), ending position (x, y)
instructions: list[tuple[str, tuple[int, int], tuple[int, int]]] = []
with open(os.path.join('data', '2015-06.in'), 'r') as f:
    # turn off 660,55 through 986,197
    for line in f:
        instruction = line.strip().split(' ')
        command = ' '.join(instruction[0: -3])
        start = tuple(map(int, instruction[-3].split(',')))
        end = tuple(map(int, instruction[-1].split(',')))
        instructions.append((command, start, end))

# --- SOLVE ---
def translate_operation(command: str, part: int):
    if part == 1:
        if command == 'turn on':
            operation: function = lambda light: 1
        elif command == 'turn off':
            operation: function = lambda light: 0
        elif command == 'toggle':
            operation: function = lambda light: (light + 1) % 2
        else:
            raise ValueError(f"Unknown command: {command}")
    elif part == 2:
        if command == 'turn on':
            operation: function = lambda light: light + 1
        elif command == 'turn off':
            operation: function = lambda light: max(light - 1, 0)
        elif command == 'toggle':
            operation: function = lambda light: light + 2
        else:
            raise ValueError(f"Unknown command: {command}")
    else:
        raise ValueError(f"Unknown part: {part}")
    
    return operation

def execute_command(grid: list[list[int]], command: str, start: tuple[int, int], end: tuple[int, int], part: int) -> None:
    # Sanity check on start and end positions
    if (start[0] < 0 or start[0] >= GRID_DIM) or \
        (start[1] < 0 or start[1] >= GRID_DIM) or \
        (end[0] < 0 or end[0] >= GRID_DIM) or \
        (end[1] < 0 or end[1] >= GRID_DIM):
        raise ValueError(f"Start or End position are out of range: start: {start}, end: {end}")
    
    # Dispatch command
    operation = translate_operation(command, part)

    # Loop from start to end and apply the operation
    for r in range(start[0], end[0] + 1): # end is included
        for c in range(start[1], end[1] + 1):
            grid[r][c] = operation(grid[r][c])

# Initialize light grid
#   0 off, 1 on
grid_part1: list[list[int]] = [[0]*GRID_DIM for _ in range(GRID_DIM)]
grid_part2: list[list[int]] = [[0]*GRID_DIM for _ in range(GRID_DIM)]

# Apply instructions
for command, start, end in instructions:
    execute_command(grid_part1, command, start, end, part=1)
    execute_command(grid_part2, command, start, end, part=2)

# --- PRINT ---
print(f"AOC_SOL_1={sum([sum(row) for row in grid_part1])}")
print(f"AOC_SOL_2={sum([sum(row) for row in grid_part2])}")
