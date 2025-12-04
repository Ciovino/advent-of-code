# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 04 - Printing Department
# Problem: See ./04-printing-department-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------

# Read the input file
INPUT_FILE = "data/2025-04.in"

# Collect paper rolls into a matrix
paper_rolls: list[list[str]] = []
with open(INPUT_FILE, 'r') as f:
    for line in f:
        paper_rolls.append(list(line.strip()))

# Compute number of rows and columns
ROWS, COLUMNS = len(paper_rolls), len(paper_rolls[0])

def can_be_accessed(paper_rolls: list[list[str]], r: int, c: int):
    neighbors_paper_rolls = 0
    for i in [-1, 0, 1]:
        # [Previous, Same, Next] Row
        row_index = r + i
        # Skip if outside the map
        if row_index < 0 or row_index >= len(paper_rolls):
            continue
        
        for j in [-1, 0, 1]:
            # [Previous, Same, Next] Column
            col_index = c + j
            # Skip if outside the map
            if col_index < 0 or col_index >= len(paper_rolls[0]):
                continue
            # Skip itself
            if row_index == r and col_index == c:
                continue
            
            if paper_rolls[row_index][col_index] == '@':
                neighbors_paper_rolls += 1
    
    # It can be removed if it has less than 4 roll neighbors
    return neighbors_paper_rolls < 4

paper_rolls_removed: list[int] = [] # How many rolls removed each turn
while True:
    # List of coords for rolls to be removed at the end of the round
    to_be_removed: list[tuple[int, int]] = []
    
    # Loop the matrix
    for r in range(ROWS):
        for c in range(COLUMNS):
            # Check only if it's a paper roll
            if paper_rolls[r][c] == '@':
                # Check if the paper roll can be removed
                #   e.g: at most 3 out of 8 neighbors are paper rolls
                if can_be_accessed(paper_rolls, r, c):
                    to_be_removed.append((r, c))

    removed_paper_rolls = len(to_be_removed)
    if removed_paper_rolls == 0:
        # Ending condition
        break
    
    # Save round value
    paper_rolls_removed.append(removed_paper_rolls)
    
    # Remove paper rolls
    for r, c in to_be_removed:
        paper_rolls[r][c] = '.'

print(f"(Part One) Paper rolls that can be accessed by a forklift:  {paper_rolls_removed[0]}") # Just the first round
print(f"(Part Two) Total number of paper rolls that can be removed: {sum(paper_rolls_removed)}")