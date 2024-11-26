#!/bin/bash

# create dir on desktop
desktopPath=~/Desktop
ankiFolderPath="$desktopPath/anki_card_generator"

if [ ! -d "$ankiFolderPath" ]; then
    mkdir "$ankiFolderPath"
    echo "Dossier anki_card_generator créé sur le bureau."
else
    echo "Le dossier anki_card_generator existe déjà."
fi

# create apkg_generator file
ankiScriptPath="$ankiFolderPath/apkg_generator.py"
cat > "$ankiScriptPath" << EOL
# Contenu de apkg_generator.py (inchangé)
EOL

echo "Fichier apkg_generator.py créé dans le dossier anki_card_generator."

# create json file
cardsJsonPath="$ankiFolderPath/cards.json"
if [ ! -f "$cardsJsonPath" ]; then
    echo "[]" > "$cardsJsonPath"
    echo "Fichier cards.json créé dans le dossier anki_card_generator."
else
    echo "Le fichier cards.json existe déjà."
fi

chmod +x "$ankiScriptPath"
echo "Permission d'exécution accordée au fichier apkg_generator.py."

# create exec with pyinstaller
cd "$ankiFolderPath"
pyinstaller --onefile apkg_generator.py

# clean build and dir

if [ -f "dist/apkg_generator" ]; then
    mv dist/apkg_generator "$ankiFolderPath/apkg_generator"
    echo "L'exécutable apkg_generator a été créé et déplacé dans le dossier anki_card_generator."
else
    echo "Erreur lors de la création de l'exécutable. Vérifiez PyInstaller."
    exit 1
fi

rm -rf build dist apkg_generator.spec
echo "Nettoyage terminé."
