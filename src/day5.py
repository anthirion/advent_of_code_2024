from command_line_parser import get_arguments_from_command_line
import re
from collections import defaultdict
from typing import Iterator

################################## PART 1 ##################################


def build_rule_dependencies(rules: list[str]) -> dict[int, list[str]]:
  """Construit les dépendances de chaque page en fonction de la liste des
  règles. Par exemple, pour la page 75, la fonction indiquera toutes les pages
  qui doivent être imprimées APRES la page 75 (les pages à droite du symbole |)
  :param rules: liste des règles
  :returns un dictionnaire dont la clé est une page de màj et la valeur est la liste
  des dépendances de cette page
  """
  # on utilise un defaultDict pour ne pas avoir à vérifier à chaque fois que la clé
  # existe
  rules_dependencies = defaultdict(list)
  for rule in rules:
    # extraction des 2 nombres présents dans chaque règle
    page, dependency = re.findall(pattern=r'\d+', string=rule)
    # pas besoin de vérifier que la clé existe grâce au defaultDict
    rules_dependencies[page].append(dependency)
  return rules_dependencies


def update_is_correct(update_pages: list[str], rules_dependencies: dict[int, list[str]]) -> bool:
  """Vérifie que l'update répond bien aux règles définies
  :param update: liste de pages à imprimer pour faire l'update
  :returns True si l'update est correcte, False sinon
  """
  # la liste d'updates est parcourue en sens inverse
  for page_index in range(len(update_pages) - 1, -1, -1):
    page = update_pages[page_index]
    dependencies = rules_dependencies[page]
    for dependency in dependencies:
      if dependency in update_pages[:page_index]:
        return False
  return True


def sum_middle_page_numbers_p1(updates: list[str], rules: list[str]) -> int:
  """Somme les numéros de pages médians de toutes les màj correctes"""
  sum = 0
  rules_dependencies = build_rule_dependencies(rules)
  for update in updates:
    update_pages = update.split(',')
    if update_is_correct(update_pages, rules_dependencies):
      sum += int(update_pages[len(update_pages) // 2])
  return sum


################################## PART 2 ##################################

############################## LAUNCH PROGRAM ##############################


def get_rules_and_updates_from_file(filename: str) -> tuple[list[str], list[str]]:
  """
  Récupère les règles et les màj du fichier donné en paramètre
  :returns un tuple de 2 listes: la première étant la liste des règles et la
  deuxième la liste des màj
  """
  rules: list[str] = []
  updates: list[str] = []
  with open(filename, 'r', encoding='utf8') as file:
    for line in file:
      if '|' in line:
        # le [:-1] permet de ne pas prendre en compte le '\n
        rules.append(line[:-1])
      elif line != '\n':
        updates.append(line[:-1])
  return rules, updates


if __name__ == "__main__":
  filename, part = get_arguments_from_command_line()
  rules, updates = get_rules_and_updates_from_file(filename)
  if part == 1:
    print("Sum of median page numbers for correct updates only:",
          sum_middle_page_numbers_p1(updates, rules))
  elif part == 2:
    print("Part 2 to be implemented")
