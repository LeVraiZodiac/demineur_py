import tkinter as tk
from tkinter import ttk, messagebox

W_WIDTH, W_HEIGHT = 800, 800

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Démineur")
        self.resizable(False, False)
        self.geometry(f"{W_WIDTH}x{W_HEIGHT}")

        # Center frame in the window
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Center main_frame in window
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(7, weight=1)  # Rows above and below buttons
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Create and layout buttons with increased size
        button_options = {"padding": (20, 10)}

        self.new_game_button = ttk.Button(self.main_frame, text="New Game", command=self.on_new_game, **button_options)
        self.new_game_button.grid(row=1, column=0, padx=5, pady=5)

        self.load_game_button = ttk.Button(self.main_frame, text="Load Game", command=self.on_load_game, **button_options)
        self.load_game_button.grid(row=2, column=0, padx=5, pady=5)

        self.scoreboard_button = ttk.Button(self.main_frame, text="Scoreboard", command=self.on_scoreboard, **button_options)
        self.scoreboard_button.grid(row=3, column=0, padx=5, pady=5)

        self.easy_button = ttk.Button(self.main_frame, text="Easy", command=self.on_easy, **button_options)
        self.easy_button.grid(row=4, column=0, padx=5, pady=5)

        self.medium_button = ttk.Button(self.main_frame, text="Medium", command=self.on_medium, **button_options)
        self.medium_button.grid(row=5, column=0, padx=5, pady=5)

        self.hard_button = ttk.Button(self.main_frame, text="Hard", command=self.on_hard, **button_options)
        self.hard_button.grid(row=6, column=0, padx=5, pady=5)

    def on_new_game(self):
        messagebox.showinfo("New Game", "Starting new game...")

    def on_load_game(self):
        messagebox.showinfo("Load Game", "Loading game...")

    def on_scoreboard(self):
        messagebox.showinfo("Scoreboard", "Opening scoreboard...")

    def on_easy(self):
        messagebox.showinfo("Difficulty", "Setting difficulty to Easy")

    def on_medium(self):
        messagebox.showinfo("Difficulty", "Setting difficulty to Medium")

    def on_hard(self):
        messagebox.showinfo("Difficulty", "Setting difficulty to Hard")

if __name__ == "__main__":
    app = App()
    app.mainloop()
