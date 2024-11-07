import random

def create_grid(height, width, difficulty, first_click=None):
    grid = [[0 for _ in range(width)] for _ in range(height)]  # Crée une grille vide

    # Calcul du nombre de mines en fonction de la difficulté
    total_mines = int(difficulty * height * width)
    placed_mines = 0

    # Placer les mines, en évitant la première case cliquée
    while placed_mines < total_mines:
        r = random.randint(0, height - 1)
        c = random.randint(0, width - 1)

        # Assurez-vous que la mine ne soit pas placée sur la première case cliquée
        if first_click and (r, c) == first_click:
            continue

        if grid[r][c] != -1:  # Vérifier qu'il n'y a pas déjà une mine
            grid[r][c] = -1  # Placer une mine
            placed_mines += 1

    return grid

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
