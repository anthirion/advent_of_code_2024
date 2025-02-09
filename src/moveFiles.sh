#!/bin/bash

# ce script utilitaire déplace les fichiers day*.py dans les dossiers associés
# ainsi day1.py est déplacé dans le dossier day1/, le fichier day2.py est déplacé
# dans le dossier day2/, et ainsi de suite jusqu'à day6.py

for i in $(seq 1 6); do
	filename="day${i}.py"
	srcFolder="day${i}"
	srcPath="$srcFolder/$filename"
	if [ -f $srcPath ]; then
		mv $srcPath .
	fi
done;
