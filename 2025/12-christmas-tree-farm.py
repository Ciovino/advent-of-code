# ---------------------------------------------------------------------
# Advent of Code 2025 - Day 12 - Christmas Tree Farm
# Problem: See .\2025/12-christmas-tree-farm-description.md for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os
import argparse
import re

INPUT_FILE = os.path.join('data', '2025-12.in')
TEST_FILE = os.path.join('data', 'test.in')

def get_args():
    parser = argparse.ArgumentParser(description="Process data files.")
    
    # Optional positional argument (for 'test')
    # nargs='?' means the argument is optional
    parser.add_argument(
        'mode', 
        nargs='?', 
        help="Optional mode (type 'test' to use test data)"
    )
    
    # Flag for verbose (store_true sets it to True if present, False otherwise)
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true', 
        help="Enable verbose output"
    )
    
    return parser.parse_args()

# Parse the input
def parse_input(file_name):
    blocks = {}
    grids = []
    block_id = None
    block_lines = []

    block_header_pattern = re.compile(r"^(\d+):$") # match "0:"
    grid_pattern = re.compile(r"^(\d+)x(\d+):\s*(.*)$") # match "4x4: 0 0 0 0 2 0"

    def save_current_block():
        nonlocal block_id, block_lines
        if block_id is not None and block_lines:
            blocks[block_id] = [line.strip() for line in block_lines]
            block_lines = []
            block_id = None
            
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            grid_match = grid_pattern.match(line)
            if grid_match:
                save_current_block() # save last block if it was building one
                
                height, width = int(grid_match.group(1)), int(grid_match.group(2))
                number_str = grid_match.group(3)
                numbers = tuple(map(int, number_str.split()))
                
                grids.append(((height, width), numbers))
            
            header_match = block_header_pattern.match(line) # Check for blocks
            if header_match:
                save_current_block()
                
                block_id = int(header_match.group(1))
                continue
            
            if block_id is not None:
                block_lines.append(line)
                
    save_current_block() # Save last block
    return blocks, grids

# --- SOLVE ---
class Block:
    def __init__(self, block_id, raw_shape):
        self.id = block_id
        self.base_shape = self._parse(raw_shape)
        self.area = len(self.base_shape)
        self.variations = self._generate_variations()
        
        max_r = max(r for r, _ in self.base_shape)
        max_c = max(c for _, c in self.base_shape)
        self.height = max_r + 1
        self.width = max_c + 1
        self.bbox_area = self.height * self.width
    
    def _parse(self, lines):
        coords = set()
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                if char == '#':
                    coords.add((r, c))
        return self._normalize(coords)
    
    def _normalize(self, coords):
        if not coords: return frozenset()
        min_r = min(r for r, _ in coords)
        min_c = min(c for _, c in coords)
        return frozenset((r-min_r, c-min_c) for r, c in coords)
    
    def _generate_variations(self):
        unique_shapes = set()
        current = self.base_shape
        
        for _ in range(4): # 4 rotations
            unique_shapes.add(self._normalize(current))
            
            flipped = set((r, -c) for r, c in current)
            unique_shapes.add(self._normalize(flipped))
            
            current = set((c, -r) for r, c in current)
        return list(unique_shapes)
    
    def visualize(self):
        print(f"--- Block {self.id} Area {self.area} ({len(self.variations)} variations) ---")
        print(f"  Bounding Box: {self.height}x{self.width}")
        for idx, var in enumerate(self.variations):
            max_r = max(r for r, _ in var)
            max_c = max(c for _, c in var)
            
            print(f"v{idx}")
            for r in range(max_r+1):
                row_str = ""
                for c in range(max_c+1):
                    if (r, c) in var:
                        row_str += " # "
                    else:
                        row_str += ' - '
                print(row_str)
            print()

class Solver:
    def __init__(self, height: int, width: int, blocks_to_use_counts: tuple[int], all_blocks_ref: dict[int, Block]):
        self.height = height
        self.width = width
        self.grid = self._reset_grid()
        self.state = 'Not solved yet'
        
        self.block_to_place = []
        for b_id, count in enumerate(blocks_to_use_counts):
            block = all_blocks_ref[b_id]
            for _ in range(count):
                self.block_to_place.append(block)
        self.block_to_place.sort(key=lambda b: b.area, reverse=True)
    
    def _reset_grid(self):
        return [['.' for _ in range(self.width)] for _ in range(self.height)]
    
    def solve(self) -> bool:
        # Area sanity check
        if sum(p.area for p in self.block_to_place) > (self.height * self.width):
            self.state = "Cannot be solved (area non sufficient)"
            return False
        
        # Fast bounding box solver
        total_bbox_area = sum(p.bbox_area for p in self.block_to_place)
        if total_bbox_area <= (self.height * self.width):
            # Run the bbox solver
            mask = [False for _ in range(len(self.block_to_place))]
            if self._solve_bbox(mask):
                self.state = "Solved using Bounding Boxes"
                return True
        
        # Slow Bruteforce+Backtracking
        self.grid = self._reset_grid()
        mask = [False for _ in range(len(self.block_to_place))]
        if self._solve_bruteforce(mask):
            self.state = "Solved using Bruteforce"
            return True
        else:
            self.state = "Cannot be solved"
            return False

    def _solve_bbox(self, mask: list[bool]):
        if all(mask):
            return True
        
        for i in range(len(self.block_to_place)):
            if not mask[i]:
                block: Block = self.block_to_place[i]
                break
        h, w = block.height, block.width
        for r in range(self.height - h + 1):
            for c in range(self.width - w + 1):                        
                if self._can_place_rect(r, c, h, w):
                    self._place_shape(r, c, h, w, block.base_shape, block.id, filler='-')
                    mask[i] = True
                    if self._solve_bbox(mask):
                        return True
                    self._remove_shape(r, c, h, w, block.base_shape, block.id, filler='-') # Backtrack
                    mask[i] = False
        return False
        
    def _can_place_rect(self, r, c, h, w):
        for i in range(r, r + h):
            for j in range(c, c + w):
                if self.grid[i][j] != '.':
                    return False
        return True
    
    def _place_shape(self, r, c, h, w, shape: set, id: int, filler: str = '.'):
        for dr in range(h):
            for dc in range(w):
                if (dr, dc) in shape:
                    self.grid[r+dr][c+dc] = id
                elif filler != '.':
                    self.grid[r+dr][c+dc] = filler
    
    def _remove_shape(self, r, c, h, w, shape: set, id: int, filler: str = '.'):
        for dr in range(h):
            for dc in range(w):
                if (dr, dc) in shape or self.grid[r+dr][c+dc] == filler:
                    self.grid[r+dr][c+dc] = '.'
    
    def _solve_bruteforce(self, mask):
        if all(mask):
            return True
        
        for i in range(len(self.block_to_place)):
            if not mask[i]:
                block: Block = self.block_to_place[i]
                break
        
        for shape_coords in block.variations:
            var_h = max(r for r, _ in shape_coords) + 1
            var_w = max(c for _, c in shape_coords) + 1
            
            for r in range(self.height):
                for c in range(self.width):
                    if self.grid[r][c] != '.': continue
                    if self._can_place_shape(shape_coords, r, c):
                        self._place_shape(r, c, var_h, var_w, shape_coords, block.id)
                        mask[i] = True
                        if self._solve_bruteforce(mask):
                            return True
                        self._remove_shape(r, c, var_h, var_w, shape_coords, block.id)
                        mask[i] = False
        return False
    
    def _can_place_shape(self, shape, r, c):
        for dr, dc in shape:
            try:
                if self.grid[r+dr][c+dc] != '.':
                    return False
            except IndexError:
                return False
        return True

    def print_state(self):
        print(self.state)
        if "yet" in self.state:
            print()
            return
        if self.state.startswith('Cannot'):
            print()
            return
        
        for r in range(self.height):
            row_str = []
            for c in range(self.width):
                val = self.grid[r][c]
                if isinstance(val, int):
                    val = chr(val + 65)
                else:
                    val = '.'
                row_str.append(f" {val} ")
            print("".join(row_str))
        print()

if __name__ == '__main__':
    args = get_args()
    if args.mode and args.mode.lower() == 'test' and os.path.exists(TEST_FILE):
        use_file = TEST_FILE
    else:
        use_file = INPUT_FILE
    VERBOSE = args.verbose
    
    blocks, grids = parse_input(use_file)
    blocks = {b_id: Block(b_id, b_lines) for b_id, b_lines in blocks.items()}
    if VERBOSE:
        for block in blocks.values():
            block.visualize()

    solvable = 0
    for g in grids:
        solver = Solver(g[0][0], g[0][1], g[1], blocks)
        solvable += solver.solve()
        if VERBOSE:
            print(f"Grid ({solver.height}x{solver.width}: {g[1]}): ", end='')
            solver.print_state()

    # --- PRINT ---
    print(f"AOC_SOL_1={solvable}")
