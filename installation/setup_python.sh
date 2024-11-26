#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Python n'est pas installé. Installation en cours..."
    brew install python
else
    echo "Python est déjà installé."
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip n'est pas installé. Installation de pip..."
    python3 -m ensurepip --upgrade
else
    echo "pip est déjà installé."
fi

echo "Installation des bibliothèques genanki
pip3 install --upgrade genanki pyinstaller
