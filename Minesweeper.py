import tkinter as tk
import random
import json
import os
import time

from PIL import Image, ImageTk
from Game import Game
from Difficulty import Difficulty


class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        self.root.geometry("1745x982")
        self.root.configure(bg="orange")
        self.game = None
        self.timer_label = None
        self.elapsed_time = 0
        self.load_main_menu()

    # Set the background image
    def set_background(self, image_path):
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        background_image = Image.open(image_path)
        background_image = background_image.resize((window_width, window_height), Image.LANCZOS)

        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.root, image=background_photo)

        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.photo = background_photo

    def load_main_menu(self):
        # Load the main menu with options
        self.clear_window()
        self.set_background("image/background.jpg")

        # Title label
        self.label = tk.Label(
            self.root, text="Démineur", font=("Impact", 44), fg="white", bg="#D2691E",
            relief="raised", bd=25
        )
        self.label.pack(pady=50)

        # Buttons for new game, saved games, and closing
        new_game_button = tk.Button(
            self.root, text="Nouvelle partie", font=("Impact", 18), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=self.load_difficulty_menu
        )
        new_game_button.pack(pady=(100, 20))

        saved_games_button = tk.Button(
            self.root, text="Parties Sauvegardées", font=("Impact", 18), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=self.load_saved_games_menu
        )
        saved_games_button.pack(pady=(5, 20))

        close_button = tk.Button(
            self.root, text="Fermer", font=("Impact", 18), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=self.root.destroy
        )
        close_button.pack(pady=(5, 180))

        # Display saved scores
        self.display_scores()

    def display_scores(self):
        # Load and display the best scores from saved games
        scores_file = "scores.json"

        # Frame to hold the score elements
        scores_frame = tk.Frame(self.root, bg="orange", relief="raised", bd=25)
        scores_frame.pack(pady=10, padx=10, fill='x')

        # Colors for each difficulty level
        difficulty_colors = {
            Difficulty.EASY: "#cd7f32",  # Bronze
            Difficulty.MEDIUM: "#c0c0c0",  # Silver
            Difficulty.HARD: "#ffd700",  # Gold
        }

        difficulties_names = {
            Difficulty.EASY: "Facile",
            Difficulty.MEDIUM: "Moyen",
            Difficulty.HARD: "Difficile"
        }

        best_scores = {Difficulty.EASY: None, Difficulty.MEDIUM: None, Difficulty.HARD: None}

        if not os.path.exists(scores_file) or os.path.getsize(scores_file) == 0:
            for difficulty, score in best_scores.items():
                difficulty_frame = tk.Frame(scores_frame, bg=difficulty_colors[difficulty], bd=5, relief="solid")
                difficulty_frame.pack(side="left", padx=10, pady=10, expand=True)

                difficulty_label = tk.Label(difficulty_frame, text=difficulties_names[difficulty],
                                            font=("Arial", 18, 'bold'), bg=difficulty_colors[difficulty],
                                            anchor="center")
                difficulty_label.pack()
        else:
            with open(scores_file, 'r') as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = []

            # Find the best scores for each difficulty
            for score in scores:
                if score['victory']:
                    difficulty = tuple(score['difficulty'])
                    if best_scores[difficulty] is None or score['best_time'] < best_scores[difficulty]['best_time']:
                        best_scores[difficulty] = score


            # Display best scores horizontally for each difficulty
            for difficulty, score in best_scores.items():
                difficulty_frame = tk.Frame(scores_frame, bg=difficulty_colors[difficulty], bd=5, relief="solid")
                difficulty_frame.pack(side="left", padx=10, pady=10, expand=True)

                difficulty_label = tk.Label(difficulty_frame, text=difficulties_names[difficulty],
                                            font=("Arial", 18, 'bold'), bg=difficulty_colors[difficulty],
                                            anchor="center")
                difficulty_label.pack()

                if score:
                    score_text = f"Records de {score['player']}"
                    score_label = tk.Label(difficulty_frame, text=score_text, font=("Arial", 14),
                                           bg=difficulty_colors[difficulty], anchor="center")
                    score_label.pack()
                    score_text = f"Avec un temps de {round(score['best_time'], 2)} sec sur la seed {score['seed']}"
                    score_label = tk.Label(difficulty_frame, text=score_text, font=("Arial", 14),
                                           bg=difficulty_colors[difficulty], anchor="center")
                    score_label.pack()
                    back_button = tk.Button(
                        difficulty_frame, text="Défier", font=("Arial", 14), bg="#8B4513", fg="white",
                        relief="raised", bd=5, command=lambda seed=score['seed'], player=score['player']:
                        self.challenge_game(seed, player))
                    back_button.pack(pady=2)
                else:
                    no_win_text = "Encore aucune victoire dans cette difficulté"
                    no_win_label = tk.Label(difficulty_frame, text=no_win_text, font=("Arial", 14),
                                            bg=difficulty_colors[difficulty], anchor="center")
                    no_win_label.pack()

                # Spacer between difficulty sections
                spacer = tk.Label(difficulty_frame, text="", bg=difficulty_colors[difficulty], width=5)
                spacer.pack(side="left")

    def load_difficulty_menu(self):
        # Load the difficulty selection menu
        self.clear_window()
        self.set_background("image/background.jpg")

        # Difficulty selection label
        label = tk.Label(
            self.root, text="Choisir la difficulté", font=("Impact", 44), bg="#D2691E", fg="white",
            relief="raised", bd=25
        )
        label.pack(pady=70)

        # Buttons for selecting difficulty
        btn_easy = tk.Button(
            self.root, text="Facile", font=("Impact", 18), bg="#8B4513", fg="white", width=20,
            height=2, relief="raised", bd=5, command=lambda: self.set_game(Difficulty.EASY)
        )
        btn_easy.pack(pady=(70, 20))

        btn_medium = tk.Button(
            self.root, text="Moyen", font=("Impact", 18), bg="#8B4513", fg="white", width=20,
            height=2, relief="raised", bd=5, command=lambda: self.set_game(Difficulty.MEDIUM)
        )
        btn_medium.pack(pady=(10, 20))

        btn_hard = tk.Button(
            self.root, text="Difficile", font=("Impact", 18), bg="#8B4513", fg="white", width=20,
            height=2, relief="raised", bd=5, command=lambda: self.set_game(Difficulty.HARD)
        )
        btn_hard.pack(pady=(10, 70))

        # Back button to main menu
        back_button = tk.Button(
            self.root, text="Retour au Menu Principal", font=("Impact", 14), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=self.load_main_menu
        )
        back_button.pack(pady=20)

    def load_saved_games_menu(self):
        # Load saved games menu
        self.clear_window()
        self.set_background("image/background.jpg")

        # Title label
        label = tk.Label(
            self.root, text="Parties Sauvegardées", font=("Impact", 44), bg="#D2691E", fg="white",
            relief="raised", bd=25
        )
        label.pack(pady=30)

        # Check if there are saved scores
        scores_file = "scores.json"
        if not os.path.exists(scores_file) or os.path.getsize(scores_file) == 0:
            tk.Label(self.root, text="Aucune partie sauvegardée.", font=("Arial", 14), bg="#D2691E", fg="white").pack(
                pady=10)
            button = tk.Button(
                self.root, text="Retour au Menu Principal", font=("Arial", 14), bg="#8B4513", fg="white",
                relief="raised", bd=5, command=self.load_main_menu
            )
            button.pack(pady=10)
            return

        # Load saved scores
        with open(scores_file, 'r') as f:
            scores = json.load(f)

        # Frame for search bar
        search_frame = tk.Frame(self.root, bg="#A0522D", relief="sunken", bd=5)
        search_frame.pack(pady=20, padx=10)

        search_label = tk.Label(search_frame, text="Rechercher par seed :", font=("Arial", 14), bg="#A0522D",
                                fg="white")
        search_label.pack(side="left")

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 14))
        search_entry.pack(side="left", padx=10, fill="x", expand=True)
        search_var.trace("w",
                         lambda name, index, mode, sv=search_var: self.update_saved_games_display(scores, sv.get()))

        # Frame to display saved games
        self.saved_games_frame = tk.Frame(self.root, bg="#8B4513", relief="raised", bd=25, padx=20, pady=20)
        self.saved_games_frame.pack(fill="both", expand=True, pady=5, padx=20)

        # Canvas to show saved games with scrollbar
        self.saved_games_canvas = tk.Canvas(self.saved_games_frame, bg="#D2B48C", highlightthickness=0)
        self.saved_games_canvas.pack(side="left", fill="both", expand=True)

        self.saved_games_scrollbar = tk.Scrollbar(
            self.saved_games_frame, orient="vertical", command=self.saved_games_canvas.yview
        )
        self.saved_games_canvas.config(yscrollcommand=self.saved_games_scrollbar.set)
        self.saved_games_canvas.bind("<Configure>", lambda e: self.saved_games_scrollbar.pack_forget() if
        self.saved_games_canvas.bbox("all")[3] <= e.height else
        self.saved_games_scrollbar.pack(side="right", fill="y"))

        self.saved_games_inner_frame = tk.Frame(self.saved_games_canvas, bg="#D2B48C")
        self.saved_games_canvas.create_window((0, 0), window=self.saved_games_inner_frame, anchor="n")

        self.update_saved_games_display(scores, "")

        # Back button to main menu
        back_button = tk.Button(
            self.root, text="Retour au Menu Principal", font=("Arial", 14), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=self.load_main_menu
        )
        back_button.pack(pady=20)

    def update_saved_games_display(self, scores, search_text):
        # Update display of saved games based on search input
        for widget in self.saved_games_inner_frame.winfo_children():
            widget.destroy()

        difficulties_names = {
            Difficulty.EASY: "Facile",
            Difficulty.MEDIUM: "Moyen",
            Difficulty.HARD: "Difficile"
        }

        row = 0
        column = 1

        for col in range(5):
            self.saved_games_inner_frame.grid_columnconfigure(col, weight=1)

        for i, score in enumerate(scores):
            if search_text.lower() not in str(score['seed']).lower():
                continue

            # Create a card for each saved game
            card_frame = tk.Frame(self.saved_games_inner_frame, bg="orange", relief="raised", bd=10, padx=20, pady=20)
            card_frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

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

            # Buttons for saved game actions
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
            if column > 7:
                column = 1
                row += 1

        self.saved_games_inner_frame.update_idletasks()
        self.saved_games_canvas.config(scrollregion=self.saved_games_canvas.bbox("all"))

    def set_game(self, difficulty):
        # Set up the game with selected difficulty
        rows, cols, mines = difficulty
        self.game = Game(rows, cols, mines, difficulty, seed=random.randint(0, 10000))
        self.elapsed_time = 0
        self.load_grid()

    def load_grid(self):
        self.clear_window()
        self.set_background("image/background.jpg")

        # Create the timer label if it doesn't exist
        if not self.timer_label:
            self.timer_label = tk.Label(
                self.root,
                text=f"Seed: {self.game.seed} | Time: 0 sec | ⚑ {self.game.flags}",
                font=("Impact", 24),
                bg="gray",
                fg="white",
                relief="raised",
                bd=5
            )
            self.timer_label.pack(pady=10)

        # Create the frame with a wood-style appearance
        self.frame = tk.Frame(
            self.root,
            bg="#8B4513",  # Light brown color for wood effect
            bd=10,  # 10-pixel border
            relief="ridge"  # Sculpted ridge border for a textured look
        )
        self.frame.pack(pady=5)

        # Create the grid of buttons
        rows, cols, mines = self.game.difficulty
        for row in range(rows):
            for col in range(cols):
                btn = tk.Button(
                    self.frame,
                    width=2,
                    height=1,
                    command=lambda r=row, c=col: self.click_case(r, c),
                    font=("Arial", 14),
                    bg="#D2B48C",  # Light sand color for buttons
                    fg="white",
                    relief="raised",  # Raised style for button relief
                    bd=3
                )
                btn.grid(row=row, column=col, padx=1, pady=1)
                self.game.grid[row][col].button = btn
                btn.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(r, c))

        # Save button to main menu
        save_button = tk.Button(
            self.root, text="Sauvegarder", font=("Arial", 14), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=lambda state=False: self.save_game(state)
        )
        save_button.pack(pady=20)

        # Back button to main menu
        back_button = tk.Button(
            self.root, text="Retour au Menu Principal", font=("Arial", 14), bg="#8B4513", fg="white",
            relief="raised", bd=5, command=self.load_main_menu
        )
        back_button.pack(pady=20)

        # Start the timer
        self.update_timer()

    def print_if_versus(self):
        if self.game.versus_player is not None and self.game.versus_player is not self.game.player:
            return f"Vous VS {self.game.versus_player} |"
        else:
            return ""

    def update_timer(self):
        if self.timer_label and self.game and self.game.start_time > 0 and self.game.is_running:
            self.elapsed_time = time.time() - self.game.start_time
            formatted_time = round(self.elapsed_time, 2)
            self.timer_label.config(text=f"Seed: {self.game.seed} | {self.print_if_versus()} Time: {formatted_time} sec | ⚑ {self.game.flags}")
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

        # Create a frame for the victory message and player name input
        victory_frame = tk.Frame(self.root, bg="orange", relief="raised", bd=25, padx=20, pady=20)
        victory_frame.pack(pady=20)

        # Display victory message
        print(self.game.versus_player)
        print(self.game.player)
        if self.game.versus_player is None or self.game.versus_player is self.game.player:
            label = tk.Label(victory_frame, text="Bravo, tu es le GOAT que tu pense être", font=("Arial", 24), fg="white", bg="orange")
            label.pack(pady=16)
        else:
            if self.game.versus_time < self.elapsed_time:
                label = tk.Label(victory_frame,
                                 text=f"Victoire mais {self.game.versus_player} a gagné de {round(self.elapsed_time - self.game.versus_time, 2)} sec",
                                 font=("Arial", 24),
                                 fg="white", bg="orange")
                label.pack(pady=16)
            else:
                label = tk.Label(victory_frame,
                                 text=f"Victoire tu as battu le record de {self.game.versus_player} de {round(self.game.versus_time - self.elapsed_time, 2)} sec",
                                 font=("Arial", 24),
                                 fg="white", bg="orange")
                label.pack(pady=16)
            self.game.versus_time = None
            self.game.versus_player = None

        # Show the seed
        label = tk.Label(victory_frame, text=f"Seed : {self.game.seed}", font=("Arial", 16), fg="white", bg="orange")
        label.pack(pady=10)

        # Show the elapsed time
        formatted_time = round(self.elapsed_time, 2)
        timer_label = tk.Label(victory_frame, text=f"Temps : {formatted_time} sec", font=("Arial", 16), fg="white",
                               bg="orange")
        timer_label.pack(pady=10)

        # Player name input field
        pseudo_label = tk.Label(victory_frame, text="Entrer votre pseudo :", font=("Arial", 16), fg="white", bg="orange")
        pseudo_label.pack(pady=10)

        pseudo_entry = tk.Entry(victory_frame, font=("Arial", 16))
        pseudo_entry.pack(pady=10)

        # Function to save the player's nickname and finish the game
        def save_pseudo():
            self.game.player = pseudo_entry.get() or "Joueur anonyme"
            self.save_game(True)
            self.elapsed_time = 0
            pseudo_entry.config(state="disabled")
            save_btn.config(state="disabled")

        # Save button
        save_btn = tk.Button(victory_frame, text="Enregistrer le pseudo", font=("Arial", 14), command=save_pseudo, fg="white",
                             bg="#8B4513")
        save_btn.pack(pady=10)

        # Replay button
        replay_btn = tk.Button(self.root, text="Rejouer", font=("Arial", 14),
                               command=lambda: self.replay_game(self.game.seed, self.game.player), fg="white",
                               bg="#8B4513")
        replay_btn.pack(pady=10)

        # Main menu button
        main_menu_btn = tk.Button(self.root, text="Retour au menu", font=("Arial", 14), command=self.load_main_menu,
                                  fg="white", bg="#8B4513")
        main_menu_btn.pack(pady=10)

    def game_over(self):
        self.game.is_running = False
        self.save_game(False)

        # Reveal all cells
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                if self.game.grid[row][col].is_flagged:
                    self.game.grid[row][col].is_flagged = False
                self.game.grid[row][col].reveal()
        self.root.after(2000, self.show_defeat_screen)

    def show_defeat_screen(self):
        self.clear_window()
        self.set_background("image/background.jpg")

        # Create defeat screen frame
        defeat_frame = tk.Frame(self.root, bg="grey", relief="raised", bd=25, padx=20, pady=20)
        defeat_frame.pack(pady=20)

        # Display defeat message
        label = tk.Label(defeat_frame, text="Dommage, c'était une bombe", font=("Arial", 24), bg="grey", fg="white")
        label.pack(pady=50)

        # Show the seed
        label = tk.Label(defeat_frame, text=f"Seed : {self.game.seed}", font=("Arial", 14), fg="white", bg="grey")
        label.pack(pady=10)

        # Show the elapsed time
        formatted_time = round(self.elapsed_time, 2)
        timer_label = tk.Label(defeat_frame, text=f" Temps: {formatted_time} sec", font=("Arial", 14), bg="grey",
                               fg="white")
        timer_label.pack(pady=10)
        self.elapsed_time = 0

        # Retake button
        replay_btn = tk.Button(
            self.root, text="Reprendre", font=("Arial", 14), bg="#8B4513", fg="white", relief="raised", bd=5,
            command=lambda: self.retake_game(self.game.seed, self.game.player)
        )
        replay_btn.pack(pady=5)

        # Replay button
        replay_btn = tk.Button(
            self.root, text="Rejouer", font=("Arial", 14), bg="#8B4513", fg="white", relief="raised", bd=5,
            command=lambda: self.replay_game(self.game.seed, self.game.player)
        )
        replay_btn.pack(pady=5)

        # Back to main menu button
        back_button = tk.Button(self.root, text="Retour au menu", font=("Arial", 14), bg="#8B4513", fg="white",
                                relief="raised", bd=5, command=self.load_main_menu)
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

        # Convert the game grid into a serializable format
        grid_serializable = [
            [case_to_dict(cell) for cell in row] for row in self.game.grid
        ]

        # Create a dictionary to hold the current game state
        score_data = {
            "seed": self.game.seed,
            "player": self.game.player,
            "versus_player": self.game.versus_player,
            "versus_time": self.game.versus_time,
            "time": self.elapsed_time,
            "difficulty": self.game.difficulty,
            "first_position": self.game.first_position,
            "grid": grid_serializable,
        }

        # If the game is not saved yet, add victory status and best time
        if not self.game.is_saved:
            score_data["victory"] = victory
            score_data["best_time"] = self.elapsed_time

        # Create the JSON file if it doesn't exist
        if not os.path.exists(scores_file):
            with open(scores_file, 'w') as f:
                json.dump([score_data], f)
        else:
            with open(scores_file, 'r+') as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = []

                # Check if a saved score exists for the current game and player
                for i, score in enumerate(scores):
                    if score['seed'] == self.game.seed and (
                            score['player'] == self.game.player or score['player'] is None):
                        # Update the score data if the player wins
                        if victory:
                            score_data["victory"] = True
                            if score['victory']:
                                if self.elapsed_time < score['best_time']:
                                    score_data["best_time"] = self.elapsed_time
                                else:
                                    score_data["best_time"] = score["best_time"]
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
                    # Add new score if not found in existing records
                    score_data["victory"] = victory
                    score_data["best_time"] = self.elapsed_time
                    scores.append(score_data)

                # Update the scores file with the modified data
                f.seek(0)
                json.dump(scores, f)
                f.truncate()

    def challenge_game(self, seed, player):
        saved_score = self.get_saved_score_by_seed(seed, player)
        if saved_score:
            difficulty = saved_score['difficulty']
            rows, cols, mines = difficulty

            # Initialize the game with saved parameters
            self.game = Game(rows, cols, mines, difficulty, seed=seed)
            self.game.first_position = saved_score['first_position']
            self.game.versus_player = player
            self.game.versus_time = saved_score['best_time']
            self.game.start_time = time.time()
            self.load_grid()

            # Restore grid state from saved data
            for r in range(len(saved_score['grid'])):
                for c in range(len(saved_score['grid'][r])):
                    self.game.grid[r][c].is_mine = saved_score['grid'][r][c]["is_mine"]
                    self.game.grid[r][c].adjacent_mines = saved_score['grid'][r][c]["adjacent_mines"]

            # Click the first position to start the game
            r, c = self.game.first_position
            self.click_case(r, c)

    def replay_game(self, seed, player):
        saved_score = self.get_saved_score_by_seed(seed, player)
        if saved_score:
            difficulty = saved_score['difficulty']
            rows, cols, mines = difficulty

            # Initialize a new game based on saved score
            self.game = Game(rows, cols, mines, difficulty, seed=seed)
            self.game.first_position = saved_score['first_position']
            self.game.is_saved = True
            self.game.player = saved_score['player']
            self.game.start_time = time.time()
            self.game.best_time = saved_score['best_time']
            self.game.versus_player = saved_score['versus_player']
            self.game.versus_time = saved_score['versus_time']
            self.load_grid()

            # Restore grid state from saved data
            for r in range(len(saved_score['grid'])):
                for c in range(len(saved_score['grid'][r])):
                    self.game.grid[r][c].is_mine = saved_score['grid'][r][c]["is_mine"]
                    self.game.grid[r][c].adjacent_mines = saved_score['grid'][r][c]["adjacent_mines"]

            # Click the first position to continue the game
            r, c = self.game.first_position
            self.click_case(r, c)

    def retake_game(self, seed, player):
        saved_score = self.get_saved_score_by_seed(seed, player)
        if saved_score:
            difficulty = saved_score['difficulty']
            rows, cols, mines = difficulty

            # Initialize a new game based on saved score
            self.game = Game(rows, cols, mines, difficulty, seed=seed)
            self.game.first_position = saved_score['first_position']
            self.game.is_saved = True
            self.game.player = saved_score['player']
            self.game.start_time = time.time() - saved_score['time']
            self.game.best_time = saved_score['best_time']
            self.game.versus_player = saved_score['versus_player']
            self.game.versus_time = saved_score['versus_time']
            self.load_grid()

            # Restore grid state from saved data
            for r in range(rows):
                for c in range(cols):
                    case = self.game.grid[r][c]
                    saved_case = saved_score['grid'][r][c]
                    case.is_mine = saved_case["is_mine"]
                    case.is_flagged = saved_case["is_flagged"]
                    case.is_revealed = saved_case["is_revealed"]
                    case.adjacent_mines = saved_case["adjacent_mines"]

                    # Ensure mines and revealed states are correct
                    if case.is_mine:
                        case.is_revealed = False
                    if not case.is_flagged and case.is_revealed:
                        case.is_revealed = False
                        case.reveal()
                    if case.is_flagged:
                        case.is_flagged = False
                        case.toggle_flag()
                        self.game.flags -= 1

    # Search saved game by seed and player
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