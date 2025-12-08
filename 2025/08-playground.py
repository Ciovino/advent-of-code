# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 08 - Playground
# Problem: See .\2025/08-playground-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
from math import sqrt, prod

PAIR = 1000

# Parse the input
jboxes: dict[int, tuple[int, int, int]] = {}
with open(os.path.join('data', '2025-08.in'), 'r') as f:
    for i, line in enumerate(f):
        jboxes[i] = tuple(map(int, line.strip().split(',')))

# --- SOLVE ---
def distance(point_a: tuple, point_b: tuple):
    return sqrt(sum([(a - b)**2 for a, b in zip(point_a, point_b)]))

def compute_all_distances(all_points: dict[int, tuple]) -> list[tuple[int, int, float]]:
    N = len(all_points)
    all_pairs: list[tuple[int, int, float]] = [] # (Point_A, Point_B, distance_A_B)
    for i in range(N-1):
        for j in range(i + 1, N):
            A, B = all_points[i], all_points[j]
            all_pairs.append((i, j, distance(A, B)))
    
    all_pairs.sort(key=lambda x: x[2]) # Sort by distance
    return all_pairs

def find(jbox_A: int, parents: list[int]) -> int:
    if parents[jbox_A] == jbox_A:
        return jbox_A
    parents[jbox_A] = find(parents[jbox_A], parents) # Recursively find the parents of jbox_A
    return parents[jbox_A]

def connect_jboxes(parents: list[int], jbox_A: int, jbox_B: int) -> bool:
    root_A = find(jbox_A, parents) # Find in which group jbox_A and jbox_B are in
    root_B = find(jbox_B, parents)
    
    if root_A != root_B:
        # Connect the two group
        parents[root_B] = root_A
        return True
    return False
    
circuits: list[int] = list(range(len(jboxes))) # Each jbox is in its own circuit
all_pairs: list[tuple[tuple, tuple, float]] = compute_all_distances(jboxes)

part_1_solved = -1
last_connected_pair: tuple[int, int] = (-1, -1)
group_sizes: dict[int, int] = {}
for i, (jbox_A, jbox_B, _) in enumerate(all_pairs):
    if i == PAIR:
        for i in range(len(circuits)):
            # Find the root for jbox_i
            root = find(i, circuits)
            dim = group_sizes.get(root, 0)
            group_sizes[root] = dim + 1
        part_1_solved = prod(sorted(group_sizes.values(), reverse=True)[:3])
    
    if connect_jboxes(circuits, jbox_A, jbox_B):
        last_connected_pair = (jbox_A, jbox_B)

# --- PRINT ---
print(f"AOC_SOL_1={part_1_solved}")
print(f"AOC_SOL_2={jboxes[last_connected_pair[0]][0] * jboxes[last_connected_pair[1]][0]}")
