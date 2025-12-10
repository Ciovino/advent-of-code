# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 09 - Movie Theater
# Problem: See .\2025/09-movie-theater-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# Parse the input
red_tiles: list[tuple[int, int]] = []
with open(os.path.join('data', '2025-09.in'), 'r') as f:
    for line in f:
        new_tile = tuple(map(int, line.strip().split(',')))
        red_tiles.append(new_tile)

# --- SOLVE ---
def area_rectangle(corner_1: tuple[int, int], corner_2: tuple[int, int]) -> int:
    return (abs(corner_1[0] - corner_2[0]) + 1) * (abs(corner_1[1] - corner_2[1]) + 1)

def get_all_rectangles(points: list[tuple[int, int]]) -> list[tuple[tuple[int, int], tuple[int, int], int]]:
    rectangles: list[tuple[tuple[int, int], tuple[int, int], int]] = [] # [(corner_1, corner_2, area)]
    
    N: int = len(points)
    for i in range(N-1):
        for j in range(i+1, N):
            corner_1, corner_2 = points[i], points[j]
            area = area_rectangle(corner_1, corner_2)
            rectangles.append((corner_1, corner_2, area))
    
    rectangles.sort(key=lambda x: x[2], reverse=True)
    return rectangles

rectangles: list[tuple[tuple[int, int], tuple[int, int], int]] = get_all_rectangles(red_tiles)

# --- PRINT ---
print(f"AOC_SOL_1={rectangles[0][2]}")
# print(f"AOC_SOL_2={}")
