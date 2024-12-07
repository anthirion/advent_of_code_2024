def distance(a: int, b: int):
    return max(a, b) - min(a, b)


def reconcile_lists(l1: list[int], l2: list[int]):
    assert len(l1) == len(l2)
    l1.sort()
    l2.sort()
    return sum(distance(i, j) for i, j in zip(l1, l2))

if __name__ == "__main__":
    l1 = [3, 4, 2, 1, 3, 3]
    l2 = [4, 3, 5, 3, 9, 3]
    print("Total distance:", reconcile_lists(l1, l2))