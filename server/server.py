# from flask import Flask, request, send_file
# import hmac
# import hashlib
# import os
# import tempfile

# app = Flask(__name__)

# SECRET_KEY = os.getenv("HMAC_KEY")
# if not SECRET_KEY:
#     raise ValueError("The HMAC_KEY environment variable must be set")

# SECRET_KEY = SECRET_KEY.encode()
# EXECUTABLE_PATH = 'dist/apkg_generator'

# @app.route('/generate', methods=['POST'])
# def generate_executable():
#     # Récupère le machine_id depuis la requête
#     machine_id = request.json.get('machine_id')
#     if not machine_id:
#         return {"error": "machine_id is required"}, 400

#     # Génère une signature HMAC basée sur le machine_id
#     signature = hmac.new(SECRET_KEY, machine_id.encode(), hashlib.sha256).hexdigest()

#     # Lis l'exécutable original
#     try:
#         with open(EXECUTABLE_PATH, 'rb') as exe_file:
#             exe_content = exe_file.read()
#     except FileNotFoundError:
#         return {"error": "Original executable not found"}, 500

#     # Ajoute le machine_id et la signature au début du fichier
#     metadata = f"{machine_id}\n{signature}\n".encode()
#     customized_exe = metadata + exe_content

#     # Enregistre un fichier temporaire personnalisé
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.exe') as temp:
#         temp.write(customized_exe)
#         temp_file_name = temp.name

#     # Renvoie le fichier personnalisé
#     response = send_file(temp_file_name, as_attachment=True)

#     # Supprime le fichier temporaire après envoi
#     @response.call_on_close
#     def cleanup():
#         if os.path.exists(temp_file_name):
#             os.remove(temp_file_name)

#     return response


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


from flask import Flask, send_file
import os
import zipfile
import tempfile

app = Flask(__name__)

# Le chemin de votre exécutable ou .app généré par PyInstaller
EXECUTABLE_PATH = 'dist/apkg_generator.app'  # Assurez-vous que c'est correct

@app.route('/download', methods=['GET'])
def download_executable():
    # Vérifie si le fichier existe
    if not os.path.exists(EXECUTABLE_PATH):
        return {"error": "Executable not found"}, 404

    # Crée un fichier temporaire zip
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isdir(EXECUTABLE_PATH):
                # Si c'est un répertoire (.app), ajoutez tout son contenu
                for root, dirs, files in os.walk(EXECUTABLE_PATH):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=os.path.dirname(EXECUTABLE_PATH))
                        zipf.write(file_path, arcname)
            else:
                # Sinon, ajoutez simplement le fichier (cas d'un exécutable seul)
                zipf.write(EXECUTABLE_PATH, os.path.basename(EXECUTABLE_PATH))

        temp_zip_name = temp_zip.name

    # Envoie le fichier zip créé
    return send_file(temp_zip_name, as_attachment=True, mimetype='application/zip', download_name='apkg_generator.zip')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
