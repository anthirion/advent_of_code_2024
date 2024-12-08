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

def is_safe(report: list[int]) -> bool:
    if is_monotonic(report):
        # vérifier que la distance entre 2 éléments adjacents est entre 1 et 3
        for i in range(len(report)-1):
            distance = abs(report[i] - report[i+1])
            if not 1 <= distance <= 3:
                return False
        return True
    return False

def count_safe_reports(data: list[list[int]]) -> int:
    return sum(map(is_safe, data))

if __name__ == "__main__":
    data = [[7, 6, 4, 2, 1],
            [1, 2, 7, 8, 9],
            [9, 7, 6, 2, 1],
            [1, 3, 2, 4, 5],
            [8, 6, 4, 4, 1],
            [1, 3, 6, 7, 9]]
    print("Number of safe reports in data:", count_safe_reports(data))