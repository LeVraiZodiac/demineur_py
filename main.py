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
        self.timer_label = None
        self.elapsed_time = 0
        self.load_main_menu()

    def load_main_menu(self):
        self.clear_window()

        label = tk.Label(self.root, text="Démineur", font=("Arial", 24))
        label.pack(pady=20)

        buttons = [
            ("Nouvelle partie", self.load_difficulty_menu),
            ("Parties Sauvegardées", self.load_saved_games_menu),
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
            ("Facile", Difficulty.EASY),
            ("Moyen", Difficulty.MEDIUM),
            ("Difficile", Difficulty.HARD)
        ]
        for text, difficulty in difficulties:
            btn = tk.Button(self.root, text=text, font=("Arial", 14), width=10,
                            command=lambda d=difficulty: self.set_game(d))
            btn.pack(pady=10)

        button = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

    def load_saved_games_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text="Parties Sauvegardées", font=("Arial", 24))
        label.pack(pady=20)

        scores_file = "scores.json"
        if not os.path.exists(scores_file) or os.path.getsize(scores_file) == 0:
            tk.Label(self.root, text="Aucune partie sauvegardée.", font=("Arial", 14)).pack(pady=10)
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

        self.saved_games_scrollbar = tk.Scrollbar(self.saved_games_frame, orient="vertical",
                                                  command=self.saved_games_canvas.yview)
        self.saved_games_canvas.config(yscrollcommand=self.saved_games_scrollbar.set)
        self.saved_games_scrollbar.pack(side="right", fill="y")

        self.saved_games_inner_frame = tk.Frame(self.saved_games_canvas)
        self.saved_games_canvas.create_window((0, 0), window=self.saved_games_inner_frame, anchor="nw")

        difficulties_names = {
            Difficulty.EASY: "Facile",
            Difficulty.MEDIUM: "Moyen",
            Difficulty.HARD: "Difficile"
        }

        for i, score in enumerate(scores):
            card_frame = tk.Frame(self.saved_games_inner_frame, relief="raised", borderwidth=2, padx=10, pady=10)
            card_frame.pack(fill="x", pady=10)

            difficulty = tuple(score['difficulty'])
            result = "Victoire" if score['victory'] else "Défaite"

            score_label_text = f"Partie {i + 1} - Seed: {score['seed']}"
            score_label = tk.Label(card_frame, text=score_label_text, font=("Arial", 14))
            score_label.pack(side="top", pady=5)

            score_label_text = f"Difficulté: {difficulties_names[difficulty]} - {result}"
            score_label = tk.Label(card_frame, text=score_label_text, font=("Arial", 14))
            score_label.pack(side="top", pady=5)

            score_label_text = f"Temps: {round(score['best_time'], 2)} sec"
            score_label = tk.Label(card_frame, text=score_label_text, font=("Arial", 14))
            score_label.pack(side="top", pady=5)

            if not score['victory']:
                replay_btn = tk.Button(card_frame, text="Reprendre", font=("Arial", 14),
                                       command=lambda seed=score['seed']: self.retake_game(seed))
                replay_btn.pack(side="top", pady=5)

            replay_btn = tk.Button(card_frame, text="Rejouer", font=("Arial", 14),
                                   command=lambda seed=score['seed']: self.replay_game(seed))
            replay_btn.pack(side="top", pady=5)

        self.saved_games_inner_frame.update_idletasks()
        self.saved_games_canvas.config(scrollregion=self.saved_games_canvas.bbox("all"))

        button = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

    def load_scoreboard_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text="Vos meilleurs scores", font=("Arial", 24))
        label.pack(pady=20)

        scores_file = "scores.json"
        if not os.path.exists(scores_file) or os.path.getsize(scores_file) == 0:
            tk.Label(self.root, text="Aucun score disponible.", font=("Arial", 14)).pack(pady=10)
        else:
            with open(scores_file, 'r') as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = []

            difficulties_names = {
                Difficulty.EASY: "Facile",
                Difficulty.MEDIUM: "Moyen",
                Difficulty.HARD: "Difficile"
            }

            best_scores = {Difficulty.EASY: None, Difficulty.MEDIUM: None, Difficulty.HARD: None}

            for score in scores:
                if score['victory']:
                    difficulty = tuple(score['difficulty'])
                    if best_scores[difficulty] is None or score['best_time'] < best_scores[difficulty]['best_time']:
                        best_scores[difficulty] = score

            for difficulty, score in best_scores.items():
                if score:
                    result = "Victoire" if score['victory'] else "Défaite"
                    score_text = f"{difficulties_names[difficulty]} - {result} - Temps : {round(score['best_time'], 2)} sec"
                    score_label = tk.Label(self.root, text=score_text, font=("Arial", 14))
                    score_label.pack(pady=5)
                else:
                    score_label = tk.Label(self.root,
                                           text=f"{difficulties_names[difficulty]} - Aucun score de victoire",
                                           font=("Arial", 14))
                    score_label.pack(pady=5)

        button = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

    def set_game(self, difficulty):
        rows, cols, mines = difficulty
        self.game = Game(rows, cols, mines, difficulty, seed=random.randint(0, 10000))
        self.elapsed_time = 0
        self.load_grid()

    def load_grid(self):
        self.clear_window()

        if not self.timer_label:
            self.timer_label = tk.Label(self.root, text=f"Temps: 0 sec | ⚑ {self.game.flags}", font=("Arial", 14))
            self.timer_label.pack(pady=10)

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        rows, cols, mines = self.game.difficulty
        for row in range(rows):
            for col in range(cols):
                btn = tk.Button(self.frame, width=4, height=3, command=lambda r=row, c=col: self.click_case(r, c), font=("Arial", 14))
                btn.grid(row=row, column=col)
                self.game.grid[row][col].button = btn
                btn.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(r, c))

        self.update_timer()

    def update_timer(self):
        if self.timer_label and self.game and self.game.start_time > 0 and self.game.is_running:
            self.elapsed_time = time.time() - self.game.start_time
            formatted_time = round(self.elapsed_time, 2)
            self.timer_label.config(text=f"Temps: {formatted_time} sec | ⚑ {self.game.flags}")
        self.root.after(100, self.update_timer)

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
        if self.game.grid[row][col].is_flagged:
            self.game.grid[row][col].toggle_flag()
            self.game.flags += 1
        else:
            if self.game.flags > 0:
                self.game.grid[row][col].toggle_flag()
                self.game.flags -= 1

        if self.check_victory():
            self.victory()

    def check_victory(self):
        mines_flagged = sum(1 for row in self.game.grid for case in row if case.is_mine and case.is_flagged)
        cases_revealed = sum(1 for row in self.game.grid for case in row if case.is_revealed and not case.is_mine)
        total_cases = self.game.rows * self.game.cols
        return mines_flagged == self.game.mines and cases_revealed == total_cases - self.game.mines

    def victory(self):
        self.game.is_running = False
        self.save_game(True)

        self.clear_window()
        self.timer_label = None
        label = tk.Label(self.root, text="Félicitations, vous avez gagné !", font=("Arial", 24))
        label.pack(pady=20)

        formatted_time = round(self.elapsed_time, 2)
        timer_label = tk.Label(self.root, text=f"Votre Temps: {formatted_time} sec", font=("Arial", 14))
        timer_label.pack(pady=20)
        self.elapsed_time = 0

        replay_btn = tk.Button(self.root, text="Rejouer", font=("Arial", 14),
                               command=lambda: self.replay_game(self.game.seed))
        replay_btn.pack(pady=10)

        button = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

    def game_over(self):
        self.game.is_running = False
        self.save_game(False)

        for row in range(self.game.rows):
            for col in range(self.game.cols):
                if self.game.grid[row][col].is_flagged:
                    self.game.grid[row][col].is_flagged = False
                self.game.grid[row][col].reveal()
        self.root.after(2000, self.show_defeat_screen)

    def show_defeat_screen(self):
        self.clear_window()
        self.timer_label = None
        label = tk.Label(self.root, text="Dommage, vous avez perdu.", font=("Arial", 24))
        label.pack(pady=20)

        formatted_time = round(self.elapsed_time, 2)
        timer_label = tk.Label(self.root, text=f"Votre Temps: {formatted_time} sec", font=("Arial", 14))
        timer_label.pack(pady=20)
        self.elapsed_time = 0

        replay_btn = tk.Button(self.root, text="Reprendre", font=("Arial", 14),
                               command=lambda: self.retake_game(self.game.seed))
        replay_btn.pack(pady=5)

        replay_btn = tk.Button(self.root, text="Rejouer", font=("Arial", 14),
                               command=lambda: self.replay_game(self.game.seed))
        replay_btn.pack(pady=5)

        button = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14), command=self.load_main_menu)
        button.pack(pady=10)

    def save_game(self, victory):
        scores_file = "scores.json"

        def case_to_dict(case):
            return {
                "is_mine": case.is_mine,
                "is_revealed": case.is_revealed,
                "is_flagged": case.is_flagged,
                "adjacent_mines": case.adjacent_mines,
            }

        grid_serializable = [
            [case_to_dict(cell) for cell in row] for row in self.game.grid
        ]

        score_data = {
            "seed": self.game.seed,
            "time": self.elapsed_time,
            "difficulty": self.game.difficulty,
            "first_position": self.game.first_position,
            "grid": grid_serializable,
        }

        if not self.game.is_saved:
            score_data["victory"] = victory
            score_data["best_time"] = self.elapsed_time

        if not os.path.exists(scores_file) or os.path.getsize(scores_file) == 0:
            with open(scores_file, 'w') as f:
                json.dump([score_data], f)
        else:
            with open(scores_file, 'r+') as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = []

                for i, score in enumerate(scores):
                    if score['seed'] == self.game.seed:
                        if victory:
                            score_data["victory"] = True
                            if score['victory']:
                                if self.elapsed_time < score['best_time']:
                                    score_data["best_time"] = self.elapsed_time
                                else:
                                    score_data["best_time"] = self.game.best_time
                            else:
                                score_data["best_time"] = self.elapsed_time
                        else:
                            if score['victory']:
                                score_data["victory"] = True
                                score_data["best_time"] = self.game.best_time
                            else:
                                score_data["victory"] = False
                                score_data["best_time"] = self.elapsed_time
                        scores[i] = score_data
                        break
                else:
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
            self.game.is_saved = True
            self.game.start_time = time.time()
            self.game.best_time = saved_score['best_time']
            self.load_grid()

            for r in range(len(saved_score['grid'])):
                for c in range(len(saved_score['grid'][r])):
                    self.game.grid[r][c].is_mine = saved_score['grid'][r][c]["is_mine"]
                    self.game.grid[r][c].adjacent_mines = saved_score['grid'][r][c]["adjacent_mines"]

            r, c = self.game.first_position
            self.click_case(r, c)

    def retake_game(self, seed):
        saved_score = self.get_saved_score_by_seed(seed)
        if saved_score:
            difficulty = saved_score['difficulty']
            rows, cols, mines = difficulty

            self.game = Game(rows, cols, mines, difficulty, seed=seed)
            self.game.first_position = saved_score['first_position']
            self.game.is_saved = True
            self.game.start_time = time.time() - saved_score['time']
            self.game.best_time = saved_score['best_time']
            self.load_grid()

            for r in range(rows):
                for c in range(cols):
                    case = self.game.grid[r][c]
                    saved_case = saved_score['grid'][r][c]
                    case.is_mine = saved_case["is_mine"]
                    case.is_flagged = saved_case["is_flagged"]
                    case.is_revealed = saved_case["is_revealed"]
                    case.adjacent_mines = saved_case["adjacent_mines"]
                    if case.is_mine:
                        case.is_revealed = False
                    if not case.is_flagged and case.is_revealed:
                        case.is_revealed = False
                        case.reveal()
                    if case.is_flagged:
                        case.is_flagged = False
                        case.toggle_flag()
                        self.game.flags -= 1

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