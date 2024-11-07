import tkinter as tk
from place_mines import create_grid, create_adjacent_values
from check_win import check_win  # Importer la fonction check_win
import tkinter.messagebox as messagebox  # Pour afficher des messages (Game Over)
import random

# Enum pour la difficulté
class Difficulty:
    EASY = 0.1
    MEDIUM = 0.15
    HARD = 0.2


height = 9
width = 9
difficulty = Difficulty.MEDIUM  # Choisir la difficulté ici
grid_with_mines = None
adj_values = None
revealed = None
buttons = []


# Créer une grille sûre pour que la première case ne soit pas une mine ni un numéro
def create_safe_grid(height, width, difficulty, first_click):
    grid_with_mines = create_grid(height, width, difficulty, first_click)
    adj_values = create_adjacent_values(grid_with_mines, height, width)

    # S'assurer que la première case n'est ni une mine ni adjacente à une mine
    fr, fc = first_click
    if grid_with_mines[fr][fc] == -1:  # Si la case cliquée est une mine
        grid_with_mines[fr][fc] = 0  # La rendre vide
        adj_values = create_adjacent_values(grid_with_mines, height, width)  # Recalculer les valeurs adjacentes

    return grid_with_mines, adj_values


# Fonction pour la couleur des numéros
def get_number_color(num):
    if num == 1:
        return "blue"
    elif num == 2:
        return "green"
    elif num == 3:
        return "red"
    elif num == 4:
        return "purple"
    elif num == 5:
        return "brown"
    elif num == 6:
        return "gray"
    else:
        return "black"  # Pour les autres numéros


# Créer l'interface graphique
def create_gui():
    global grid_with_mines, adj_values, revealed, buttons
    revealed = [[False for _ in range(width)] for _ in range(height)]  # Suivi des cellules révélées
    root = tk.Tk()
    root.title("Démineur")

    # Créer un bouton pour chaque case
    for row in range(height):
        button_row = []
        for col in range(width):
            button = tk.Button(root, text="", width=4, height=2,
                               command=lambda r=row, c=col: on_cell_click(r, c))  # Capture row and col
            button.grid(row=row, column=col)
            button_row.append(button)
        buttons.append(button_row)

    root.mainloop()


# Fonction pour révéler les cellules adjacentes (case vide)
def reveal_empty_cells(row, col, grid_with_mines, adj_values, revealed, height, width):
    to_reveal = [(row, col)]  # Liste des cellules à révéler

    # Fonction pour révéler la cellule et ses voisins adjacents
    def reveal_neighbors(r, c):
        if revealed[r][c]:
            return
        revealed[r][c] = True
        if grid_with_mines[r][c] == -1:  # Si c'est une mine
            buttons[r][c].config(bg="red", text="X")
        else:
            buttons[r][c].config(bg="lightgray", text=str(adj_values[r][c]) if adj_values[r][c] > 0 else "")
            # Appliquer la couleur des numéros
            num = adj_values[r][c]
            if num > 0:
                buttons[r][c].config(fg=get_number_color(num))

        if adj_values[r][c] == 0:  # Si la cellule est vide, on veut révéler les voisins
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width and not revealed[nr][nc]:
                        to_reveal.append((nr, nc))

    # On commence par révéler la cellule initiale
    reveal_neighbors(row, col)

    # Révéler les autres cellules
    while to_reveal:
        r, c = to_reveal.pop()
        reveal_neighbors(r, c)  # Révèle cette cellule


# Fonction de gestion du clic sur une cellule
def on_cell_click(row, col):
    global grid_with_mines, adj_values
    if grid_with_mines is None or adj_values is None:  # Si la grille n'est pas encore initialisée
        # Initialiser la grille sans mine à cet endroit
        first_click = (row, col)
        grid_with_mines, adj_values = create_safe_grid(height, width, difficulty, first_click)
        reveal_empty_cells(row, col, grid_with_mines, adj_values, revealed, height, width)
        return  # Ne pas faire plus après le premier clic

    if grid_with_mines[row][col] == -1:  # Si une mine est cliquée
        buttons[row][col].config(bg="red", text="X")
        print(f"Mine clicked at ({row}, {col})")
        game_over()  # Appel de la fonction pour arrêter le jeu
    else:
        reveal_empty_cells(row, col, grid_with_mines, adj_values, revealed, height, width)

    # Vérification de la victoire à chaque clic
    if check_win(grid_with_mines, revealed, buttons, height, width):
        print("Vous avez gagné !")
        # Ajouter ici un message ou une boîte de dialogue si nécessaire


# Fonction pour gérer la fin de la partie (Game Over)
def game_over():
    messagebox.showinfo("Game Over", "Vous avez cliqué sur une mine !")
    # Désactiver tous les boutons
    for row in range(height):
        for col in range(width):
            buttons[row][col].config(state="disabled")


# Fonction pour créer la grille avec des mines
def create_grid(height, width, difficulty, first_click=None):
    grid = [[0 for _ in range(width)] for _ in range(height)]  # Crée une grille vide

    # Calcul du nombre de mines en fonction de la difficulté
    total_mines = int(difficulty * height * width)
    placed_mines = 0

    # Placer les mines en évitant la première case cliquée et ses voisins
    while placed_mines < total_mines:
        r = random.randint(0, height - 1)
        c = random.randint(0, width - 1)

        # S'assurer que la mine ne soit pas placée sur la première case cliquée ni ses voisines
        if first_click:
            fr, fc = first_click
            if (r == fr and c == fc) or any(
                (r == fr + dr and c == fc + dc) for dr in range(-1, 2) for dc in range(-1, 2)
            ):
                continue

        if grid[r][c] != -1:  # Vérifier qu'il n'y a pas déjà une mine
            grid[r][c] = -1  # Placer une mine
            placed_mines += 1

    return grid


# Fonction pour créer les valeurs adjacentes
def create_adjacent_values(grid, height, width):
    adj_values = [[0 for _ in range(width)] for _ in range(height)]

    # Calcul des valeurs adjacentes
    for r in range(height):
        for c in range(width):
            if grid[r][c] == -1:  # Si c'est une mine, on ne calcule pas l'adjacence
                continue
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] == -1:
                        adj_values[r][c] += 1

    return adj_values


# Fonction pour vérifier la victoire
def check_win(grid_with_mines, revealed, buttons, height, width):
    game_over = False  # Variable pour vérifier si la partie est terminée

    # Vérifier si toutes les cases sans mine ont été révélées
    for r in range(height):
        for c in range(width):
            if grid_with_mines[r][c] != -1 and not revealed[r][c]:  # Si une case sans mine n'est pas révélée
                return game_over  # La partie continue

    # Si toutes les cases sans mine sont révélées, le joueur a gagné
    game_over = True
    print("Vous avez gagné !")

    # Désactiver tous les boutons
    for row in range(height):
        for col in range(width):
            buttons[row][col].config(state="disabled")

    return game_over


# Créer la grille initiale et démarrer le jeu
if __name__ == "__main__":
    create_gui()
