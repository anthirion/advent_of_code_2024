# Jour 1

- compter le nombre d'occurences -> count(element)

# Jour 3

- lire le contenu d'un fichier avec la fonction read :

```python
with open(filename, 'r', encoding='utf8') as file:
        content = file.read()
```

- fonction reduce

# Jour 4

- ATTENTION en python, liste[-1] ne retourne pas d'erreur
  Par conséquent, bien vérifier que les indices sont positifs

# Jour 5

- retourner l'index où se trouve l'élément d'une liste -> list.index()
- l'opérateur '==' compare 2 arrays élément par élément -> cela signifie que l'opérateur retourne un array de booléens auquel il faut appliquer un np.all ou np.any
- pour comparer directement 2 arrays, utiliser la fonction np.array_equal

# Optimisation jour 6 avec Cython
ATTENTION à la lecture et écriture des caractères de la grille :
  le C stocke les caractères sous forme d'entiers (table ASCII) donc il faut
  bien penser à convertir les caractères Python en entier (à l'aide de la fonction ord) et à convertir le  contenu de la grille en caractère (à l'aide de la fonction chr)