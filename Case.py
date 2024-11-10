class Case:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
        self.button = None
        self.color = ["#D3D3D3", "#0000FF", "#3300E6", "#6600CC", "#9900B3", "#CC0099", "#FF0066", "#FF0033", "#FF0000"]

    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
            self.button.config(text="⚑" if self.is_flagged else "")
            self.button.config(fg="black" if self.is_flagged else "red")

    def reveal(self):
        if not self.is_flagged and self.button:
            self.is_revealed = True
            self.button.config(state="disabled")
            if self.is_mine:
                self.button.config(text="x", fg="white", bg="black")
                return False
            else:
                self.button.config(text=str(self.adjacent_mines) if self.adjacent_mines > 0 else "")
                self.button.config(fg="white", bg=self.color[self.adjacent_mines])
                return True
        return True