# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 09 - Movie Theater
# Problem: See .\2025/09-movie-theater-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
from bisect import bisect_left, bisect_right

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

def build_edges(points: list[tuple[int, int]]) -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    h_edges = [] # (y, x_min, x_max)
    v_edges = [] # (x, y_min, y_max)
    
    n = len(points)
    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n] # Wrap around to first point
        
        if p1[1] == p2[1]: # Horizontal
            h_edges.append((p1[1], min(p1[0], p2[0]), max(p1[0], p2[0])))
        else: # Vertical
            v_edges.append((p1[0], min(p1[1], p2[1]), max(p1[1], p2[1])))
            
    # Sort for binary search
    h_edges.sort(key=lambda e: e[0]) # Sort by Y
    v_edges.sort(key=lambda e: e[0]) # Sort by X
    return h_edges, v_edges

def is_valid_rect(r_x1: int, r_x2: int, r_y1: int, r_y2: int, h_edges: list[tuple[int, int, int]], v_edges: list[tuple[int, int, int]]) -> bool:
    # Normalize coords
    x_min, x_max = min(r_x1, r_x2), max(r_x1, r_x2)
    y_min, y_max = min(r_y1, r_y2), max(r_y1, r_y2)

    # Find vertical edges with x strictly between x_min and x_max
    start_idx = bisect_right(v_edges, (x_min, float('inf'), float('inf')))
    end_idx = bisect_left(v_edges, (x_max, -1, -1))
    
    for i in range(start_idx, end_idx):
        _, vy_min, vy_max = v_edges[i]
        # Intersection if the edge's Y range strictly overlaps rect's Y range
        if not (vy_max <= y_min or vy_min >= y_max):
            return False

    # Find horizontal edges with y strictly between y_min and y_max
    start_idx = bisect_right(h_edges, (y_min, float('inf'), float('inf')))
    end_idx = bisect_left(h_edges, (y_max, -1, -1))
    
    for i in range(start_idx, end_idx):
        _, hx_min, hx_max = h_edges[i]
        # Intersection if the edge's X range strictly overlaps rect's X range
        if not (hx_max <= x_min or hx_min >= x_max):
            return False

    # If no edges cross the interior, the rect is either fully inside or fully outside.
    # Test the midpoint
    mid_x = (x_min + x_max) / 2.0
    mid_y = (y_min + y_max) / 2.0
    
    # Ray Casting
    intersections = 0
    
    start_search = bisect_right(v_edges, (mid_x, float('inf'), float('inf')))
    for i in range(start_search, len(v_edges)):
        _, vy_min, vy_max = v_edges[i]
        if vy_min <= mid_y < vy_max:
            intersections += 1

    return (intersections % 2) == 1 # Odd intersections => Inside

h_edges, v_edges = build_edges(red_tiles)
rectangles: list[tuple[tuple[int, int], tuple[int, int], int]] = get_all_rectangles(red_tiles)
found_area: int = 0
for p1, p2, area in rectangles:
    if is_valid_rect(p1[0], p2[0], p1[1], p2[1], h_edges, v_edges):
        found_area = area
        break

# --- PRINT ---
print(f"AOC_SOL_1={rectangles[0][2]}")
print(f"AOC_SOL_2={found_area}")
