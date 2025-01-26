"""
ATTENTION : bien vérifier que les valeurs de N_ROWS et N_COLUMNS sont correctes
"""
# global variables
DEF N_ROWS = 130
DEF N_COLUMNS = 130
obstacle_symbols = ('#', 'O')
guard_symbols = ('^', '<', '>')
cdef char[N_ROWS][N_COLUMNS] grid

################################## PART 1 ##################################


cpdef bint obstacle_ahead((int, int) position, (int, int) direction):
  next_position = (position[0] + direction[0], position[1] + direction[1])
  if 0 <= next_position[0] < N_ROWS and 0 <= next_position[1] < N_COLUMNS:
    next_x, next_y = next_position
    if chr(grid[next_x][next_y]) in obstacle_symbols:
      return True
  return False


cpdef (int, int) change_direction((int, int) direction):
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


cpdef ((int, int), (int, int)) determine_start_position_and_direction():
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
  while obstacle_ahead(init_position, init_direction):
    init_direction = change_direction(init_direction)
  return init_position, init_direction


cpdef list determine_visited_locations():
  """Détermine le chemin du garde"""
  # ne pas changer visited_locations en set car il doit y avoir des doublons
  # dans la liste pour la partie 2
  visited_locations = []
  position, direction = determine_start_position_and_direction()
  while 0 <= position[0] < N_ROWS and 0 <= position[1] < N_COLUMNS:
    visited_locations.append(position)
    position = (position[0] + direction[0], position[1] + direction[1])
    while obstacle_ahead(position, direction):
      direction = change_direction(direction)
  return visited_locations


cpdef int count_unique_locations(list visited_locations):
  return len(set(visited_locations))


################################## PART 2 ##################################

# bint is equivalent to bool
cpdef bint stuck_in_loop((int, int) start_position, (int, int) start_direction):
  """
  Le garde est bloqué s'il repasse par un emplacement qu'il a déjà visité avec la MEME
  direction
  """
  # pour accélérer la fonction, remplacer les listes previous_positions et previous_directions
  # par un dictionnaire dont la clé est la position et la valeur est la direction
  cdef dict history = {}
  stuck = False
  position, direction = start_position, start_direction
  while (0 <= position[0] < N_ROWS and 0 <= position[1] < N_COLUMNS):
    history[position] = direction
    position = (position[0] + direction[0], position[1] + direction[1])
    while obstacle_ahead(position, direction):
      direction = change_direction(direction)
    # éviter les try-except couteux en Cython et les remplacer par des if
    if position in history and history[position] == direction:
        stuck = True
        break
  return stuck


cpdef set determine_obstructions_locations():
  """Détermine les positions où un obstacle peut être mis pour bloquer
  le garde dans une boucle infinie
  :returns liste des positions de l'obstacle 
  """
  cdef set obstructions_positions = set()
  visited_locations = determine_visited_locations()
  nb_locations_to_visit = len(visited_locations)
  start_position, start_direction = determine_start_position_and_direction()
  for position in visited_locations[1:]:
    x, y = position
    old_value = chr(grid[x][y])
    grid[x][y] = b'O'
    if stuck_in_loop(start_position, start_direction):
      obstructions_positions.add(position)
    grid[x][y] = ord(old_value)
  return obstructions_positions


cpdef int count_obstructions(set obstructions_positions):
  return len(obstructions_positions)

############################## LAUNCH PROGRAM ##############################


cpdef void init_grid_from_file(str filename):
  """
  Récupère le contenu de la grille depuis le fichier donné en paramètre
  """
  content = ""
  # récupérer le contenu de la grille sans les retours à la ligne
  with open(filename, 'r', encoding='utf8') as file:
    for line in file:
      content += ''.join([symbol for symbol in line if symbol != '\n'])
  # on convertit la grille temporaire en C array pour des questions de performances
  # define x and y as C types to compile for-loop in pure C code
  cdef int x = 0, y = 0
  for x in range(N_ROWS):
    for y in range(N_COLUMNS):
      index_in_content = x * N_COLUMNS + y
      grid[x][y] = ord(content[index_in_content])

cpdef void display_grid():
  """Fonction qui permet d'afficher la grille sous une forme
  plus lisible que l'affichage par défaut via print
  """
  # define x and y as C types to compile for-loop in pure C code
  cdef int x = 0, y = 0
  for x in range(N_ROWS):
    for y in range(N_COLUMNS):
      print(chr(grid[x][y]), end='')
    print()

