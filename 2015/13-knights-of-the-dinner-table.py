# ---------------------------------------------------------------------
# Advent of Code 2015 - Day 13 - Knights Of The Dinner Table
# Problem: See .\2015\13-knights-of-the-dinner-table-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
from itertools import permutations

# Parse the input
happiness_points: dict[tuple[str, str], int] = {}
with open(os.path.join('data', '2015-13.in'), 'r') as f:
    for line in f:
        splitted_line = line.strip().split()
        who, potentially, amount, next_to = splitted_line[0], splitted_line[2], splitted_line[3], splitted_line[-1][:-1]
        total_happiness = int(amount) * (1 if potentially == 'gain' else -1)
        happiness_points[(who, next_to)] = total_happiness

# --- SOLVE ---
def get_people(scores) -> list[str]:
    people = set(p1 for (p1, _), _ in scores.items())
    people.update(p2 for (_, p2), _ in scores.items())
    return sorted(list(people))

def get_best_arrangement(scores: dict[tuple[str, str], int]) -> int:
    def calculate_score(arrangement: list[str], scores_dict: dict[tuple[str, str], int]) -> int:
        total_score = 0
        num_people = len(arrangement)
        for i in range(num_people):
            p1, p2 = arrangement[i], arrangement[(i + 1) % num_people] # Wrap around
            total_score += scores_dict.get((p1, p2), 0) + scores_dict.get((p2, p1), 0) # Get score, check for both pair
        return total_score
    return max([calculate_score(arrangement, scores) for arrangement in permutations(get_people(scores))])

scores: dict[tuple[str, str], int] = {pair: score for pair, score in happiness_points.items()}
print(f"AOC_SOL_1={get_best_arrangement(scores)}")

# Part 2 - Add myself, and set 0 points for every combinations of people
for p in get_people(scores):
    scores[("Me", p)] = 0
print(f"AOC_SOL_2={get_best_arrangement(scores)}")
