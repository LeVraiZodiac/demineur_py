import random
import time

from Case import Case

class Difficulty:
    EASY = (9, 9, 10)
    MEDIUM = (16, 16, 40)
    HARD = (30, 16, 99)

class Game:
    def __init__(self, rows, cols, mines, difficulty, seed=None):
        self.is_saved = False
        self.is_running = True
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.difficulty = difficulty
        self.flags = mines
        self.seed = seed
        self.start_time = 0
        self.best_time = None
        self.grid = [[Case(row, col) for col in range(cols)] for row in range(rows)]
        self.first_position = None
        if seed is not None:
            random.seed(seed)

    def place_mines(self):
        if self.first_position:
            first_row, first_col = self.first_position
            forbidden_positions = {(first_row + dr, first_col + dc)
                                   for dr in range(-2, 3) for dc in range(-2, 3)
                                   if 0 <= first_row + dr < self.rows and 0 <= first_col + dc < self.cols}
        else:
            forbidden_positions = set()

        possible_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)
                              if (r, c) not in forbidden_positions]
        selected_positions = random.sample(possible_positions, self.mines)

        for row, col in selected_positions:
            self.grid[row][col].is_mine = True

    def calculate_adjacent_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.grid[row][col].is_mine:
                    adjacent = self.get_adjacent_cases(row, col)
                    self.grid[row][col].adjacent_mines = sum(1 for cell in adjacent if cell.is_mine)

    def get_adjacent_cases(self, row, col):
        adjacent = []
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if r != row or c != col:
                    adjacent.append(self.grid[r][c])
        return adjacent

    def first_move(self, row, col):
        if self.first_position is None:
            self.first_position = (row, col)
            self.start_time = time.time()
            self.place_mines()
            self.calculate_adjacent_mines()

    def reveal_case(self, row, col):
        self.first_move(row, col)
        case = self.grid[row][col]
        if case.reveal():
            if case.adjacent_mines == 0:
                for adjacent in self.get_adjacent_cases(row, col):
                    if not adjacent.is_revealed and not adjacent.is_flagged and adjacent.button:
                        self.reveal_case(adjacent.row, adjacent.col)
            return True
        return False