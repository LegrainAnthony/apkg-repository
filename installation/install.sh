#!/bin/bash

# sudo verification
if [ "$EUID" -ne 0 ]; then
    echo "Veuillez exécuter ce script avec sudo : sudo $0"
    exit 1
fi

echo "Début de l'installation..."

./setup_brew.sh
./setup_python.sh
./setup_environment.sh
./generate_apkg.sh

echo "Installation terminée avec succès."
