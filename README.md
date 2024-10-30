# Démineur
## Prérequis
Installer Tkinker pour WSL :
```sudo apt install python3-tk```
## Branch
Chacun possède une branch, avant de prog, pensez à `pull`. Ne pas `push` votre travail, avant il faut check les fichiers qui ont été modifier pour éviter de créer un conflit. Pour `pull` les modifications de la branche main, faites `git rebase main`.
>[!attention]
>Avant de `pull` vos modifications, annoncez aux autres les fichiers que vous avez modifiers.
## To Do
### Evan
  Créer les fonctions create_grid(), place_mines(), check_win()
### Dylan
  Créer une class game qui permet de stocker le nombre de mines, l'état de la partie et la longueur, la largeur de la grid (Game.py)
### Vincent
  Créer un système de logs. Sauvegarder la génération d'une partie + l'état d'une partie en cours
### Victor
  Créer un système de restart, mettre en place Tkinter
