import argparse

def get_arguments_from_command_line() -> tuple[str, int]:
    """
    Récupère les arguments filename et part de la ligne de commande
    """
    parser = argparse.ArgumentParser(
                    prog='List reconciliation',
                    description='Compute the distance between 2 lists')
    parser.add_argument('filename')
    parser.add_argument('-p', '--part', required=True,
                        help="The part of the problem to be solved. \
                        Each problem has exactly 2 parts")
    args = parser.parse_args()
    filename = args.filename
    part = args.part
    # vérifier que le nom du fichier se termine par ".txt"
    if not filename.endswith(".txt"):
        raise ValueError("Filename MUST be a txt file")
    # vérifier que part est bien un entier
    if not part.isdecimal():
        raise ValueError("Argument part MUST be an integer")
    part = int(part)
    # vérifier que le numéro de la partie est 1 ou 2
    if part not in (1, 2):
        raise ValueError("Argument part MUST be 1 or 2")
    return filename, part