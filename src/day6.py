from command_line_parser import get_arguments_from_command_line
import time

obstacle_symbols = ('#', 'O')
guard_symbols = ('^', '<', '>')

################################## PART 1 ##################################


def obstacle_ahead(grid: list[list[str]], position: tuple[int, int], direction: tuple[int, int]) -> bool:
  next_position = (position[0] + direction[0], position[1] + direction[1])
  if 0 <= next_position[0] < len(grid) and 0 <= next_position[1] < len(grid[0]):
    next_x, next_y = next_position
    if grid[next_x][next_y] in obstacle_symbols:
      return True
  return False


def change_direction(direction: tuple[int, int]) -> tuple[int, int]:
  """Lorsqu'un obstacle est rencontré, cette fonction détermine la nouvelle direction
  qui est l'ancienne direction tournée de 90° dans le sens des aiguilles d'une montre
  """
  new_direction = (0, 0)
  if direction == (0, 1):
    # si on allait sur la droite, aller vers le bas
    new_direction = (1, 0)
  elif direction == (0, -1):
    # si on allait sur la gauche, aller vers le haut
    new_direction = (-1, 0)
  elif direction == (-1, 0):
    # si on allait vers le haut, aller à droite
    new_direction = (0, 1)
  elif direction == (1, 0):
    # si on allait en bas, aller à gauche
    new_direction = (0, -1)
  return new_direction


def determine_start_position_and_direction(grid: list[list[str]]) -> tuple[tuple[int, int], tuple[int, int]]:
  """Détermine la position de départ du garde et sa direction. La position initiale du garde peut être indiquée
    par les symboles '^', '<' ou '>'. En fonction du symbole, la direction peut être droite, gauche, haut ou bas.
  :returns position (x,y) initiale du garde et sa direction (x,y)
  """
  init_position = (0, 0)
  init_direction = (0, 0)
  for line in range(len(grid)):
    for column in range(len(grid[0])):
      if 0 <= line < len(grid) and 0 <= column < len(grid[0]):
        current_character = grid[line][column]
        if current_character in guard_symbols:
          init_position = (line, column)
          if current_character == guard_symbols[0]:
            init_direction = (-1, 0)
          elif current_character == guard_symbols[1]:
            init_direction = (0, -1)
          elif current_character == guard_symbols[2]:
            init_direction = (0, 1)
  while obstacle_ahead(grid, init_position, init_direction):
    init_direction = change_direction(init_direction)
  return init_position, init_direction


def determine_visited_locations(grid: list[list[str]]) -> list[tuple[int, int]]:
  """Détermine le chemin du garde"""
  visited_locations: list[tuple[int, int]] = []
  position, direction = determine_start_position_and_direction(grid)
  while 0 <= position[0] < len(grid) and 0 <= position[1] < len(grid[0]):
    visited_locations.append(position)
    position = (position[0] + direction[0], position[1] + direction[1])
    while obstacle_ahead(grid, position, direction):
      direction = change_direction(direction)
  return visited_locations


def count_unique_locations(visited_locations: list[tuple[int, int]]) -> int:
  return len(set(visited_locations))


################################## PART 2 ##################################

def stuck_in_loop(grid: list[list[str]], start_position: tuple[int, int],
                  start_direction: tuple[int, int]) -> bool:
  """
  Le garde est bloqué s'il repasse par un emplacement qu'il a déjà visité avec la MEME
  direction
  """
  # pour accélérer la fonction, remplacer les listes previous_positions et previous_directions
  # par un dictionnaire dont la clé est la position et la valeur est la direction
  history = {}
  stuck = False
  position, direction = start_position, start_direction
  nb_lines, nb_columns = len(grid), len(grid[0])
  while (0 <= position[0] < nb_lines and 0 <= position[1] < nb_columns):
    history[position] = direction
    position = (position[0] + direction[0], position[1] + direction[1])
    while obstacle_ahead(grid, position, direction):
      direction = change_direction(direction)
    # éviter les try-except couteux et les remplacer par des if
    if position in history and history[position] == direction:
      stuck = True
      break
  return stuck


def determine_obstructions_locations(grid: list[list[str]]) -> set[tuple[int, int]]:
  """Détermine les positions où un obstacle peut être mis pour bloquer
  le garde dans une boucle infinie
  :returns liste des positions de l'obstacle 
  """
  obstructions_positions: set[tuple[int, int]] = set()
  visited_locations = determine_visited_locations(grid)
  start_position, start_direction = determine_start_position_and_direction(
      grid)
  for position in visited_locations[1:]:
    x, y = position
    old_value = grid[x][y]
    grid[x][y] = 'O'
    if stuck_in_loop(grid, start_position, start_direction):
      if position not in obstructions_positions:
        obstructions_positions.add(position)
    grid[x][y] = old_value
  return obstructions_positions


def count_obstructions(obstructions_positions: set[tuple[int, int]]) -> int:
  return len(obstructions_positions)

############################## LAUNCH PROGRAM ##############################


def build_guard_path(grid: list[list[str]], visited_locations: list[tuple[int, int]]) -> list[list[str]]:
  """Construit une nouvelle grille où le chemin par où est passé le guard est indiqué par des 'X'
  :returns nouvelle grille avec le chemin du guard et le nombre de cases différentes qu'a visité
    le guard
  """
  guard_path: list[list[str]] = grid.copy()
  for position in visited_locations:
    x, y = position
    guard_path[x][y] = 'X'
  return guard_path


def get_grid_from_file(filename: str) -> list[list[str]]:
  """
  Récupère la grille depuis le fichier donné en paramètre
  :returns la grille qui ne contient que 3 caractères : '.', '#' et '^' (ou ses dérivés: '<', '>')
  """
  grid: list[list[str]] = []
  with open(filename, 'r', encoding='utf8') as file:
    for line in file:
      grid.append([character for character in line if character != '\n'])
  return grid


def display_grid(grid: list[list[str]]) -> None:
  """Fonction qui permet d'afficher la grille sous une forme
  plus lisible que l'affichage par défaut via print
  """
  for line in range(len(grid)):
    row_elements = [grid[line][column] for column in range(len(grid[0]))]
    print(*row_elements)


if __name__ == "__main__":
  filename, part = get_arguments_from_command_line()
  start_time = time.time()
  grid = get_grid_from_file(filename)
  if part == 1:
    visited_locations = determine_visited_locations(grid)
    unique_locations_count = count_unique_locations(visited_locations)
    # ne pas calculer ni afficher le chemin du garde si la map est trop grande
    # guard_path = build_guard_path(grid, visited_locations)
    # display_grid(guard_path)
    print("Number of locations visited:", unique_locations_count)
  elif part == 2:
    obstructions_positions = determine_obstructions_locations(grid)
    print("Number of possible locations for obstacle:",
          count_obstructions(obstructions_positions))
  print(f"Elapsed time: {time.time() - start_time} s")

# IMPORTANT : si le fichier est compilé avec mypyc s'assurer des choses suivantes :
# 1. La ligne "if __name__ == __main__" est bien retirée
# 2. Compiler le fichier et ses dépendances (imports)
# 3. Lancer le programme avec la commande suivante :
# python -c "import day6" .\inputs\day6.txt -p=2
