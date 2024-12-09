from command_line_parser import get_arguments_from_command_line
import re
from typing import Iterator
from functools import reduce

################################## PART 1 ##################################


def extract_correct_instructions(code: str) -> list[str]:
    """Cette fonction extrait les instructions mul correctes du type "mul(X,Y)"
    :param code : code brut corrompu
    :return liste des instructions correctes de la forme ["mul(X,Y)", "mul(X1,Y1)"]
    """
    regexp = r"mul\([1-9]\d{0,2},[1-9]\d{0,2}\)"
    return re.findall(regexp, code)


def execute_instructions(correct_instructions: list[str]) -> Iterator[int]:
    """Extrait les nombres de chaque instruction et les multiplie entre eux
    Par exemple, pour mul(X,Y) la fonction va retourner X*Y
    :param correct_instructions: liste des instructions de la forme "mul(X,Y)"
    :return générateur du résultat de chaque instruction
    Pour des questions de perf, on retourne un générateur plutôt qu'une liste car
    ce générateur sera ensuite utilisé pour faire la somme des nombres
    """
    # rq: je ne capture aucune exception car je veux que le programme s'arrête si
    # les données ne sont pas de la forme attendue
    for instruction in correct_instructions:
        x, y = re.findall(r"\d{1,3}", instruction)
        x, y = int(x), int(y)
        yield x*y


def compute_result(instructions_results: Iterator[int]) -> int:
    """Calcule le résultat final en additionnant les résultats des instructions
    :param instructions_results: générateur des multiplications des nombres des
    instructions correctes
    """
    return sum(instructions_results)

################################## PART 2 ##################################


def extract_enabled_code(code: str) -> str:
    """Extrait les portions de code qui sont précédées de do() et pas de don't()
    :param code: code brut
    :return chaine de caractères concaténant les instructions à prendre en compte
    """
    enabled_code: list[str] = []
    portions_of_code: list[str] = code.split("don't()")
    # la portion de code qui précède le premier don't est forcément enabled
    enabled_code.append(portions_of_code[0])
    for i in range(1, len(portions_of_code)):
        conditional_statements: list[str] = portions_of_code[i].split("do()")
        if len(conditional_statements) > 1:
            enabled_code.extend(conditional_statements[1:])
    return reduce(lambda str1, str2: str1 + str2, enabled_code)

############################## LAUNCH PROGRAM ##############################


def get_code_from_file(filename: str) -> str:
    """
    Récupère les rapports dans le fichier donné en paramètre
    """
    with open(filename, 'r', encoding='utf8') as file:
        content = file.read()
    return content


if __name__ == "__main__":
    filename, part = get_arguments_from_command_line()
    code = get_code_from_file(filename)
    if part == 1:
        correct_instructions = extract_correct_instructions(code)
    elif part == 2:
        enabled_code = extract_enabled_code(code)
        correct_instructions = extract_correct_instructions(enabled_code)
    instructions_results = execute_instructions(correct_instructions)
    print("Final result:", compute_result(instructions_results))
