# check_win.py

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
