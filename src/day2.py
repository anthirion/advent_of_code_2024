from command_line_parser import get_arguments_from_command_line

################################## PART 1 ##################################

def is_increasing(l1: list[int]) -> bool:
    """Vérifie que la liste est croissante, càd que chaque élément de la liste
    est supérieur ou égal à l'élément précédent
    :param l1: liste à vérfier
    :return true si la liste est croissante, false sinon
    """
    for i in range(len(l1)-1):
        if l1[i] > l1[i+1]:
            return False
    return True

def is_decreasing(l1: list[int]) -> bool:
    """Vérifie que la liste est décroissante, càd que chaque élément de la liste
    est inférieur ou égal à l'élément précédent
    :param l1: liste à vérfier
    :return true si la liste est décroissante, false sinon
    """
    for i in range(len(l1)-1):
        if l1[i] < l1[i+1]:
            return False
    return True

def is_monotonic(l1: list[int]) -> bool:
    """Vérifie que la liste est monotone, càd soit croissante soit décroissante
    :param l1: liste à vérfier
    :return true si la liste est monotone, false sinon
    """
    return is_increasing(l1) or is_decreasing(l1)

def is_safe_without_dampener(report: list[int]) -> bool:
    if is_monotonic(report):
        # vérifier que la distance entre 2 éléments adjacents est entre 1 et 3
        for i in range(len(report)-1):
            distance = abs(report[i] - report[i+1])
            if not 1 <= distance <= 3:
                return False
        return True
    return False

def count_safe_reports_without_dampener(data: list[list[int]]) -> int:
    return sum(map(is_safe_without_dampener, data))

################################## PART 2 ##################################

def is_safe_with_dampener(report: list[int]) -> bool:
    if is_safe_without_dampener(report):
        return True
    else:
        # retirer les éléments un à un du 1er au dernier puis vérifier si
        # en retirant cet élément, le rapport est correct
        index = 0
        while True:
            try:
                test_report = report.copy()
                del test_report[index]
                if is_safe_without_dampener(test_report):
                    return True
                index += 1
            except IndexError:
                # la fin de la liste est atteinte
                return False

def count_safe_reports_with_dampener(data: list[list[int]]) -> int:
    return sum(map(is_safe_with_dampener, data))

############################## LAUNCH PROGRAM ##############################

def get_data_from_file(filename: str) -> list[list[int]]:
    """
    Récupère les rapports dans le fichier donné en paramètre
    """
    data = []
    with open(filename, 'r', encoding='utf8') as file:
        for line in file:
            report = [int(level) for level in line.split()]
            data.append(report)
    if len(data) == 0:
        print("WARNING: there is no data. It means that the file is probably empty.")
    return data

if __name__ == "__main__":
    filename, part = get_arguments_from_command_line()
    data = get_data_from_file(filename)
    if part == 1:
        print("Number of safe reports:", count_safe_reports_without_dampener(data))
    elif part == 2:
        print("Number of safe reports:", count_safe_reports_with_dampener(data))