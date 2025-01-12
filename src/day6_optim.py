"""
Ce module et le module day6 sont tous les 2 une solution au problème
du jour 6. Ce module implémente la solution à l'aide de numpy pour
améliorer les performances.
Dans les grandes lignes, les différences sont :
- la grille est implémentée sous forme de ndarray
- la liste des positions est aussi un ndarray
- la liste des obstacles est un ndarray
- les fonctions natives de python (sum, len, set) sont remplacées par des fonctions numpy
- une classe Guard a été créée pour stocker sa position et sa direction sans avoir à passer
un tuple à chaque fois
"""

from command_line_parser import get_arguments_from_command_line
import time
import numpy as np
from numpy.typing import NDArray


class Guard:
  def __init__(self, grid: NDArray[np.str_]) -> None:
    self.grid = grid
    self.n_lines, self.n_columns = self.grid.shape
    self.guard_symbols = ['^', '<', '>']
    self.obstacle_symbols = ['#', 'O']
    # Déterminer la position et la direction de départ du garde
    # La position initiale du garde est indiquée par les symboles '^', '<' ou '>'
    # on cherche si la grille contient au moins un de ces symboles
    init_positions = [np.argwhere(self.grid == symbol)
                      for symbol in self.guard_symbols]
    # on retient le seul array non-vide qui indique la position de départ du garde
    self.position: NDArray[np.int_] = np.concatenate(init_positions)[0]
    # En fonction du symbole du garde ('^', '<' ou '>'), la direction de départ est droite, gauche ou haut
    guard_symbol = self.grid[tuple(self.position)]
    if guard_symbol == self.guard_symbols[0]:
      self.direction = np.array([-1, 0])
    elif guard_symbol == self.guard_symbols[1]:
      self.direction = np.array([0, -1])
    elif guard_symbol == self.guard_symbols[2]:
      self.direction = np.array([0, 1])
    # Si le garde commence avec un obstacle devant lui, sa direction est modifiée de telle sorte qu'il
    # n'ait pas d'obstacle devant lui
    while self.obstacle_ahead():
      self.change_direction()

  def obstacle_ahead(self) -> bool:
    next_position = self.position + self.direction
    if 0 <= next_position[0] < self.n_lines and 0 <= next_position[1] < self.n_columns:
      if self.grid[tuple(next_position)] in self.obstacle_symbols:
        return True
      else:
        return False
    else:
      raise IndexError("Le garde est sorti de la grille")

  def change_direction(self) -> None:
    """Lorsqu'un obstacle est rencontré, cette fonction détermine la nouvelle direction
    qui est l'ancienne direction tournée de 90° dans le sens des aiguilles d'une montre
    """
    if np.all(self.direction == (0, 1)):
      # si le garde allait sur la droite, il doit aller vers le bas
      self.direction = np.array([1, 0])
    elif np.all(self.direction == (0, -1)):
      # si le garde allait sur la gauche, il doit aller vers le haut
      self.direction = np.array([-1, 0])
    elif np.all(self.direction == (-1, 0)):
      # si le garde allait vers le haut, il doit aller à droite
      self.direction = np.array([0, 1])
    elif np.all(self.direction == (1, 0)):
      # si le garde allait en bas, aller il doit à gauche
      self.direction = np.array([0, -1])

  def move(self) -> None:
    while self.obstacle_ahead():
      self.change_direction()
    # on vérifie que le garde ne sort pas de la grille dans la méthode obstacle_ahead
    self.position = self.position + self.direction

################################## PART 1 ##################################


def determine_visited_locations(guard: Guard) -> list[NDArray[np.int_]]:
  visited_locations: list[NDArray[np.int_]] = []
  while True:
    try:
      location_is_visited = \
          np.any([np.array_equal(guard.position, l)
                 for l in visited_locations])
      if not location_is_visited:
        visited_locations.append(guard.position)
      guard.move()
    except IndexError:
      # le garde sort de la grille
      break
  return visited_locations


def count_unique_locations(visited_locations: list[NDArray[np.int_]]) -> int:
  return len(visited_locations)


################################## PART 2 ##################################

def count_obstacles(grid: NDArray[np.str_]) -> int:
  """
  Compte le nombre d'obstacles présents dans la grille
  """
  obstacle_symbols = ('#', 'O')
  return sum(grid[x][y] in obstacle_symbols for x in range(len(grid))
             for y in range(len(grid[0])))


def stuck_in_loop(grid: NDArray[np.str_], start_position: tuple[int, int],
                  start_direction: tuple[int, int]) -> bool:
  """
  Le garde est bloqué s'il repasse par un emplacement qu'il a déjà visité avec la MEME
  direction
  """
  previous_positions: list[tuple[int, int]] = []
  previous_directions: list[tuple[int, int]] = []
  stuck = False
  position, direction = start_position, start_direction
  nb_lines, nb_columns = len(grid), len(grid[0])
  while (0 <= position[0] < nb_lines and 0 <= position[1] < nb_columns):
    previous_positions.append(position)
    previous_directions.append(direction)
    position = (position[0] + direction[0], position[1] + direction[1])
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


def determine_obstructions_locations(grid: NDArray[np.str_]) -> list[tuple[int, int]]:
  """Détermine les positions où un obstacle peut être mis pour bloquer
  le garde dans une boucle infinie
  :returns liste des positions de l'obstacle 
  """
  obstructions_positions: list[tuple[int, int]] = []
  visited_locations = determine_visited_locations(grid)
  no_locations_to_visit = len(visited_locations)
  start_position, start_direction = determine_start_position_and_direction(
      grid)
  for index, position in enumerate(visited_locations[1:]):
    if index % 10 == 0:
      print(f"Progression: {index / no_locations_to_visit * 100} %")
    x, y = position
    old_value = grid[x][y]
    grid[x][y] = 'O'
    if stuck_in_loop(grid, start_position, start_direction):
      if position not in obstructions_positions:
        obstructions_positions.append(position)
    grid[x][y] = old_value
  return obstructions_positions


def count_obstructions(obstructions_positions: list[tuple[int, int]]) -> int:
  return len(obstructions_positions)

############################## LAUNCH PROGRAM ##############################


def build_guard_path(grid: NDArray[np.str_], visited_locations: list[tuple[int, int]]) -> list[list[str]]:
  """Construit une nouvelle grille où le chemin par où est passé le guard est indiqué par des 'X'
  :returns nouvelle grille avec le chemin du guard et le nombre de cases différentes qu'a visité
    le guard
  """
  guard_path = np.copy(grid)
  for position in visited_locations:
    guard_path[tuple(position)] = 'X'
  return guard_path


def init_grid_from_file(filename: str) -> NDArray[np.str_]:
  """
  Récupère la grille depuis le fichier donné en paramètre
  :returns la grille qui ne contient que 3 caractères : '.', '#' et '^' (ou ses dérivés: '<', '>')
  """
  # ici on représente la grille sous forme de liste et pas d'un ndarray
  # car on ne connait pas la shape de la grille avant d'avoir lu le fichier
  tmp_grid: list[list[str]] = []
  with open(filename, 'r', encoding='utf8') as file:
    for line in file:
      tmp_grid.append([character for character in line if character != '\n'])
  n_lines, n_columns = len(tmp_grid), len(tmp_grid[0])
  grid = np.full((n_lines, n_columns), '.')
  for line in range(n_lines):
    for col in range(n_columns):
      grid[line, col] = tmp_grid[line][col]
  return grid


def display_grid(grid: NDArray[np.str_]) -> None:
  """Fonction qui permet d'afficher la grille sous une forme
  plus lisible que l'affichage par défaut via print
  """
  for line in range(grid.shape[0]):
    row_elements = [grid[line, col] for col in range(grid.shape[1])]
    print(*row_elements)


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
