class Case:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
        self.button = None
        self.color = ["#d7b899", "#19a4d2", "#1976d2", "#4d19d2", "#7c19d2", "#bc19d2", "#CC0099", "#d21947", "#d21919"]

    def toggle_flag(self):
        if self.is_revealed:
            return False
        self.is_flagged = not self.is_flagged
        self.button.config(text="⚑" if self.is_flagged else "", fg="red")
        return True

    def reveal(self):
        if not self.is_flagged and self.button:
            self.is_revealed = True
            self.button.config(state="normal", disabledforeground="#ffffff")
            self.button.bind("<Button-1>", lambda e: "break")
            if self.is_mine:
                self.button.config(text="x", fg="#ffffff", bg="#212121")
                return False
            else:
                if self.adjacent_mines > 0:
                    self.button.config(text=str(self.adjacent_mines), fg="#ffffff", bg=self.color[self.adjacent_mines])
                else:
                    bg_color = "#d7b899" if (self.row + self.col) % 2 == 0 else "#e5c29f"
                    self.button.config(text="", bg=bg_color)
                return True

        return True