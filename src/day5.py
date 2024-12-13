from command_line_parser import get_arguments_from_command_line
import re
from collections import defaultdict

################################## PART 1 ##################################


def build_rule_dependencies(rules: list[str]) -> dict[str, list[str]]:
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


def update_is_correct(update_pages: list[str], rules_dependencies: dict[str, list[str]]) -> bool:
  """Vérifie que l'update répond bien aux règles définies
  :param update: liste de pages à imprimer pour faire l'update
  :returns True si l'update est correcte, False sinon
  """
  assert len(update_pages) > 0
  # la liste d'updates est parcourue en sens inverse
  for page_index in range(len(update_pages) - 1, -1, -1):
    page = update_pages[page_index]
    if page in rules_dependencies.keys():
      dependencies = rules_dependencies[page]
      for dependency in dependencies:
        if dependency in update_pages[:page_index]:
          return False
  return True


def sum_middle_page_numbers_p1(updates: list[str], rules: list[str]) -> int:
  """Somme les numéros de pages médians de toutes les màj correctes"""
  assert len(updates) > 0 and len(rules) > 0
  sum = 0
  rules_dependencies = build_rule_dependencies(rules)
  for update in updates:
    update_pages = update.split(',')
    if update_is_correct(update_pages, rules_dependencies):
      sum += int(update_pages[len(update_pages) // 2])
  return sum


################################## PART 2 ##################################

def swap(liste: list[str], index1: int, index2: int) -> None:
  if 0 <= index1 < len(liste) and 0 <= index2 < len(liste):
    liste[index1], liste[index2] = liste[index2], liste[index1]
  else:
    raise IndexError


def reorder_incorrect_update(update_pages: list[str], rules_dependencies: dict[str, list[str]]) -> None:
  """Remet une màj incorrecte dans un ordre correct
  :returns liste des pages de la màj dans le bon ordre
  ATTENTION: la liste update_pages est modifiée EN PLACE
  """
  assert len(update_pages) > 0
  while not update_is_correct(update_pages, rules_dependencies):
    for page_index in range(len(update_pages) - 1, -1, -1):
      page = update_pages[page_index]
      if page in rules_dependencies.keys():
        dependencies = rules_dependencies[page]
        for dependency in dependencies:
          try:
            dependency_index = update_pages.index(dependency, 0, page_index)
            swap(update_pages, dependency_index, page_index)
          except ValueError:
            # la dépendance n'a pas été trouvée
            continue


def sum_middle_page_numbers_p2(updates: list[str], rules: list[str]) -> int:
  """Somme les numéros de pages médians de toutes les màj incorrectes"""
  sum = 0
  rules_dependencies = build_rule_dependencies(rules)
  for update in updates:
    update_pages = update.split(',')
    if not update_is_correct(update_pages, rules_dependencies):
      reorder_incorrect_update(update_pages, rules_dependencies)
      sum += int(update_pages[len(update_pages) // 2])
  return sum

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
    print("Sum of median page numbers for incorrect updates only:",
          sum_middle_page_numbers_p2(updates, rules))
