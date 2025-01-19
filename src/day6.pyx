# global variables
DEF N_ROWS = 10
DEF N_COLUMNS = 10
obstacle_symbols = ('#', 'O')
guard_symbols = ('^', '<', '>')

################################## PART 1 ##################################


def obstacle_ahead(grid: char[N_ROWS][N_COLUMNS], position: tuple[int, int], direction: tuple[int, int]) -> bool:
  next_position = (position[0] + direction[0], position[1] + direction[1])
  if 0 <= next_position[0] < N_ROWS and 0 <= next_position[1] < N_COLUMNS:
    next_x, next_y = next_position
    if chr(grid[next_x][next_y]) in obstacle_symbols:
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


def determine_start_position_and_direction(grid: char[N_ROWS][N_COLUMNS]) -> tuple[tuple[int, int], tuple[int, int]]:
  """Détermine la position de départ du garde et sa direction. La position initiale du garde peut être indiquée
    par les symboles '^', '<' ou '>'. En fonction du symbole, la direction peut être droite, gauche, haut ou bas.
  :returns position (x,y) initiale du garde et sa direction (x,y)
  """
  init_position = (0, 0)
  init_direction = (0, 0)
  # define x and y as C types to compile for-loop in pure C code
  cdef int x = 0, y = 0
  for x in range(N_ROWS):
    for y in range(N_COLUMNS):
      current_character = chr(grid[x][y])
      if current_character in guard_symbols:
        init_position = (x, y)
        if current_character == guard_symbols[0]:
          init_direction = (-1, 0)
        elif current_character == guard_symbols[1]:
          init_direction = (0, -1)
        elif current_character == guard_symbols[2]:
          init_direction = (0, 1)
  while obstacle_ahead(grid, init_position, init_direction):
    init_direction = change_direction(init_direction)
  return init_position, init_direction


def determine_visited_locations(grid: char[N_ROWS][N_COLUMNS]) -> list[tuple[int, int]]:
  """Détermine le chemin du garde"""
  visited_locations: list[tuple[int, int]] = []
  position, direction = determine_start_position_and_direction(grid)
  while 0 <= position[0] < N_ROWS and 0 <= position[1] < N_COLUMNS:
    visited_locations.append(position)
    position = (position[0] + direction[0], position[1] + direction[1])
    while obstacle_ahead(grid, position, direction):
      direction = change_direction(direction)
  return visited_locations


def count_unique_locations(visited_locations: list[tuple[int, int]]) -> int:
  return len(set(visited_locations))


################################## PART 2 ##################################

def stuck_in_loop(grid: char[N_ROWS][N_COLUMNS], start_position: tuple[int, int],
                  start_direction: tuple[int, int]) -> bool:
  """
  Le garde est bloqué s'il repasse par un emplacement qu'il a déjà visité avec la MEME
  direction
  """
  previous_positions: list[tuple[int, int]] = []
  previous_directions: list[tuple[int, int]] = []
  stuck = False
  position, direction = start_position, start_direction
  cdef int x = position[0]
  cdef int y = position[1]
  while (0 <= x < N_ROWS and 0 <= y < N_COLUMNS):
    previous_positions.append(position)
    previous_directions.append(direction)
    position = (x + direction[0], y + direction[1])
    while obstacle_ahead(grid, position, direction):
      direction = change_direction(direction)
    try:
      position_index = previous_positions.index(position)
      if previous_directions[position_index] == direction:
        stuck = True
        break
    except ValueError:
      # la position courante n'a pas été trouvée dans les anciennes positions
      continue
  return stuck


def determine_obstructions_locations(grid: char[N_ROWS][N_COLUMNS]) -> list[tuple[int, int]]:
  """Détermine les positions où un obstacle peut être mis pour bloquer
  le garde dans une boucle infinie
  :returns liste des positions de l'obstacle 
  """
  obstructions_positions: list[tuple[int, int]] = []
  visited_locations = determine_visited_locations(grid)
  nb_locations_to_visit = len(visited_locations)
  start_position, start_direction = determine_start_position_and_direction(
      grid)
  for index, position in enumerate(visited_locations[1:]):
    if index % 30 == 0:
      print(f"Progression: {index / nb_locations_to_visit * 100} %")
    x, y = position
    old_value = chr(grid[x][y])
    grid[x][y] = ord("O")
    if stuck_in_loop(grid, start_position, start_direction):
      if position not in obstructions_positions:
        obstructions_positions.append(position)
    grid[x][y] = ord(old_value)
  return obstructions_positions


def count_obstructions(obstructions_positions: list[tuple[int, int]]) -> int:
  return len(obstructions_positions)

############################## LAUNCH PROGRAM ##############################


def build_guard_path(grid: char[N_ROWS][N_COLUMNS], visited_locations: list[tuple[int, int]]) -> list[list[str]]:
  """Construit une nouvelle grille où le chemin par où est passé le guard est indiqué par des 'X'
  :returns nouvelle grille avec le chemin du guard et le nombre de cases différentes qu'a visité
    le guard
  """
  # define x and y as C types to compile for-loop in pure C code
  cdef int x = 0, y = 0
  cdef char[N_ROWS][N_COLUMNS] guard_path
  for x in range(N_ROWS):
    for y in range(N_COLUMNS):
      if (x, y) in visited_locations:
        guard_path[x][y] = ord("X")
      else:
        guard_path[x][y] = grid[x][y]
  return guard_path


def init_grid_from_file(filename: str) -> char[N_ROWS][N_COLUMNS]:
  """
  Récupère la grille depuis le fichier donné en paramètre
  :returns la grille qui ne contient que 3 caractères : '.', '#' et '^' (ou ses dérivés: '<', '>')
  """
  content = ""
  # récupérer le contenu de la grille sans les retours à la ligne
  with open(filename, 'r', encoding='utf8') as file:
    for line in file:
      content += ''.join([symbol for symbol in line if symbol != '\n'])
  # on convertit la grille temporaire en C array pour des questions de performances
  # define x and y as C types to compile for-loop in pure C code
  cdef int x = 0, y = 0
  cdef char[N_ROWS][N_COLUMNS] grid
  for x in range(N_ROWS):
    for y in range(N_COLUMNS):
      index_in_content = x * N_COLUMNS + y
      grid[x][y] = ord(content[index_in_content])
  return grid


def display_grid(grid: char[N_ROWS][N_COLUMNS]) -> None:
  """Fonction qui permet d'afficher la grille sous une forme
  plus lisible que l'affichage par défaut via print
  """
  # define x and y as C types to compile for-loop in pure C code
  cdef int x = 0, y = 0
  for x in range(N_ROWS):
    for y in range(N_COLUMNS):
      print(chr(grid[x][y]), end='')
    print()

