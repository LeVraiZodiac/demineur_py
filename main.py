import tkinter as tk
from Game import Game, Difficulty

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.game = None
        self.cells = []
        self.load_main_menu()
        self.revealed_cells = set()
        self.color = ["#D3D3D3", "#0000FF", "#3300E6", "#6600CC", "#9900B3", "#CC0099", "#FF0066", "#FF0033", "#FF0000"]

    def load_main_menu(self):
        self.clear_window()

        label = tk.Label(self.root, text="Minesweeper", font=("Arial", 24))
        label.pack(pady=20)

        buttons = [
            ("New Game", self.load_difficulty_menu),
            ("Load Game", self.load_game_saved_menu),
            ("Scoreboard", self.load_scoreboard_menu),
            ("Exit", self.root.destroy)
        ]
        for text, command in buttons:
            button = tk.Button(self.root, text=text, font=("Arial", 14), command=command)
            button.pack(pady=10)

    def load_difficulty_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text="Choose Difficulty", font=("Arial", 24))
        label.pack(pady=20)

        difficulties = [
            ("Easy", Difficulty.EASY),
            ("Medium", Difficulty.MEDIUM),
            ("Hard", Difficulty.HARD)
        ]
        for text, difficulty in difficulties:
            btn = tk.Button(self.root, text=text, font=("Arial", 14), width=10,
                            command=lambda d=difficulty: self.start_game(d))
            btn.pack(pady=10)

        button = tk.Button(self.root, text="Back", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

    def start_game(self, difficulty):
        self.clear_window()
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()

        rows, cols, mines = difficulty
        self.game = Game(rows, cols, mines)
        self.cells = [[None for _ in range(cols)] for _ in range(rows)]

        for row in range(rows):
            for col in range(cols):
                btn = tk.Button(self.grid_frame, text="", width=4, height=3,
                                command=lambda r=row, c=col: self.reveal_cell(r, c), bg="grey")
                btn.grid(row=row, column=col)
                self.cells[row][col] = btn

    def reveal_cell(self, row, col):
        if (row, col) in self.revealed_cells or not self.game.is_valid_cell(row, col):
            return

        self.revealed_cells.add((row, col))
        cell_value = self.game.reveal_cell(row, col)

        if cell_value == "mine":
            self.cells[row][col].config(text="X", fg="white", bg="black", state="disabled")
            self.game_over()
        elif cell_value == 0:
            self.cells[row][col].config(text="", bg="lightgrey", state="disabled")
            cells_to_reveal = self.game.reveal_around_cell(row, col)
            for next_row, next_col in cells_to_reveal:
                self.reveal_cell(next_row, next_col)
        else:
            self.cells[row][col].config(text=str(cell_value), fg="white", bg=self.color[cell_value], state="disabled")

    def game_over(self):
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                cell_value = self.game.grid[row][col]
                if (row, col) not in self.revealed_cells:
                    if cell_value == -1:
                        self.cells[row][col].config(text="X", fg="white", bg="black", state="disabled")
                    elif cell_value > 0:
                        self.cells[row][col].config(text=str(cell_value), fg="white", bg=self.color[cell_value], state="disabled")
                    else:
                        self.cells[row][col].config(text="", bg="lightgrey", state="disabled")
        #self.load_game_over_screen()

    def load_game_over_screen(self):
        self.clear_window()

        label = tk.Label(self.root, text="Game Over", font=("Arial", 36), fg="red")
        label.pack(pady=20)

    def load_game_saved_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text="Load Game", font=("Arial", 24))
        label.pack(pady=20)

        button = tk.Button(self.root, text="Back", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

    def load_scoreboard_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text="Best Score", font=("Arial", 24))
        label.pack(pady=20)

        label = tk.Label(self.root, text="Test : 13m14s", font=("Arial", 24))
        label.pack(pady=20)

        button = tk.Button(self.root, text="Back", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
