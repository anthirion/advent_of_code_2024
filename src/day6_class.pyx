"""
Ce module est une optimisation du module day6.py.
Dans les grandes lignes, les optimisations qui ont été faites sont :
- les listes (grille, positions, obstacles) sont des C arrays
- une classe Guard a été créée pour stocker sa position et sa direction sans avoir à passer
un tuple à chaque fois
- les fonctions natives de python (sum, len, set) sont remplacées par des fonctions numpy
"""

from command_line_parser import get_arguments_from_command_line
import time

# global variables
DEF N_ROWS = 130
DEF N_COLUMNS = 130

class NoGuardFoundInTheGridError(Exception):
  pass

class OutOfGridError(Exception):
  def __init__(self, position: Position):
    self.position = position
  
  def message(self):
    print(f"La position {self.position} est en dehors de la grille")

class Direction:
  def __init__(self, direction: tuple[int, int] = (0, 0)) -> None:
    self.dx = direction[0]
    self.dy = direction[1]

  def __eq__(self, other: Direction) -> bool:
    return self.dx == other.dx and self.dy == other.dy

  def __hash__(self) -> int:
    return hash((self.dx, self.dy))

class Position:
  def __init__(self, position: tuple[int, int] = (0, 0)) -> None:
    self.x = position[0]
    self.y = position[1]

  def in_grid(self) -> bool:
    return 0 <= self.x < N_ROWS and 0 <= self.y < N_COLUMNS

  def __eq__(self, other: Position) -> bool:
    return self.x == other.x and self.y == other.y

  def __hash__(self) -> int:
    return hash((self.x, self.y))

cdef class Guard:
  guard_symbols = ['^', '<', '>']
  obstacle_symbols = ['#', 'O']

  def __init__(self, grid: char[N_ROWS][N_COLUMNS]) -> None:
    self.grid = grid
    self.position = Position()
    self.direction = Direction()
    self.init_position_and_direction()
    self.start_position = self.position
    self.start_direction = self.direction

  def init_position_and_direction(self) -> None:
    """Détermine la position de départ du garde et sa direction. La position initiale du garde peut être indiquée
    par les symboles '^', '<' ou '>'. En fonction du symbole, la direction peut être droite, gauche, haut ou bas.
    """
    # define x and y as C types to compile for-loop in pure C code
    cdef int x = 0, y = 0
    while (0 <= x < N_ROWS and 0 <= y < N_COLUMNS
          and self.grid[x][y] not in self.guard_symbols):
      x += 1
      y += 1
    if self.grid[x][y] in self.guard_symbols:
      self.position = Position((x, y))
      current_character = self.grid[x][y]
      if current_character == self.guard_symbols[0]:
        self.direction = Direction((-1, 0))
      elif current_character == self.guard_symbols[1]:
        self.direction = Direction((0, -1))
      elif current_character == self.guard_symbols[2]:
        self.direction = Direction((0, 1))
      # changer la direction du garde pour que celui-ci ne soit pas
      # devant un obstacle au commencement du parcours
      while self.obstacle_ahead():
        self.change_direction()
    else:
      raise NoGuardFoundInTheGridError()


  def obstacle_ahead(self) -> bool:
    # on considère ici que la next position est dans la grid
    # ceci est vérifié par la méthode in_grid
    next_position = Position(self.position.x + self.direction.dx,
                              self.position.y + self.direction.dy)
    return self.grid[next_position.x][next_position.y] in self.obstacle_symbols

  def change_direction(self) -> None:
    """Lorsqu'un obstacle est rencontré, la nouvelle direction du guarde est l'ancienne
    direction tournée de 90° dans le sens des aiguilles d'une montre
    """
    if self.direction == Direction((0, 1)):
      # si le garde allait sur la droite, il doit aller vers le bas
      self.direction = Direction((1, 0))
    elif self.direction == Direction((0, -1)):
      # si le garde allait sur la gauche, il doit aller vers le haut
      self.direction = Direction((-1, 0))
    elif self.direction == Direction((-1, 0)):
      # si le garde allait vers le haut, il doit aller à droite
      self.direction = Direction((0, 1))
    elif self.direction == Direction((1, 0)):
      # si le garde allait en bas, aller il doit à gauche
      self.direction = Direction((0, -1))

  def move(self) -> None:
    next_position = Position(self.position.x + self.direction.dx,
                              self.position.y + self.direction.dy)
    if next_position.in_grid():
      while self.obstacle_ahead():
        self.change_direction()
      self.position = Position(self.position.x + self.direction.dx,
                                self.position.y + self.direction.dy)
    else:
      raise OutOfGridError(next_position)

################################## PART 1 ##################################


def determine_visited_locations(guard: Guard) -> list[Position]:
  visited_locations: list[Position] = []
  while True:
    try:
      visited_locations.append(guard.position)
      guard.move()
    except OutOfGridError:
      # le garde sort de la grille
      break
  return visited_locations


def count_unique_locations(visited_locations: list[Position]) -> int:
  return len(set(visited_locations))


################################## PART 2 ##################################

def guard_already_passed_here(guard: Guard, previous_positions: list[Position],
                        previous_directions: list[Direction]):
  try:
    position_index = previous_positions.index(guard.position)
    if previous_directions[position_index] == guard.direction:
      return True
    else:
      return False
  except ValueError:
    # la position courante n'a pas été trouvée dans les anciennes positions
    return False

def stuck_in_loop(guard: Guard) -> bool:
  """
  Le garde est bloqué s'il repasse par un emplacement qu'il a déjà visité avec la MEME
  direction
  """
  previous_positions: list[Position] = []
  previous_directions: list[Direction] = []
  stuck = False
  guard.position = guard.start_position
  guard.direction = guard.start_direction
  while True:
    try:
      previous_positions.append(guard.position)
      previous_directions.append(guard.direction)
      guard.move()
      # vérifier que le garde n'est pas déjà passé
      if guard_already_passed_here(guard, previous_positions, previous_directions):
        stuck = True
        break
    except OutOfGridError:
      # le garde sort de la grille donc il n'est pas bloqué
      break
  return stuck


def determine_obstructions_locations(guard: Guard) -> list[Position]:
  """Détermine les positions où un obstacle peut être mis pour bloquer
  le garde dans une boucle infinie
  :returns liste des positions de l'obstacle 
  """
  obstructions_positions: list[Position] = []
  visited_locations = determine_visited_locations(guard)
  nb_locations_to_visit = len(visited_locations)
  for index, position in enumerate(visited_locations[1:]):
    if index % 30 == 0:
      print(f"Progression: {index / nb_locations_to_visit * 100} %")
    old_value = grid[position.x][position.y]
    grid[position.x][position.y] = b'O'
    if stuck_in_loop(guard):
      if position not in obstructions_positions:
        obstructions_positions.append(position)
    grid[position.x][position.y] = old_value
  return obstructions_positions


def count_obstructions(obstructions_positions: list[tuple[int, int]]) -> int:
  return len(obstructions_positions)

############################## LAUNCH PROGRAM ##############################


def build_guard_path(grid: char[N_ROWS][N_COLUMNS], visited_locations: list[Position]) -> list[list[str]]:
  """Construit une nouvelle grille où le chemin par où est passé le guard est indiqué par des 'X'
  :returns nouvelle grille avec le chemin du guard et le nombre de cases différentes qu'a visité
    le guard
  """
  # define x and y as C types to compile for-loop in pure C code
  cdef int x = 0, y = 0
  cdef char[N_ROWS][N_COLUMNS] guard_path
  for x in range(N_ROWS):
    for y in range(N_COLUMNS):
      if Position((x, y)) in visited_locations:
        guard_path[x][y] = b'X'
      else:
        guard_path[x][y] = grid[x][y]
  return guard_path


def init_grid_from_file(filename: str) -> char[N_ROWS][N_COLUMNS]:
  """
  Récupère la grille depuis le fichier donné en paramètre
  :returns la grille qui ne contient que 3 caractères : '.', '#' et '^' (ou ses dérivés: '<', '>')
  """
  with open(filename, 'r', encoding='utf8') as file:
    content = file.read()
  # on convertit la grille temporaire en C array pour des questions de performances
  # define x and y as C types to compile for-loop in pure C code
  cdef int x = 0, y = 0
  cdef char[N_ROWS][N_COLUMNS] grid
  for x in range(N_ROWS):
    for y in range(N_COLUMNS):
      index_in_content = x * N_ROWS + N_COLUMNS
      grid[x][y] = content[index_in_content]
  return grid


def display_grid(grid: char[N_ROWS][N_COLUMNS]) -> None:
  """Fonction qui permet d'afficher la grille sous une forme
  plus lisible que l'affichage par défaut via print
  """
  # define x and y as C types to compile for-loop in pure C code
  cdef int x = 0, y = 0
  for x in range(N_ROWS):
    for y in range(N_COLUMNS):
      print(grid[x][y], end='\t')
    print()


if __name__ == "__main__":
  filename, part = get_arguments_from_command_line()
  start_time = time.time()
  grid = init_grid_from_file(filename)
  guard = Guard(grid)
  if part == 1:
    visited_locations = determine_visited_locations(guard)
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
