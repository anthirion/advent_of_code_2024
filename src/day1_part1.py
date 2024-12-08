import argparse

def distance(a: int, b: int) -> int:
    return max(a, b) - min(a, b)


def reconcile_lists(l1: list[int], l2: list[int]) -> int:
    assert len(l1) == len(l2)
    l1.sort()
    l2.sort()
    return sum(distance(i, j) for i, j in zip(l1, l2))

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
            if line:
                # s'assurer qu'il y a bien 2 colonnes par ligne
                list_of_elements: list[str] = line.split()
                assert len(list_of_elements) == 2
                element_of_first_list, element_of_second_list = list_of_elements
                l1.append(int(element_of_first_list))
                l2.append(int(element_of_second_list))
    return l1, l2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='List reconcialiation',
                    description='Compute the distance between 2 lists')
    parser.add_argument('filename')
    args = parser.parse_args()
    l1, l2 = build_lists(args.filename)
    print("Total distance:", reconcile_lists(l1, l2))