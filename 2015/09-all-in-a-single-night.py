# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 09 - All In A Single Night
# Problem: See .\2015/09-all-in-a-single-night-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
import itertools

# Parse the input
locations: list[str] = []
locations_tmp: set[str] = set()
edges: list[tuple[str, str, int]] = []
with open(os.path.join('data', '2015-09.in'), 'r') as f:
    for line in f:
        splitted_line = line.strip().split()
        # Example: London to Dublin = 464
        start, end, distance = splitted_line[0], splitted_line[2], splitted_line[-1]
        
        locations_tmp.add(start)
        locations_tmp.add(end)
        edges.append((start, end, int(distance)))
locations = sorted(list(locations_tmp))

# --- SOLVE ---
def build_adjacency_matrix(locations: list[str], edges: list[tuple[str, str, int]]):
    N: int = len(locations)
    location_to_index: dict[str, int] = {loc: i for i, loc in enumerate(locations)}
    
    graph = [[float('inf')] * N for _ in range(N)]
    for i in range(N):
        graph[i][i] = 0
    
    for start, end, distance in edges:
        i = location_to_index[start]
        j = location_to_index[end]
        graph[i][j] = min(graph[i][j], distance)
        graph[j][i] = min(graph[j][i], distance)
    
    return graph

def compute_all_paths(locations: set[str], edges: list[tuple[str, str, int]]) -> list:
    N: int = len(locations) # number of nodes
    graph = build_adjacency_matrix(locations, edges)
    
    # Compute complete paths and the total distance
    # variation of the TSP
    indices = list(range(N))
    all_paths = []
    
    for path_indices in itertools.permutations(indices): # All possible permutations
        current_distance = 0
        possible = True
        
        for i in range(N - 1):
            start = path_indices[i]
            end = path_indices[i+1]
            segment = graph[start][end]
            
            if segment == float('inf'):
                possible = False
                break
            current_distance += segment
        if possible:
            path_names = [locations[i] for i in path_indices]
            all_paths.append((path_names, current_distance))
    
    all_paths.sort(key=lambda x: x[1])
    return all_paths

all_paths = compute_all_paths(locations, edges)

# --- PRINT ---
print(f"AOC_SOL_1={all_paths[0][1]}")
print(f"AOC_SOL_2={all_paths[-1][1]}")
