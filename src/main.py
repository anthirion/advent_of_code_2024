"""
Ce script donne une solution au problème du jour 6. 
Pour gagner en performance, les fonctions utiles ont été traduites en C
avec l'aide de Cython (fonctions écrites dans le module day6.pyx).
"""
import time
from command_line_parser import get_arguments_from_command_line
from day6 import (
    init_grid_from_file, build_guard_path,
    display_grid, determine_visited_locations, count_obstructions,
    count_unique_locations, determine_obstructions_locations,
)

if __name__ == "__main__":
  filename, part = get_arguments_from_command_line()
  start_time = time.time()
  grid = init_grid_from_file(filename)
  if part == 1:
    visited_locations = determine_visited_locations(grid)
    unique_locations_count = count_unique_locations(visited_locations)
    # ne pas calculer ni afficher le chemin du garde si la map est trop grande
    guard_path = build_guard_path(grid, visited_locations)
    display_grid(guard_path)
    print("Number of locations visited:", unique_locations_count)
  elif part == 2:
    obstructions_positions = determine_obstructions_locations(grid)
    print("Number of possible locations for obstacle:",
          count_obstructions(obstructions_positions))
  print(f"Elapsed time: {time.time() - start_time} s")
