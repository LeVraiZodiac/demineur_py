import tkinter as tk
from tkinter import ttk

class DifficultyMenu(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Chose Difficulty")
        self.resizable(False, False)
        self.geometry("200x400")

        self.parent = parent

        self.easy_button = ttk.Button(self, text="Easy", command=self.on_easy)
        self.easy_button.pack(pady=10)

        self.medium_button = ttk.Button(self, text="Medium", command=self.on_medium)
        self.medium_button.pack(pady=10)

        self.hard_button = ttk.Button(self, text="Hard", command=self.on_hard)
        self.hard_button.pack(pady=10)

        self.cancel_button = ttk.Button(self, text="Back", command=self.destroy)
        self.cancel_button.pack(pady=10)

    def on_easy(self):
        self.parent.on_difficulty("Easy")
        self.destroy()

    def on_medium(self):
        self.parent.on_difficulty("Medium")
        self.destroy()

    def on_hard(self):
        self.parent.on_difficulty("Hard")
        self.destroy()

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        self.root.resizable(False, False)
        self.root.geometry(f"400x400")
        self.load_main_menu()

    def load_main_menu(self):
        self.clear_window()

        label = tk.Label(self.root, text="Minesweeper", font=("Arial", 24))
        label.pack(pady=20)

        buttons = [
            ("New Game", lambda: self.load_difficulty_menu()),
            ("Load Game", lambda: self.load_game_saved_menu()),
            ("Scoreboard", lambda: self.load_scoreboard_menu()),
            ("Exit", lambda: self.root.destroy())
        ]
        for text, command in buttons:
            button = tk.Button(self.root, text=text, font=("Arial", 14), command=command)
            button.pack(pady=10)

    def load_difficulty_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text="Chose Difficulty", font=("Arial", 24))
        label.pack(pady=20)

        for difficulty in ["Easy", "Medium", "Hard"]:
            btn = tk.Button(self.root, text=difficulty, font=("Arial", 14), width=10,
                            command=lambda d=difficulty: d.set())
            btn.pack(pady=10)

        button = tk.Button(self.root, text="Back", font=("Arial", 14), command=lambda: self.load_main_menu())
        button.pack(pady=10)

    def load_game_saved_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text="Load Game", font=("Arial", 24))
        label.pack(pady=20)

        button = tk.Button(self.root, text="Back", font=("Arial", 14), command=lambda: self.load_main_menu())
        button.pack(pady=10)

    def load_scoreboard_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text="Best Score", font=("Arial", 24))
        label.pack(pady=20)

        label = tk.Label(self.root, text="Test : 13m14s", font=("Arial", 24))
        label.pack(pady=20)

        button = tk.Button(self.root, text="Back", font=("Arial", 14), command=lambda: self.load_main_menu())
        button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()