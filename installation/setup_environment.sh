#!/bin/bash

current_user=$(whoami)
export_line="export PATH=\"/Users/$current_user/Library/Python/3.9/bin:\$PATH\""

if ! grep -Fxq "$export_line" ~/.zshrc; then
    echo "$export_line" >> ~/.zshrc
    echo "La ligne suivante a été ajoutée à ~/.zshrc :"
    echo "$export_line"
    source ~/.zshrc
else
    echo "Le chemin Python est déjà configuré dans ~/.zshrc."
fi
