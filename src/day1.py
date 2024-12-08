from command_line_parser import get_arguments_from_command_line

################################## PART 1 ##################################

def distance(a: int, b: int) -> int:
    return max(a, b) - min(a, b)

def list_similarity(l1: list[int], l2: list[int]) -> int:
    """
    La similarité de 2 listes est calculée en additionnant les distances entre les éléments
    des 2 listes
    """
    assert len(l1) == len(l2)
    l1.sort()
    l2.sort()
    return sum(distance(i, j) for i, j in zip(l1, l2))

################################## PART 2 ##################################

def second_similarity_score(l1: list[int], l2: list[int]) -> int:
    """
    Ce second score de similarité est calculé en additionnant chaque nombre de la liste 1
    après l'avoir multiplié par le nombre de fois qu'il apparaît dans la liste 2
    """
    # nombre d'occurences dans la liste l2 des éléments de l1
    occurences = [l2.count(element) for element in l1]
    return sum(element*occurences for element, occurences in zip(l1, occurences))


############################## LAUNCH PROGRAM ##############################

def build_lists(filename: str) -> tuple[list, list]:
    """Construit les listes à réconcilier à partir
    d'un fichier dont la première colonne représente la première
    liste et la deuxième colonne la deuxième liste
    :param filename: nom du fichier à parser
    :return listes l1 et l2 construites à partir du fichier
    """
    l1, l2 = [], []
    with open(filename, 'r', encoding='utf8') as file:
        for line in file:
            # ignorer les lignes vides
            if line:
                # s'assurer qu'il y a bien 2 colonnes par ligne
                list_of_elements: list[str] = line.split()
                assert len(list_of_elements) == 2
                element_of_first_list, element_of_second_list = list_of_elements
                l1.append(int(element_of_first_list))
                l2.append(int(element_of_second_list))
    if len(l1) == 0 and len(l2) == 0:
        print("WARNING: the two lists are empty. It means that the file is probably empty.")
    return l1, l2

if __name__ == "__main__":
    filename, part = get_arguments_from_command_line()
    l1, l2 = build_lists(filename)
    if part == 1:
        print("List similarity:", list_similarity(l1, l2))
    elif part == 2:
        print("Second list similarity score:", second_similarity_score(l1, l2))