from flask import Flask, request, render_template
import os
from datetime import datetime

app = Flask(__name__)

# Emplacement pour enregistrer les fichiers uploadés
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Emplacement pour enregistrer l'index
INDEX_FILE = 'index.csv'

def index_file(filename, indexing_type='automatic', additional_info=None):
    # Chemin complet du fichier
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Indexation automatique par date, heure et taille
    if indexing_type == 'automatic':
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file_size = os.path.getsize(file_path)
        index_entry = f'{filename},{current_time},{file_size}\n'
        
        # Classer le fichier dans un dossier basé sur la date
        date_folder = datetime.now().strftime('%Y-%m-%d')
        size_folder = f'size_{file_size // (1024 * 1024)}MB'  # Classement par taille
        destination_folder = os.path.join(app.config['UPLOAD_FOLDER'], date_folder, size_folder)

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Gérer le cas du fichier déjà existant
        base, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(destination_folder, filename)):
            filename = f'{base}_{counter}{extension}'
            counter += 1

        os.rename(file_path, os.path.join(destination_folder, filename))
        
    # Indexation manuelle avec des champs supplémentaires
    elif indexing_type == 'manual' and additional_info:
        index_entry = f'{filename},{additional_info}\n'
    else:
        return False
    
    with open(INDEX_FILE, 'a') as index_file:
        index_file.write(index_entry)
    return True

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', message='Aucun fichier sélectionné')

        file = request.files['file']

        if file.filename == '':
            return render_template('upload.html', message='Aucun fichier sélectionné')

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        # Indexation automatique
        if index_file(file.filename, 'automatic'):
            return render_template('upload.html', message='Fichier téléchargé et indexé avec succès')

    return render_template('upload.html', message='')

@app.route('/manual_index', methods=['GET','POST'])
def manual_index():
    if request.method == 'POST':
        filename = request.form['filename']
        additional_info = request.form['additional_info']

        # Indexation manuelle
        if index_file(filename, 'manual', additional_info):
            return render_template('manual_index.html', message='Fichier indexé avec succès')

    return render_template('manual_index.html', message='')

@app.route('/evaluation', methods=['GET'])
def evaluation():
    result = {}  # Dictionnaire pour stocker les résultats
    root_folder = app.config['UPLOAD_FOLDER']

    for date_folder in os.listdir(root_folder):
        date_path = os.path.join(root_folder, date_folder)
        
        if os.path.isdir(date_path):  # Vérifier si c'est un dossier
            result[date_folder] = {}  # Dictionnaire pour chaque date

            for size_folder in os.listdir(date_path):
                size_path = os.path.join(date_path, size_folder)

                if os.path.isdir(size_path):  # Vérifier si c'est un dossier
                    result[date_folder][size_folder] = len(os.listdir(size_path))

    return render_template('evaluation.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
