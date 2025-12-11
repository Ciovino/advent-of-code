# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 11 - Reactor
# Problem: See .\2025\11-reactor-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# Parse the input
connections: dict[str, list[str]] = {}
with open(os.path.join('data', '2025-11.in'), 'r') as f:
    for line in f:
        in_out = line.strip().split(':')
        input_str, output = in_out[0], in_out[1].split()
        connections[input_str] = output

# --- SOLVE ---
def get_paths(start: str, end:str, connections: dict[str, list[str]], required: set[str] = set()) -> int:
    def run_all_path(position: str, required_found: int, cache: dict[tuple[str, int], int]) -> int:
        nonlocal end, required
        if position == end: # Reached the target position
            return int(required_found >= len(required))

        # How many path lead to "end" from "position"
        total_paths = 0
        for out in connections[position]:
            if out in required:
                required_found += 1
            
            if (out, required_found) in cache:
                out_result = cache[(out, required_found)]
            else:
                out_result = run_all_path(out, required_found, cache)
                cache[(out, required_found)] = out_result
            
            total_paths += out_result
            if out in required:
                required_found -= 1
        return total_paths

    return run_all_path(start, 0, {})

you_to_out = get_paths("you", "out", connections)
svr_to_out = get_paths("svr", "out", connections, required={"dac", "fft"})

# --- PRINT ---
print(f"AOC_SOL_1={you_to_out}")
print(f"AOC_SOL_2={svr_to_out}")
