from command_line_parser import get_arguments_from_command_line

visited_locations: list[tuple[int, int]] = []

################################## PART 1 ##################################


def obstacle_ahead(grid: list[list[str]], position: tuple[int, int], direction: tuple[int, int]) -> bool:
  next_position = (position[0] + direction[0], position[1] + direction[1])
  if 0 <= next_position[0] < len(grid) and 0 <= next_position[1] < len(grid[0]):
    next_x, next_y = next_position
    if grid[next_x][next_y] == '#':
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
  guard_symbols = ('^', '<', '>')
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
  return init_position, init_direction


def count_unique_locations(grid: list[list[str]]) -> int:
  unique_locations_count = 0
  position, direction = determine_start_position_and_direction(grid)
  while 0 <= position[0] < len(grid) and 0 <= position[1] < len(grid[0]):
    if position not in visited_locations:
      visited_locations.append(position)
      unique_locations_count += 1
    # marquer la case comme visitée si elle ne l'est pas déjà
    if obstacle_ahead(grid, position, direction):
      direction = change_direction(direction)
    position = (position[0] + direction[0], position[1] + direction[1])
  return unique_locations_count


################################## PART 2 ##################################

############################## LAUNCH PROGRAM ##############################

def build_guard_path(grid: list[list[str]]) -> list[list[str]]:
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
  grid = get_grid_from_file(filename)
  if part == 1:
    unique_locations_count = count_unique_locations(grid)
    # ne pas calculer ni afficher le chemin du garde si la map est trop grande
    # guard_path = build_guard_path(grid)
    # display_grid(guard_path)
    print("Number of locations visited:", unique_locations_count)
  elif part == 2:
    print("Part 2 to be implemented")
