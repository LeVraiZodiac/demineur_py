import tkinter as tk
from tkinter import messagebox
import json
import os
import time

from grille import Grille

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

    # Autres méthodes de la classe Demineur