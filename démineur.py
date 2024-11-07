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

    def reveal(self):
        if not self.is_flagged:
            self.is_revealed = True
            return not self.is_mine

class Grille:
    def __init__(self, rows, cols, mines, seed=None):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[Case(row, col) for col in range(cols)] for row in range(rows)]
        self.seed = seed
        if seed is not None:
            random.seed(seed)  # Utilisation du seed pour reproduire la même grille
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
        self.previous_start = None
        self.scores_file = "scores.json"
        self.start_time = None
        self.seed = None
        self.create_menu()

    def create_menu(self):
        """ Affiche le menu principal. """
        self.clear_window()
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
        """ Définit la difficulté et démarre une nouvelle partie. """
        self.difficulty = difficulty
        self.setup_game()

    def setup_game(self):
        """ Initialise la grille de jeu en fonction de la difficulté sélectionnée. """
        if self.difficulty == "Facile":
            rows, cols, mines = 9, 9, 10
        elif self.difficulty == "Moyen":
            rows, cols, mines = 16, 16, 40
        else:
            rows, cols, mines = 24, 24, 99

        self.seed = random.randint(0, 10000)  # Générer un seed aléatoire pour la grille
        self.grid = Grille(rows, cols, mines, seed=self.seed)
        self.start_time = time.time()  # Commence le chronométrage de la partie
        self.create_widgets(rows, cols)

    def create_widgets(self, rows, cols):
        """ Crée les boutons de la grille de jeu pour chaque case. """
        self.clear_window()
        for row in range(rows):
            for col in range(cols):
                btn = tk.Button(self.root, width=2, height=1, command=lambda r=row, c=col: self.click_case(r, c))
                btn.grid(row=row, column=col)
                self.grid.grid[row][col].button = btn
                btn.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(r, c))

    def clear_window(self):
        """ Efface tous les widgets de la fenêtre pour afficher une nouvelle page. """
        for widget in self.root.winfo_children():
            widget.destroy()

    def click_case(self, row, col):
        """ Gère le clic gauche sur une case pour la révéler. """
        case = self.grid.grid[row][col]
        if case.is_flagged:
            return

        if self.previous_start is None:
            self.previous_start = (row, col)
            if case.is_mine:
                self.grid.grid[row][col].is_mine = False

        if case.reveal():
            self.update_button(row, col)
            if case.adjacent_mines == 0:
                for adj in self.grid.get_adjacent_cases(row, col):
                    self.update_button(adj.row, adj.col)
        else:
            self.game_over()

        if self.check_victory():
            self.victory()

    def update_button(self, row, col):
        """ Met à jour l'affichage de la case après l'avoir révélée. """
        case = self.grid.grid[row][col]
        btn = case.button
        if case.is_mine:
            btn.config(text="*", bg="red")
        else:
            btn.config(text=str(case.adjacent_mines) if case.adjacent_mines > 0 else "", bg="light grey")
        btn.config(state="disabled")

    def toggle_flag(self, row, col):
        """ Gère le clic droit pour placer un drapeau sur une case. """
        case = self.grid.grid[row][col]
        case.toggle_flag()
        btn = case.button
        btn.config(text="⚑" if case.is_flagged else "", fg="blue" if case.is_flagged else "black")

    def game_over(self):
        """ Affiche toutes les mines et redirige vers l'écran de défaite. """
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                case = self.grid.grid[row][col]
                if case.is_mine:
                    case.button.config(text="*", bg="red")
        self.show_defeat_screen()

    def check_victory(self):
        """ Vérifie si le joueur a gagné la partie. """
        for row in self.grid.grid:
            for case in row:
                if not case.is_mine and not case.is_revealed:
                    return False
        return True

    def victory(self):
        """ Affiche l'écran de victoire et sauvegarde le score. """
        self.clear_window()
        label = tk.Label(self.root, text="Félicitations, vous avez gagné !", font=("Arial", 16))
        label.pack(pady=20)

        replay_btn = tk.Button(self.root, text="Rejouer", font=("Arial", 12), command=self.setup_game)
        replay_btn.pack(pady=5)

        main_menu_btn = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 12), command=self.create_menu)
        main_menu_btn.pack(pady=5)

        end_time = time.time()
        elapsed_time = end_time - self.start_time
        self.save_score(True, elapsed_time)

    def show_defeat_screen(self):
        """ Affiche l'écran de défaite et permet de rejouer ou de retourner au menu principal. """
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
        """ Sauvegarde le score de la partie dans un fichier JSON. """
        score_data = {
            "difficulty": self.difficulty,
            "victory": victory,
            "time": elapsed_time,
            "seed": self.seed,
            "timestamp": time.ctime()
        }

        if not os.path.exists(self.scores_file):
            with open(self.scores_file, 'w') as f:
                json.dump([score_data], f)
        else:
            with open(self.scores_file, 'r+') as f:
                scores = json.load(f)
                scores.append(score_data)
                f.seek(0)
                json.dump(scores, f)

    def show_saved_games(self):
        """ Affiche les parties sauvegardées et permet de rejouer avec un seed spécifique. """
        self.clear_window()
        label = tk.Label(self.root, text="Parties Sauvegardées", font=("Arial", 14))
        label.pack(pady=20)

        if not os.path.exists(self.scores_file):
            tk.Label(self.root, text="Aucune partie sauvegardée.").pack()
            return

        with open(self.scores_file, 'r') as f:
            scores = json.load(f)

        for i, score in enumerate(scores):
            result = "Victoire" if score['victory'] else "Défaite"
            score_label = f"Partie {i + 1} - Difficulté: {score['difficulty']} - {result} - Temps: {round(score['time'], 2)} sec"
            tk.Label(self.root, text=score_label).pack()

            replay_btn = tk.Button(self.root, text="Rejouer", command=lambda seed=score['seed']: self.replay_game(seed))
            replay_btn.pack(pady=5)

        back_btn = tk.Button(self.root, text="Retour", command=self.create_menu)
        back_btn.pack(pady=10)

    def get_saved_score_by_seed(self, seed):
        """ Récupère les informations d'une partie sauvegardée à partir du seed. """
        if not os.path.exists(self.scores_file):
            return None
        with open(self.scores_file, 'r') as f:
            scores = json.load(f)
            for score in scores:
                if score['seed'] == seed:
                    return score
        return None

    def replay_game(self, seed):
        """ Rejoue une partie en utilisant un seed spécifique. """
        self.seed = seed  # Utilisation du seed sauvegardé
        # Récupérer la difficulté de la partie sauvegardée
        # Vous pouvez éventuellement récupérer cette information depuis le fichier JSON des scores
        saved_score = self.get_saved_score_by_seed(seed)
        if saved_score:
            difficulty = saved_score['difficulty']
            # Initialiser la grille avec la difficulté correspondante
            if difficulty == "Facile":
                rows, cols, mines = 9, 9, 10
            elif difficulty == "Moyen":
                rows, cols, mines = 16, 16, 40
            else:
                rows, cols, mines = 24, 24, 99

            self.grid = Grille(rows, cols, mines, seed=self.seed)
            self.start_time = time.time()  # Redémarrer le chronomètre
            self.create_widgets(rows, cols)


if __name__ == "__main__":
    root = tk.Tk()
    jeu = Demineur(root)
    root.mainloop()
