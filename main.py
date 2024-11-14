import tkinter as tk
from Minesweeper import Minesweeper

if __name__ == "__main__":
    root = tk.Tk()
    jeu = Minesweeper(root)
    root.mainloop()
