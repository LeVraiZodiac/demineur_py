import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import time

class Case:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
        self.button = None

    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
            self.button.config(text="⚑" if self.is_flagged else "")
            self.button.config(fg="blue" if self.is_flagged else "black")

    def reveal(self):
        if not self.is_flagged:
            self.is_revealed = True
            self.button.config(state="disabled")
            if self.is_mine:
                self.button.config(text="*", bg="red")
                return False
            else:
                self.button.config(text=str(self.adjacent_mines) if self.adjacent_mines > 0 else "")
                self.button.config(bg="light grey")
                return True

class Grille:
    def __init__(self, rows, cols, mines, seed=None):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[Case(row, col) for col in range(cols)] for row in range(rows)]
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self.place_mines()
        self.calculate_adjacent_mines()

    def place_mines(self):
        placed_mines = 0
        while placed_mines < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.grid[row][col].is_mine:
                self.grid[row][col].is_mine = True
                placed_mines += 1

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

    def reveal_case(self, row, col):
        case = self.grid[row][col]
        if case.reveal():
            if case.adjacent_mines == 0:
                for adjacent in self.get_adjacent_cases(row, col):
                    if not adjacent.is_revealed:
                        self.reveal_case(adjacent.row, adjacent.col)
            return True
        return False

class Demineur:
    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        self.difficulty = None
        self.grid = None
        self.rows = 0
        self.cols = 0
        self.start_time = None
        self.seed = None
        self.create_menu()

    def get_high_scores(self):
        high_scores = {"Facile": "Aucun", "Moyen": "Aucun", "Difficile": "Aucun"}
        scores_file = "scores.json"
        if os.path.exists(scores_file):
            with open(scores_file, 'r') as f:
                scores = json.load(f)
                for score in scores:
                    if score['victory']:
                        difficulty = score['difficulty']
                        time = round(score['time'], 2)
                        if high_scores[difficulty] == "Aucun" or time < high_scores[difficulty]:
                            high_scores[difficulty] = time
        return high_scores

    def create_menu(self):
        self.clear_window()
        high_scores = self.get_high_scores()
        label = tk.Label(self.root, text="Meilleurs Scores :", font=("Arial", 14))
        label.pack(pady=10)

        for difficulty, time in high_scores.items():
            score_label = f"{difficulty}: {time} sec"
            label = tk.Label(self.root, text=score_label, font=("Arial", 12))
            label.pack(pady=2)

        label = tk.Label(self.root, text="Choisissez la difficulté :", font=("Arial", 14))
        label.pack(pady=20)

        for difficulty in ["Facile", "Moyen", "Difficile"]:
            btn = tk.Button(self.root, text=difficulty, font=("Arial", 12), width=10,
                            command=lambda d=difficulty: self.set_difficulty(d))
            btn.pack(pady=5)

        btn_saved_games = tk.Button(self.root, text="Parties Sauvegardées", font=("Arial", 12),
                                   command=self.show_saved_games)
        btn_saved_games.pack(pady=10)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.setup_game()

    def setup_game(self):
        if self.difficulty == "Facile":
            rows, cols, mines = 9, 9, 10
        elif self.difficulty == "Moyen":
            rows, cols, mines = 16, 16, 40
        else:
            rows, cols, mines = 24, 24, 99

        self.rows = rows
        self.cols = cols
        self.seed = random.randint(0, 10000)
        self.grid = Grille(rows, cols, mines, seed=self.seed)
        self.start_time = time.time()
        self.create_widgets(rows, cols)

    def create_widgets(self, rows, cols):
        self.clear_window()
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=self.cols * 30, height=self.rows * 30)
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        for row in range(rows):
            for col in range(cols):
                btn = tk.Button(self.inner_frame, width=2, height=1, command=lambda r=row, c=col: self.click_case(r, c))
                btn.grid(row=row, column=col)
                self.grid.grid[row][col].button = btn
                btn.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(r, c))

        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def click_case(self, row, col):
        case = self.grid.grid[row][col]
        if case.is_flagged:
            return
        if self.grid.reveal_case(row, col):
            if self.check_victory():
                self.victory()
        else:
            self.game_over()

    def toggle_flag(self, row, col):
        case = self.grid.grid[row][col]
        case.toggle_flag()

    def game_over(self):
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                case = self.grid.grid[row][col]
                if case.is_mine:
                    case.button.config(text="*", bg="red")
        self.show_defeat_screen()

    def check_victory(self):
        mines_flagged = sum(1 for row in self.grid.grid for case in row if case.is_mine and case.is_flagged)
        cases_revealed = sum(1 for row in self.grid.grid for case in row if case.is_revealed and not case.is_mine)
        total_cases = self.grid.rows * self.grid.cols
        return mines_flagged == self.grid.mines and cases_revealed == total_cases - self.grid.mines

    def victory(self):
        self.clear_window()
        label = tk.Label(self.root, text="Félicitations, vous avez gagné !", font=("Arial", 16))
        label.pack(pady=20)

        replay_btn = tk.Button(self.root, text="Rejouer", font=("Arial", 12), command=self.setup_game)
        replay_btn.pack(pady=5)

        main_menu_btn = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 12),
                                  command=self.create_menu)
        main_menu_btn.pack(pady=5)

        end_time = time.time()
        elapsed_time = end_time - self.start_time
        self.save_score(True, elapsed_time)

    def show_defeat_screen(self):
        self.clear_window()
        label = tk.Label(self.root, text="Dommage, vous avez perdu.", font=("Arial", 16))
        label.pack(pady=20)

        replay_btn = tk.Button(self.root, text="Rejouer", font=("Arial", 12), command=self.setup_game)
        replay_btn.pack(pady=5)

        main_menu_btn = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 12), command=self.create_menu)
        main_menu_btn.pack(pady=5)

        end_time = time.time()
        elapsed_time = end_time - self.start_time
        self.save_score(False, elapsed_time)

    def save_score(self, victory, elapsed_time):
        scores_file = "scores.json"
        score_data = {
            "difficulty": self.difficulty,
            "victory": victory,
            "time": elapsed_time,
            "seed": self.seed,
            "timestamp": time.ctime()
        }

        if not os.path.exists(scores_file):
            with open(scores_file, 'w') as f:
                json.dump([score_data], f)
        else:
            with open(scores_file, 'r+') as f:
                scores = json.load(f)
                scores.append(score_data)
                f.seek(0)
                json.dump(scores, f)

    def show_saved_games(self):
        self.clear_window()
        label = tk.Label(self.root, text="Parties Sauvegardées", font=("Arial", 14))
        label.pack(pady=20)

        scores_file = "scores.json"
        if not os.path.exists(scores_file):
            tk.Label(self.root, text="Aucune partie sauvegardée.").pack()
            return

        with open(scores_file, 'r') as f:
            scores = json.load(f)

        self.saved_games_frame = tk.Frame(self.root)
        self.saved_games_frame.pack(fill="both", expand=True)

        self.saved_games_canvas = tk.Canvas(self.saved_games_frame)
        self.saved_games_canvas.pack(side="left", fill="both", expand=True)

        self.saved_games_scrollbar = tk.Scrollbar(self.saved_games_frame, orient="vertical", command=self.saved_games_canvas.yview)
        self.saved_games_canvas.config(yscrollcommand=self.saved_games_scrollbar.set)

        self.saved_games_scrollbar.pack(side="right", fill="y")

        self.saved_games_inner_frame = tk.Frame(self.saved_games_canvas)
        self.saved_games_canvas.create_window((0, 0), window=self.saved_games_inner_frame, anchor="nw")

        for i, score in enumerate(scores):
            result = "Victoire" if score['victory'] else "Défaite"
            score_label = f"Partie {i + 1} - Difficulté: {score['difficulty']} - {result} - Temps: {round(score['time'], 2)} sec"
            label = tk.Label(self.saved_games_inner_frame, text=score_label, font=("Arial", 12))
            label.pack(pady=5)

            replay_btn = tk.Button(self.saved_games_inner_frame, text="Rejouer", command=lambda seed=score['seed']: self.replay_game(seed))
            replay_btn.pack(pady=2)

        self.saved_games_inner_frame.update_idletasks()
        self.saved_games_canvas.config(scrollregion=self.saved_games_canvas.bbox("all"))

        back_btn = tk.Button(self.root, text="Retour", command=self.create_menu)
        back_btn.pack(pady=10)

    def replay_game(self, seed):
        self.seed = seed
        saved_score = self.get_saved_score_by_seed(seed)
        if saved_score:
            difficulty = saved_score['difficulty']
            if difficulty == "Facile":
                rows, cols, mines = 9, 9, 10
            elif difficulty == "Moyen":
                rows, cols, mines = 16, 16, 40
            else:
                rows, cols, mines = 24, 24, 99

            self.rows = rows
            self.cols = cols
            self.grid = Grille(rows, cols, mines, seed=self.seed)
            self.start_time = time.time()
            self.create_widgets(rows, cols)

    def get_saved_score_by_seed(self, seed):
        scores_file = "scores.json"
        if not os.path.exists(scores_file):
            return None
        with open(scores_file, 'r') as f:
            scores = json.load(f)
            for score in scores:
                if score['seed'] == seed:
                    return score
        return None

if __name__ == "__main__":
    root = tk.Tk()
    jeu = Demineur(root)
    root.mainloop()