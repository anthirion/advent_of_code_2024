from command_line_parser import get_arguments_from_command_line

# positions des lettres correspondant aux occurences du mot 'XMAS'
match_positions: list[tuple[int, int]] = []


def remove_incorrect_positions(times):
  for _ in range(times):
    if match_positions:
      del match_positions[-1]

################################## PART 1 ##################################


def search_from_position(grid: list[list[str]], position: tuple[int, int], keyword: str) -> int:
  """Cherche le nombre d'occurences du keyword à partir de la position donnée
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
  start_line, start_column = position
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
      # au moins une occurence de xmas a été trouvée
      match_positions.append(position)
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


def cross_search_from_position(grid: list[list[str]], position: tuple[int, int], keyword: str) -> int:
  """Cherche le nombre d'occurences du keyword en forme de croix à partir de la position donnée
  :param grid: grille de recherche
  :param position : position à partir de laquelle chercher le keyword
  :param keyword : le keyword à chercher
  :returns nombre d'occurences du keyword trouvées
  """
  xmas_local_count = 0
  keyword_length = len(keyword)
  directions = [(-1, -1), (1, 1),     # diagonale descendante
                (1, -1), (-1, 1),     # diagonale montante
                ]
  start_line, start_column = position
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
        remove_incorrect_positions(keyword_index)
        break
    if (keyword_index == keyword_length - 1 and
            current_letter == keyword[keyword_index]):
      xmas_local_count += 1
  return xmas_local_count


def count_crossed_mas_occurrences(grid: list[list[str]], keyword: str) -> int:
  xmas_count = 0
  max_lines, max_columns = len(grid), len(grid[0])
  for line in range(max_lines):
    for column in range(max_columns):
      if grid[line][column] == keyword[0]:
        position = (line, column)
        match_positions.append(position)
        xmas_count += cross_search_from_position(grid, position, keyword)
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
  new_grid = build_grid_with_match_positions(grid)
  display_grid(new_grid)
