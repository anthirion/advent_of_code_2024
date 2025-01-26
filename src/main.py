"""
Ce script donne une solution au problème du jour 6. 
Pour gagner en performance, les fonctions utiles ont été traduites en C
avec l'aide de Cython (fonctions écrites dans le module day6_o.pyx).
"""
import time
from command_line_parser import get_arguments_from_command_line
from day6_o import (
    init_grid_from_file, determine_visited_locations, count_obstructions,
    count_unique_locations, determine_obstructions_locations,
)

if __name__ == "__main__":
  filename, part = get_arguments_from_command_line()
  start_time = time.time()
  init_grid_from_file(filename)
  if part == 1:
    visited_locations = determine_visited_locations()
    unique_locations_count = count_unique_locations(visited_locations)
    print("Number of locations visited:", unique_locations_count)
  elif part == 2:
    obstructions_positions = determine_obstructions_locations()
    print("Number of possible locations for obstacle:",
          count_obstructions(obstructions_positions))
  print(f"Elapsed time: {time.time() - start_time} s")
