import os
import json
import genanki
import uuid
import sys
import hmac
import hashlib

# hash key to send in the exec
SECRET_KEY = "4d282400acab6e3e01f231d7dfae20ea6df57696fca505781473a5d7e0f43005"

def get_local_machine_id():
    return str(uuid.getnode())

def validate_executable():
    try:
        # Ouvre l'exécutable en mode binaire
        with open(sys.argv[0], 'rb') as exe_file:
            # Lis les deux premières lignes pour le machine_id et la signature
            machine_id = exe_file.readline().strip().decode()
            embedded_signature = exe_file.readline().strip().decode()

            # Recalculer le HMAC avec le machine_id
            calculated_signature = hmac.new(SECRET_KEY, machine_id.encode(), hashlib.sha256).hexdigest()

            # Vérifier si les signatures correspondent
            if embedded_signature != calculated_signature:
                print("Signature invalide. L'exécutable a été modifié.")
                sys.exit(1)

            # Vérifier si le machine_id correspond à la machine locale
            local_machine_id = get_local_machine_id()
            if machine_id != local_machine_id:
                print("Cet exécutable n'est pas autorisé sur cette machine.")
                sys.exit(1)

    except Exception as e:
        print(f"Erreur lors de la validation : {e}")
        sys.exit(1)

    print("Validation réussie. L'exécutable est authentique et autorisé.")

validate_executable()

# Reste de votre script
print("Exécution de l'exécutable...")


# Définir le chemin absolu du fichier cards.json
if getattr(sys, 'frozen', False):
    # Lorsque le script est "frozen" par PyInstaller
    base_path = os.path.dirname(sys.executable)
else:
    # Lorsque le script est exécuté normalement
    base_path = os.path.dirname(os.path.abspath(__file__))

cards_json_path = os.path.join(base_path, 'cards.json')

# Charger les données JSON depuis un fichier
if not os.path.exists(cards_json_path):
    raise FileNotFoundError(f"Le fichier cards.json est introuvable dans {cards_json_path}. Assurez-vous qu'il se trouve dans le même répertoire que l'exécutable.")

with open(cards_json_path, 'r') as file:
    cards_data = json.load(file)

# Créer un modèle de carte Anki
def create_model():
    return genanki.Model(
        model_id=int(uuid.uuid4().int & 0x7FFFFFFF),  # Réduire la taille de l'ID à une valeur positive de 32 bits
        name='BasicModel',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
     css="""
        .card {
        font-family: Arial, sans-serif;
        font-size: 20px;
        color: black;
        background-color: white;
        text-align: center; /* Changer en "left" pour un meilleur alignement des listes */
        }
        hr {
        margin-top: 20px;
        margin-bottom: 20px;
        }
        ul {
        list-style-type: disc;
        margin-left: 20px;
        }
        """
    )

# Créer un deck Anki
my_deck = genanki.Deck(
    deck_id=int(uuid.uuid4().int & 0x7FFFFFFF),  # Réduire la taille de l'ID à une valeur positive de 32 bits
    name="My Generated Deck"
)

# Créer un modèle pour les cartes
my_model = create_model()

# Ajouter les cartes au deck
for card in cards_data:
    question = card.get('question')
    answer = card.get('answer')
    card_type = card.get('card_type', 'basic')

    # Créer la carte de base
    if card_type == 'basic':
        my_note = genanki.Note(
            model=my_model,
            fields=[question, answer]
        )
        my_deck.add_note(my_note)
    
    # Créer la carte inversée (question <-> réponse)
    elif card_type == 'reverse':
        my_note = genanki.Note(
            model=my_model,
            fields=[question, answer]
        )
        my_deck.add_note(my_note)

        reverse_note = genanki.Note(
            model=my_model,
            fields=[answer, question]
        )
        my_deck.add_note(reverse_note)

# Générer le fichier .apkg au même emplacement que l'exécutable
output_file = os.path.join(base_path, "my_deck.apkg")
genanki.Package(my_deck).write_to_file(output_file)

print(f"Le fichier {output_file} a été généré avec succès.")

