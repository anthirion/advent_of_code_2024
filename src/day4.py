from command_line_parser import get_arguments_from_command_line

# positions des lettres correspondant aux occurences du mot 'XMAS'
match_positions: list[tuple[int, int]] = []


def remove_incorrect_positions(times):
  for _ in range(times):
    if match_positions:
      del match_positions[-1]

################################## PART 1 ##################################


def search_from_position(grid: list[list[str]], start_position: tuple[int, int], keyword: str) -> int:
  """Cherche le nombre d'occurences du keyword à partir de la position donnée. A la position initiale,
  on a forcément la première lettre du keyword, à savoir 'X' 
  On peut avoir au plus 8 occurences (keyword à l'endroit, à l'envers, à l'horizontale,
  à la verticale ou en diagonale)
  :param grid: grille de recherche
  :param position : position à partir de laquelle chercher le keyword
  :param keyword : le keyword à chercher
  :returns nombre d'occurences du keyword trouvées
  """
  xmas_local_count = 0
  keyword_length = len(keyword)
  directions = [(0, 1), (0, -1),      # droite et gauche
                (1, 0), (-1, 0),      # bas et haut
                (-1, -1), (1, 1),     # diagonale descendante
                (1, -1), (-1, 1),     # diagonale montante
                ]
  start_line, start_column = start_position
  for step_row, step_column in directions:
    for keyword_index in range(1, keyword_length):
      new_line = start_line + step_row * keyword_index
      new_column = start_column + step_column * keyword_index
      if 0 <= new_line < len(grid) and 0 <= new_column < len(grid[0]):
        current_letter: str = grid[new_line][new_column]
        match_positions.append((new_line, new_column))
        if current_letter != keyword[keyword_index]:
          remove_incorrect_positions(keyword_index)
          break
      else:
        remove_incorrect_positions(keyword_index - 1)
        break
    if (keyword_index == keyword_length - 1 and
            current_letter == keyword[keyword_index]):
      xmas_local_count += 1
  if xmas_local_count:
    # au moins une occurence de keyword a été trouvée
    match_positions.append(start_position)
  return xmas_local_count


def count_xmas_occurrences(grid: list[list[str]], keyword: str) -> int:
  xmas_count = 0
  max_lines, max_columns = len(grid), len(grid[0])
  for line in range(max_lines):
    for column in range(max_columns):
      if grid[line][column] == keyword[0]:
        position = (line, column)
        xmas_count += search_from_position(grid, position, keyword)
  return xmas_count

################################## PART 2 ##################################


def found_cross_pattern_from_position(grid: list[list[str]], start_position: tuple[int, int], keyword: str) -> bool:
  """Indique si le pattern MAS en forme de croix est présent à la position donnée.
  A la position initiale, on a forcément la lettre 'A'
  :param grid: grille de recherche
  :param position : position à partir de laquelle chercher le keyword
  :param keyword : le keyword à chercher
  :returns nombre d'occurences du keyword trouvées
  """
  pattern_found = False
  row, column = start_position
  # diagonale descendante
  top_left, center, bottom_right = (-1, -1), (0, 0), (1, 1)
  bottom_left, center, top_right = (1, -1), (0, 0), (-1, 1)
  descending_diagonale = ""
  # on concatène les éléments de la grille de la diagonale descendante dans la variable descending_diagonale
  # cette variable aura pour valeur soit "MAS" soit "SAM" dans le cas où un pattern est trouvé
  for position in (top_left, center, bottom_right):
    step_row, step_column = position
    new_row, new_column = row + step_row, column + step_column
    if not (0 <= new_row < len(grid) and 0 <= new_column < len(grid[0])):
      return False
    descending_diagonale += grid[new_row][new_column]
  ascending_diagonale = ""
  # on concatène les éléments de la grille de la diagonale montante dans la variable ascending_diagonale
  # cette variable aura pour valeur soit "MAS" soit "SAM" dans le cas où un pattern est trouvé
  for position in (bottom_left, center, top_right):
    step_row, step_column = position
    new_row, new_column = row + step_row, column + step_column
    if not (0 <= new_row < len(grid) and 0 <= new_column < len(grid[0])):
      return False
    ascending_diagonale += grid[new_row][new_column]
  # vérifier que la diagonale descendante correspond à "MAS" ou "SAM"
  correct_descending_diagonale = (descending_diagonale == keyword or
                                  descending_diagonale == keyword[::-1])
  # vérifier que la diagonale montante correspond à "MAS" ou "SAM"
  correct_ascending_diagonale = (ascending_diagonale == keyword or
                                 ascending_diagonale == keyword[::-1])
  if sum((correct_descending_diagonale, correct_ascending_diagonale)) == 2:
    pattern_found = True
    # ajouter les positions du pattern
    pattern_positions: list[tuple[int, int]] = [(row + position[0], column + position[1])
                                                for position in (top_left, center, bottom_right, bottom_left, top_right)]
    match_positions.extend(pattern_positions)
  return pattern_found


def count_crossed_mas_occurrences(grid: list[list[str]], keyword: str) -> int:
  xmas_count = 0
  max_lines, max_columns = len(grid), len(grid[0])
  for line in range(max_lines):
    for column in range(max_columns):
      if grid[line][column] == 'A':
        position = (line, column)
        if found_cross_pattern_from_position(grid, position, keyword):
          xmas_count += 1
  return xmas_count


############################## LAUNCH PROGRAM ##############################


def build_grid_from_file(filename: str) -> list[list[str]]:
  """
  Construit une grille de lettres à partir du fichier d'entrée
  """
  grid = []
  with open(filename, 'r', encoding='utf8') as file:
    for line in file:
      grid.append([letter for letter in line if letter != '\n'])
  return grid


def build_grid_with_match_positions(old_grid: list[list[str]]) -> list[list[str]]:
  """Construit une grille où seules les lettres correspondant aux occurences trouvées
  de 'XMAS' sont écrites. Aux autres emplacements, un point est inscrit.
  :param old_grid: grille originelle avec toutes les lettres
  :returns grille avec uniquement les lettres pertinentes
  """
  n_rows, n_columns = len(old_grid), len(old_grid[0])
  new_grid = [['.' for _ in range(n_columns)] for _ in range(n_rows)]
  for position in match_positions:
    line, column = position
    new_grid[line][column] = old_grid[line][column]
  return new_grid


def display_grid(grid: list[list[str]]) -> None:
  """Fonction qui permet d'afficher la grille sous une forme
  plus lisible que l'affichage par défaut via print
  """
  for line in range(len(grid)):
    row_elements = [grid[line][column] for column in range(len(grid[0]))]
    print(*row_elements)


if __name__ == "__main__":
  filename, part = get_arguments_from_command_line()
  grid = build_grid_from_file(filename)
  if part == 1:
    keyword = "XMAS"
    print("Number of times XMAS appears:",
          count_xmas_occurrences(grid, keyword))
  elif part == 2:
    keyword = "MAS"
    print("Number of times crossed MAS appears:",
          count_crossed_mas_occurrences(grid, keyword))
  # ne pas afficher la liste lorsque l'input est trop grand
  # new_grid = build_grid_with_match_positions(grid)
  # display_grid(new_grid)
