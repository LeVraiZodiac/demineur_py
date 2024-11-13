import tkinter as tk
import random
import json
import os
import time

from PIL import Image, ImageTk


from Game import Game, Difficulty

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        self.root.geometry("1536x864")
        self.root.configure(bg="orange")
        self.game = None
        self.timer_label = None
        self.elapsed_time = 0
        self.load_main_menu()

    def set_background(self, image_path):
        background_image = Image.open(image_path)
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.root, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.photo = background_photo

    def load_main_menu(self):
        self.clear_window()
        self.set_background("image/background.jpg")

        # Label "Démineur" avec un effet bois
        self.label = tk.Label(
            self.root, text="Démineur", font=("Impact", 44), fg="white", bg="#D2691E",
            relief="raised", bd=25
        )
        self.label.pack(pady=50)

        # Bouton "Nouvelle partie" avec un style bois
        new_game_button = tk.Button(
            self.root, text="Nouvelle partie", font=("Impact", 18), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=self.load_difficulty_menu
        )
        new_game_button.pack(pady=(100, 20))

        # Bouton "Parties Sauvegardées" avec style bois
        saved_games_button = tk.Button(
            self.root, text="Parties Sauvegardées", font=("Impact", 18), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=self.load_saved_games_menu
        )
        saved_games_button.pack(pady=(5, 20))

        # Bouton "Fermer" avec style bois
        close_button = tk.Button(
            self.root, text="Fermer", font=("Impact", 18), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=self.root.destroy
        )
        close_button.pack(pady=(5, 100))

        # Charger les scores directement dans le menu principal
        self.display_scores()

    def display_scores(self):
        scores_file = "scores.json"

        # Si aucun score n'est disponible
        if not os.path.exists(scores_file) or os.path.getsize(scores_file) == 0:
            score_label = tk.Label(
                self.root, text="Parties Sauvegardées", font=("Impact", 44), bg="#D2691E", fg="white",
                relief="raised", bd=25
            )
            score_label.pack(pady=10)
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

            # Trouver les meilleurs scores
            for score in scores:
                if score['victory']:
                    difficulty = tuple(score['difficulty'])
                    if best_scores[difficulty] is None or score['best_time'] < best_scores[difficulty]['best_time']:
                        best_scores[difficulty] = score

            # Créer un cadre (Frame) pour organiser les éléments horizontalement
            scores_frame = tk.Frame(self.root, bg="orange", relief="raised", bd=25)
            scores_frame.pack(pady=10, padx=10, fill='x')  # Remplir horizontalement

            # Dictionnaire des couleurs pour chaque difficulté
            difficulty_colors = {
                Difficulty.EASY: "#cd7f32",  # Bronze
                Difficulty.MEDIUM: "#c0c0c0",  # Argent
                Difficulty.HARD: "#ffd700",  # Or
            }

            # Afficher les meilleurs scores horizontalement avec un espace visible entre les difficultés
            for difficulty, score in best_scores.items():
                # Créer un frame pour chaque difficulté
                difficulty_frame = tk.Frame(scores_frame, bg=difficulty_colors[difficulty], bd=5, relief="solid")
                difficulty_frame.pack(side="left", padx=10, pady=10, expand=True)

                # Centrer les éléments dans le cadre
                difficulty_label = tk.Label(difficulty_frame, text=difficulties_names[difficulty],
                                            font=("Arial", 18, 'bold'), bg=difficulty_colors[difficulty],
                                            anchor="center")
                difficulty_label.pack()

                # Afficher le score ou le message en fonction des données
                if score:
                    score_text = f"Records de {score['player']} avec un temps de {round(score['best_time'], 2)} sec"
                    score_label = tk.Label(difficulty_frame, text=score_text, font=("Arial", 14),
                                           bg=difficulty_colors[difficulty], anchor="center")
                    score_label.pack()
                else:
                    no_win_text = "Encore aucune victoire dans cette difficulté"
                    no_win_label = tk.Label(difficulty_frame, text=no_win_text, font=("Arial", 14),
                                            bg=difficulty_colors[difficulty], anchor="center")
                    no_win_label.pack()

                # Ajouter un espace vide (pour voir l'arrière-plan) entre chaque difficulté
                spacer = tk.Label(difficulty_frame, text="", bg=difficulty_colors[difficulty], width=5)
                spacer.pack(side="left")

    def load_difficulty_menu(self):
        self.clear_window()
        self.set_background("image/background.jpg")

        # Label "Choisir la difficulté" avec effet bois
        label = tk.Label(
            self.root, text="Choisir la difficulté", font=("Impact", 44), bg="#D2691E", fg="white",
            relief="raised", bd=25
        )
        label.pack(pady=70)  # Espacement pour séparer le label des boutons

        # Bouton "Facile" avec style bois
        btn_easy = tk.Button(
            self.root, text="Facile", font=("Impact", 18), bg="#8B4513", fg="white", width=20,
            height=2, relief="raised", bd=5, command=lambda: self.set_game(Difficulty.EASY)
        )
        btn_easy.pack(pady=(70, 20))

        # Bouton "Moyen" avec style bois
        btn_medium = tk.Button(
            self.root, text="Moyen", font=("Impact", 18), bg="#8B4513", fg="white", width=20,
            height=2, relief="raised", bd=5, command=lambda: self.set_game(Difficulty.MEDIUM)
        )
        btn_medium.pack(pady=(10, 20))

        # Bouton "Difficile" avec style bois
        btn_hard = tk.Button(
            self.root, text="Difficile", font=("Impact", 18), bg="#8B4513", fg="white", width=20,
            height=2, relief="raised", bd=5, command=lambda: self.set_game(Difficulty.HARD)
        )
        btn_hard.pack(pady=(10, 70))

        # Bouton de retour au menu principal avec style bois
        back_button = tk.Button(
            self.root, text="Retour au Menu Principal", font=("Impact", 14), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=self.load_main_menu
        )
        back_button.pack(pady=20)

    def load_saved_games_menu(self):
        self.clear_window()
        self.set_background("image/background.jpg")

        # Titre du menu avec effet bois
        label = tk.Label(
            self.root, text="Parties Sauvegardées", font=("Impact", 44), bg="#D2691E", fg="white",
            relief="raised", bd=25
        )
        label.pack(pady=30)

        # Vérification de l'existence de sauvegardes
        scores_file = "scores.json"
        if not os.path.exists(scores_file) or os.path.getsize(scores_file) == 0:
            tk.Label(self.root, text="Aucune partie sauvegardée.", font=("Arial", 14), bg="#D2691E", fg="white").pack(
                pady=10
            )
            button = tk.Button(
                self.root, text="Retour au Menu Principal", font=("Arial", 14), bg="#8B4513", fg="white",
                relief="raised", bd=5, command=self.load_main_menu
            )
            button.pack(pady=20)
            return

        # Chargement des scores
        with open(scores_file, 'r') as f:
            scores = json.load(f)

        # Recherche par seed avec un cadre couleur bois
        search_frame = tk.Frame(self.root, bg="#A0522D", relief="sunken", bd=5, padx=5, pady=5)
        search_frame.pack(pady=1, padx=600, fill="x")

        search_label = tk.Label(search_frame, text="Rechercher par seed :", font=("Arial", 14), bg="#A0522D",
                                fg="white")
        search_label.pack(side="left")

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 14))
        search_entry.pack(side="left", padx=10, fill="x", expand=True)
        search_var.trace("w",
                         lambda name, index, mode, sv=search_var: self.update_saved_games_display(scores, sv.get()))

        # Cadre principal pour les parties sauvegardées avec effet bois
        self.saved_games_frame = tk.Frame(self.root, bg="#8B4513", relief="raised", bd=25, padx=20, pady=20)
        self.saved_games_frame.pack(fill="both", expand=True, pady=5, padx=20)

        # Canvas pour les parties sauvegardées
        self.saved_games_canvas = tk.Canvas(self.saved_games_frame, bg="#D2B48C", highlightthickness=0)
        self.saved_games_canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar (cachée si inutile)
        self.saved_games_scrollbar = tk.Scrollbar(
            self.saved_games_frame, orient="vertical", command=self.saved_games_canvas.yview
        )
        self.saved_games_canvas.config(yscrollcommand=self.saved_games_scrollbar.set)
        self.saved_games_canvas.bind("<Configure>", lambda e: self.saved_games_scrollbar.pack_forget() if
        self.saved_games_canvas.bbox("all")[3] <= e.height else
        self.saved_games_scrollbar.pack(side="right", fill="y"))

        # Inner frame pour l'affichage des sauvegardes
        self.saved_games_inner_frame = tk.Frame(self.saved_games_canvas, bg="#D2B48C")
        self.saved_games_canvas.create_window((0, 0), window=self.saved_games_inner_frame, anchor="n")

        # Affichage initial des parties sauvegardées
        self.update_saved_games_display(scores, "")

        # Bouton pour retourner au menu principal avec style bois
        back_button = tk.Button(
            self.root, text="Retour au Menu Principal", font=("Arial", 14), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=self.load_main_menu
        )
        back_button.pack(pady=20)

    def update_saved_games_display(self, scores, search_text):
        for widget in self.saved_games_inner_frame.winfo_children():
            widget.destroy()

        difficulties_names = {
            Difficulty.EASY: "Facile",
            Difficulty.MEDIUM: "Moyen",
            Difficulty.HARD: "Difficile"
        }

        row = 0
        column = 1  # Commence à 1 pour laisser la première colonne vide

        # Configurer trois colonnes principales au centre et deux colonnes vides pour le centrage
        for col in range(5):
            self.saved_games_inner_frame.grid_columnconfigure(col, weight=1)

        for i, score in enumerate(scores):
            if search_text.lower() not in str(score['seed']).lower():
                continue

            # Appliquer le style de la victory_frame pour chaque carte de sauvegarde
            card_frame = tk.Frame(self.saved_games_inner_frame, bg="orange", relief="raised", bd=10, padx=20, pady=20)
            card_frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

            # Informations de sauvegarde formatées
            difficulty = tuple(score['difficulty'])
            result = "Victoire" if score['victory'] else "Défaite"

            score_label_text = f"Seed: {score['seed']}"
            score_label = tk.Label(card_frame, text=score_label_text, font=("Arial", 10), bg="orange", fg="white")
            score_label.pack(side="top", pady=2)

            difficulty_text = f"Difficulté: {difficulties_names[difficulty]} - {result}"
            difficulty_label = tk.Label(card_frame, text=difficulty_text, font=("Arial", 10), bg="orange", fg="white")
            difficulty_label.pack(side="top", pady=2)

            player_text = f"Joueur: {score['player']}"
            player_label = tk.Label(card_frame, text=player_text, font=("Arial", 10), bg="orange", fg="white")
            player_label.pack(side="top", pady=2)

            time_text = f"Temps: {round(score['best_time'], 2)} sec"
            time_label = tk.Label(card_frame, text=time_text, font=("Arial", 10), bg="orange", fg="white")
            time_label.pack(side="top", pady=2)

            # Boutons pour les actions de la sauvegarde
            if not score['victory']:
                replay_btn = tk.Button(card_frame, text="Reprendre", font=("Arial", 10), bg="brown", fg="white",
                                       command=lambda seed=score['seed'], player=score['player']: self.retake_game(seed,
                                                                                                                   player))
                replay_btn.pack(side="top", pady=2)

            replay_btn = tk.Button(card_frame, text="Rejouer", font=("Arial", 10), bg="brown", fg="white",
                                   command=lambda seed=score['seed'], player=score['player']: self.replay_game(seed,
                                                                                                               player))
            replay_btn.pack(side="top", pady=2)

            if score['player'] is not None:
                challenge_btn = tk.Button(card_frame, text="Défier", font=("Arial", 10), bg="brown", fg="white",
                                          command=lambda seed=score['seed'],
                                                         player=score['player']: self.challenge_game(seed, player))
                challenge_btn.pack(side="top", pady=2)

            column += 1
            if column > 6:
                column = 1
                row += 1

        self.saved_games_inner_frame.update_idletasks()
        self.saved_games_canvas.config(scrollregion=self.saved_games_canvas.bbox("all"))

    def set_game(self, difficulty):
        rows, cols, mines = difficulty
        self.game = Game(rows, cols, mines, difficulty, seed=random.randint(0, 10000))
        self.elapsed_time = 0
        self.load_grid()

    def load_grid(self):
        self.clear_window()
        self.set_background("image/background.jpg")

        # Création de l'étiquette de minuterie
        if not self.timer_label:
            self.timer_label = tk.Label(
                self.root,
                text=f"Temps: 0 sec | ⚑ {self.game.flags}",
                font=("Impact", 24),
                bg="gray",
                fg="white",
                relief="raised",
                bd=5
            )
            self.timer_label.pack(pady=10)

        # Création de la frame avec un style bois
        self.frame = tk.Frame(
            self.root,
            bg="#8B4513",  # Couleur marron clair pour un effet bois
            bd=10,  # Bordure de 10 pixels
            relief="ridge"  # Bordure style crête pour un effet sculpté
        )
        self.frame.pack(pady=5)  # Espacement vertical pour bien encadrer la grille

        # Création de la grille de boutons
        rows, cols, mines = self.game.difficulty
        for row in range(rows):
            for col in range(cols):
                btn = tk.Button(
                    self.frame,
                    width=2,
                    height=1,
                    command=lambda r=row, c=col: self.click_case(r, c),
                    font=("Arial", 14),
                    bg="#D2B48C",  # Couleur sable clair pour les boutons, rappelant du bois clair
                    fg="white",  # Texte blanc
                    relief="raised",  # Style surélevé pour l'effet de relief
                    bd=3  # Bordure légère pour une touche de profondeur
                )
                btn.grid(row=row, column=col, padx=1, pady=1)  # Espacement entre les boutons pour simuler des planches
                self.game.grid[row][col].button = btn
                btn.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(r, c))

        # Démarre le minuteur
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
        self.timer_label = None

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
        if not self.game.grid[row][col].is_revealed:
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
        self.clear_window()
        self.set_background("image/background.jpg")
        self.timer_label = None

        # Création de la frame pour contenir les messages de victoire et l'entrée de pseudo
        victory_frame = tk.Frame(self.root, bg="orange", relief="raised", bd=25, padx=20, pady=20)
        victory_frame.pack(pady=20) # Padding extérieur pour espacer la frame du reste

        # Message de félicitations
        label = tk.Label(victory_frame, text="Félicitations, vous avez gagné !", font=("Arial", 24), fg="white",
                         bg="orange")
        label.pack(pady=10)

        # Afficher le temps écoulé
        formatted_time = round(self.elapsed_time, 2)
        timer_label = tk.Label(victory_frame, text=f"Votre Temps: {formatted_time} sec", font=("Arial", 14), fg="white",
                               bg="orange")
        timer_label.pack(pady=10)

        # Champ d'entrée pour le pseudo
        pseudo_label = tk.Label(victory_frame, text="Entrez votre pseudo :", font=("Arial", 14), fg="white",
                                bg="orange")
        pseudo_label.pack(pady=10)

        pseudo_entry = tk.Entry(victory_frame, font=("Arial", 14))
        pseudo_entry.pack(pady=10)

        # Fonction pour sauvegarder le pseudo et terminer la partie
        def save_pseudo():
            self.game.player = pseudo_entry.get() or "Joueur"  # Utiliser "Joueur" par défaut si le champ est vide
            self.save_game(True)
            self.elapsed_time = 0  # Réinitialiser le temps après la sauvegarde
            # Désactiver le champ d'entrée et le bouton après l'enregistrement
            pseudo_entry.config(state="disabled")
            save_btn.config(state="disabled")

        # Bouton d'enregistrement
        save_btn = tk.Button(victory_frame, text="Enregistrer le pseudo", font=("Arial", 14), command=save_pseudo,
                             fg="white", bg="brown")
        save_btn.pack(pady=10)

        # Bouton pour rejouer
        replay_btn = tk.Button(self.root, text="Rejouer", font=("Arial", 14),
                               command=lambda: self.replay_game(self.game.seed, self.game.player), fg="white",
                               bg="brown")
        replay_btn.pack(pady=10)

        # Bouton pour retourner au menu principal
        main_menu_btn = tk.Button(self.root, text="Retour au Menu Principal", font=("Arial", 14),
                                  command=self.load_main_menu, fg="white", bg="brown")
        main_menu_btn.pack(pady=10)

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
        self.set_background("image/background.jpg")

        # Frame de défaite avec couleur grise et effet bois sur la bordure
        defeat_frame = tk.Frame(self.root, bg="grey", relief="raised", bd=25, padx=20, pady=20)
        defeat_frame.pack(pady=20)  # Espacement extérieur pour séparer la frame

        # Label principal de défaite en blanc sur fond gris
        label = tk.Label(defeat_frame, text="Dommage, vous avez perdu.", font=("Arial", 24), bg="grey", fg="white")
        label.pack(pady=50)

        # Affichage du temps écoulé
        formatted_time = round(self.elapsed_time, 2)
        timer_label = tk.Label(defeat_frame, text=f"Votre Temps: {formatted_time} sec", font=("Arial", 14), bg="grey",
                               fg="white")
        timer_label.pack(pady=10)
        self.elapsed_time = 0

        # Bouton "Reprendre" avec effet bois
        replay_btn = tk.Button(
            self.root, text="Reprendre", font=("Arial", 14), bg="#8B4513", fg="white", relief="raised", bd=5,
            command=lambda: self.retake_game(self.game.seed, self.game.player)
        )
        replay_btn.pack(pady=5)

        # Bouton "Rejouer" avec effet bois
        replay_btn = tk.Button(
            self.root, text="Rejouer", font=("Arial", 14), bg="#8B4513", fg="white", relief="raised", bd=5,
            command=lambda: self.replay_game(self.game.seed, self.game.player)
        )
        replay_btn.pack(pady=5)

        # Bouton "Retour au Menu Principal" avec effet bois
        back_button = tk.Button(
            self.root, text="Retour au Menu Principal", font=("Arial", 14), bg="#8B4513", fg="white", relief="raised",
            bd=5,
            command=self.load_main_menu
        )
        back_button.pack(pady=10)

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
            "player": self.game.player,
            "time": self.elapsed_time,
            "difficulty": self.game.difficulty,
            "first_position": self.game.first_position,
            "grid": grid_serializable,
        }

        if not self.game.is_saved:
            score_data["victory"] = victory
            score_data["best_time"] = self.elapsed_time

        # Créer le fichier JSON s'il n'existe pas
        if not os.path.exists(scores_file):
            with open(scores_file, 'w') as f:
                json.dump([score_data], f)
        else:
            with open(scores_file, 'r+') as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = []

                for i, score in enumerate(scores):
                    if score['seed'] == self.game.seed and (
                            score['player'] == self.game.player or score['player'] is None):
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
                    score_data["victory"] = victory
                    score_data["best_time"] = self.elapsed_time
                    scores.append(score_data)

                f.seek(0)
                json.dump(scores, f)
                f.truncate()

    def challenge_game(self, seed, player):
        saved_score = self.get_saved_score_by_seed(seed, player)
        if saved_score:
            difficulty = saved_score['difficulty']
            rows, cols, mines = difficulty

            self.game = Game(rows, cols, mines, difficulty, seed=seed)
            self.game.first_position = saved_score['first_position']
            self.game.start_time = time.time()
            self.load_grid()

            for r in range(len(saved_score['grid'])):
                for c in range(len(saved_score['grid'][r])):
                    self.game.grid[r][c].is_mine = saved_score['grid'][r][c]["is_mine"]
                    self.game.grid[r][c].adjacent_mines = saved_score['grid'][r][c]["adjacent_mines"]

            r, c = self.game.first_position
            self.click_case(r, c)

    def replay_game(self, seed, player):
        saved_score = self.get_saved_score_by_seed(seed, player)
        if saved_score:
            difficulty = saved_score['difficulty']
            rows, cols, mines = difficulty

            self.game = Game(rows, cols, mines, difficulty, seed=seed)
            self.game.first_position = saved_score['first_position']
            self.game.is_saved = True
            self.game.player = saved_score['player']
            self.game.start_time = time.time()
            self.game.best_time = saved_score['best_time']
            self.load_grid()

            for r in range(len(saved_score['grid'])):
                for c in range(len(saved_score['grid'][r])):
                    self.game.grid[r][c].is_mine = saved_score['grid'][r][c]["is_mine"]
                    self.game.grid[r][c].adjacent_mines = saved_score['grid'][r][c]["adjacent_mines"]

            r, c = self.game.first_position
            self.click_case(r, c)

    def retake_game(self, seed, player):
        saved_score = self.get_saved_score_by_seed(seed, player)
        if saved_score:
            difficulty = saved_score['difficulty']
            rows, cols, mines = difficulty

            self.game = Game(rows, cols, mines, difficulty, seed=seed)
            self.game.first_position = saved_score['first_position']
            self.game.is_saved = True
            self.game.player = saved_score['player']
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

    def get_saved_score_by_seed(self, seed, player):
        scores_file = "scores.json"
        if not os.path.exists(scores_file):
            return None
        with open(scores_file, 'r') as f:
            scores = json.load(f)
            for score in scores:
                if score['seed'] == seed and (score['player'] == player or score['player'] is None):
                    return score
        return None

if __name__ == "__main__":
    root = tk.Tk()
    jeu = Minesweeper(root)
    root.mainloop()