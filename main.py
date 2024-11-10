import tkinter as tk
import random
import json
import os
import time

from Game import Game, Difficulty

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        self.root.resizable(False, False)
        self.game = None
        self.old_seed = None
        self.load_main_menu()

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

    def load_main_menu(self):
        self.clear_window()

        label = tk.Label(self.root, text="Démineur", font=("Arial", 24))
        label.pack(pady=20)

        buttons = [
            ("Nouvelle partie", self.load_difficulty_menu),
            ("Parties Sauvegardées", self.show_saved_games),
            ("Scoreboard", self.load_scoreboard_menu),
            ("Fermer", self.root.destroy)
        ]

        for text, command in buttons:
            button = tk.Button(self.root, text=text, font=("Arial", 14), command=command)
            button.pack(pady=10)

    def load_difficulty_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text="Choisir la difficulté", font=("Arial", 24))
        label.pack(pady=20)

        difficulties = [
            ("Easy", Difficulty.EASY),
            ("Medium", Difficulty.MEDIUM),
            ("Hard", Difficulty.HARD)
        ]
        for text, difficulty in difficulties:
            btn = tk.Button(self.root, text=text, font=("Arial", 14), width=10,
                            command=lambda d=difficulty: self.set_game(d))
            btn.pack(pady=10)

        button = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

    def load_scoreboard_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text="Vos meilleurs scores", font=("Arial", 24))
        label.pack(pady=20)

        high_scores = self.get_high_scores()
        label = tk.Label(self.root, text="Meilleurs Scores :", font=("Arial", 14))
        label.pack(pady=10)

        for difficulty, time in high_scores.items():
            score_label = f"{difficulty}: {time} sec"
            label = tk.Label(self.root, text=score_label, font=("Arial", 14))
            label.pack(pady=2)

        button = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

    def set_game(self, difficulty):
        rows, cols, mines = difficulty
        self.game = Game(rows, cols, mines, difficulty, seed=random.randint(0, 10000))
        self.load_grid()

    def load_grid(self):
        self.clear_window()
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        rows, cols, mines = self.game.difficulty
        for row in range(rows):
            for col in range(cols):
                btn = tk.Button(self.frame, width=4, height=3, command=lambda r=row, c=col: self.click_case(r, c))
                btn.grid(row=row, column=col)
                self.game.grid[row][col].button = btn
                btn.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(r, c))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def click_case(self, row, col):
        case = self.game.grid[row][col]
        if case.is_flagged:
            return
        if self.game.reveal_case(row, col):
            if self.check_victory():
                self.victory()
        else:
            self.game_over()

    def toggle_flag(self, row, col):
        case = self.game.grid[row][col]
        case.toggle_flag()

    def game_over(self):
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                case = self.game.grid[row][col]
                if case.is_mine:
                    case.button.config(text="*", bg="red")
        self.show_defeat_screen()

    def check_victory(self):
        mines_flagged = sum(1 for row in self.game.grid for case in row if case.is_mine and case.is_flagged)
        cases_revealed = sum(1 for row in self.game.grid for case in row if case.is_revealed and not case.is_mine)
        total_cases = self.game.rows * self.game.cols
        return mines_flagged == self.game.mines and cases_revealed == total_cases - self.game.mines

    def victory(self):
        self.clear_window()
        label = tk.Label(self.root, text="Félicitations, vous avez gagné !", font=("Arial", 24))
        label.pack(pady=20)

        replay_btn = tk.Button(self.root, text="Rejouer", font=("Arial", 14),
                               command=lambda: self.replay_game(self.game.seed))
        replay_btn.pack(pady=10)

        button = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

        end_time = time.time()
        elapsed_time = end_time - self.game.start_time
        self.save_game(True, elapsed_time)

    def show_defeat_screen(self):
        self.clear_window()
        label = tk.Label(self.root, text="Dommage, vous avez perdu.", font=("Arial", 24))
        label.pack(pady=20)

        replay_btn = tk.Button(self.root, text="Rejouer", font=("Arial", 14),
                               command=lambda: self.replay_game(self.game.seed))
        replay_btn.pack(pady=5)

        button = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

        end_time = time.time()
        elapsed_time = end_time - self.game.start_time
        self.save_game(False, elapsed_time)

    def show_saved_games(self):
        self.clear_window()
        label = tk.Label(self.root, text="Parties Sauvegardées", font=("Arial", 24))
        label.pack(pady=20)

        scores_file = "scores.json"
        if not os.path.exists(scores_file):
            tk.Label(self.root, text="Aucune partie sauvegardée.", font=("Arial", 14)).pack()

            button = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14),
                               command=self.load_main_menu)
            button.pack(pady=10)
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
            label = tk.Label(self.saved_games_inner_frame, text=score_label, font=("Arial", 14))
            label.pack(pady=5)

            replay_btn = tk.Button(self.saved_games_inner_frame, text="Rejouer", font=("Arial", 14), command=lambda seed=score['seed']: self.replay_game(seed))
            replay_btn.pack(pady=10)

        self.saved_games_inner_frame.update_idletasks()
        self.saved_games_canvas.config(scrollregion=self.saved_games_canvas.bbox("all"))

        button = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

    def save_game(self, victory, elapsed_time):
        if self.game.seed == self.old_seed:
            return
        else:
            self.old_seed = self.game.seed

        scores_file = "scores.json"

        def case_to_dict(case):
            return {
                "is_mine": case.is_mine,
            }

        grid_serializable = [
            [case_to_dict(cell) for cell in row] for row in self.game.grid
        ]

        score_data = {
            "seed": self.game.seed,
            "victory": victory,
            "time": elapsed_time,
            "difficulty": self.game.difficulty,
            "first_position": self.game.first_position,
            "grid": grid_serializable,
            "timestamp": time.ctime()
        }

        if not os.path.exists(scores_file) or os.path.getsize(scores_file) == 0:
            with open(scores_file, 'w') as f:
                json.dump([score_data], f)
        else:
            with open(scores_file, 'r+') as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = []
                scores.append(score_data)
                f.seek(0)
                json.dump(scores, f)
                f.truncate()

    def replay_game(self, seed):
        saved_score = self.get_saved_score_by_seed(seed)
        if saved_score:
            difficulty = saved_score['difficulty']
            rows, cols, mines = difficulty

            self.game = Game(rows, cols, mines, difficulty, seed=seed)
            self.game.first_position = saved_score['first_position']
            self.game.start_time = time.time()

            # First create the grid UI
            self.load_grid()

            # Then load the saved game state
            self.load_grid_from_saved(saved_score['grid'])
            self.game.calculate_adjacent_mines()

            # Finally reveal the first move
            r, c = self.game.first_position
            self.click_case(r, c)

    def load_grid_from_saved(self, saved_grid):
        for r in range(len(saved_grid)):
            for c in range(len(saved_grid[r])):
                self.game.grid[r][c].is_mine = saved_grid[r][c]["is_mine"]

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
    jeu = Minesweeper(root)
    root.mainloop()