from command_line_parser import get_arguments_from_command_line

################################## PART 1 ##################################
# global variables
keyword = "XMAS"
keyword_length = len(keyword)


def search_from_position(grid: list[list[str]], position: tuple[int, int]) -> int:
    """Cherche le nombre d'occurences du keyword à partir de la position donnée
    On peut avoir au plus 8 occurences (keyword à l'endroit, à l'envers, à l'horizontale,
    à la verticale ou en diagonale)
    :param grid: grille de recherche
    :param position : position à partir de laquelle chercher le keyword
    :returns nombre d'occurences du keyword trouvées
    """
    xmas_local_count = 0
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
                if current_letter != keyword[keyword_index]:
                    break
            else:
                break
        if (keyword_index == keyword_length - 1 and
                current_letter == keyword[keyword_index]):
            xmas_local_count += 1
    return xmas_local_count


def count_xmas_occurrences(grid: list[list[str]]) -> int:
    xmas_count = 0
    max_lines, max_columns = len(grid), len(grid[0])
    for line in range(max_lines):
        for column in range(max_columns):
            if grid[line][column] == keyword[0]:
                position = (line, column)
                xmas_count += search_from_position(grid, position)
    return xmas_count

################################## PART 2 ##################################

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


def display_grid(grid):
    for line in grid:
        list_of_letters = [letter for letter in line]
        print(*list_of_letters)


if __name__ == "__main__":
    filename, part = get_arguments_from_command_line()
    grid = build_grid_from_file(filename)
    if part == 1:
        print("Number of times XMAS appears:", count_xmas_occurrences(grid))
    elif part == 2:
        print("Part 2 to be implemented")
