import random

class Difficulty:
    EASY = [9, 9, 10]
    MEDIUM = [16, 16, 40]
    HARD = [30, 16, 99]

class Game:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()
        self.calculate_adjacent_mines()
        self.first_position = None

    def is_valid_cell(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get_mine_positions(self):
        return self.mine_positions

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
            self.mine_positions.add((row, col))
            self.grid[row][col] = -1

    def calculate_adjacent_mines(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for row, col in self.mine_positions:
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != -1:
                    self.grid[r][c] += 1

    def reveal_around_cell(self, row, col):
        cells_to_reveal = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            next_row, next_col = row + dr, col + dc
            if self.is_valid_cell(next_row, next_col):
                cells_to_reveal.append((next_row, next_col))

        return cells_to_reveal

    def first_move(self, row, col):
        if self.first_position is None:
            self.first_position = (row, col)
            self.place_mines()
            self.calculate_adjacent_mines()

    def reveal_cell(self, row, col):
        self.first_move(row, col)
        if (row, col) in self.mine_positions:
            return "mine"
        return self.grid[row][col]