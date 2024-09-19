import base64
import csv
import os
import requests

# Nom du fichier CSV
csv_file = 'C:/Users/nabil/Desktop/MLP/machine_a_ecrire_729.csv'  # Remplacez par le chemin de votre fichier CSV
output_folder = 'C:/Users/nabil/Desktop/MLP/dataset/machine_a_ecrire'  # Répertoire où les images seront enregistrées

# Créez le répertoire de sortie s'il n'existe pas déjà
os.makedirs(output_folder, exist_ok=True)

# Ouvrir le fichier CSV
with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Sauter l'en-tête

    for i, row in enumerate(reader):
        if row:
            data = row[0]
            if data.startswith("data:image"):  # Pour les images encodées en base64
                try:
                    img_data = data.split(',')[1]  # Séparer le préfixe de l'encodage base64
                    img_bytes = base64.b64decode(img_data)

                    # Définir le nom du fichier de sortie
                    img_filename = os.path.join(output_folder, f'image_base64_{i+1}.jpg')
                    
                    # Écrire l'image dans un fichier
                    with open(img_filename, 'wb') as img_file:
                        img_file.write(img_bytes)

                    print(f'Image base64 {i+1} sauvegardée sous {img_filename}')
                except Exception as e:
                    print(f'Erreur lors du traitement de la ligne {i+1}: {e}')
            elif data.startswith("http"):  # Pour les liens URL d'images
                try:
                    img_response = requests.get(data)
                    img_response.raise_for_status()

                    # Définir le nom du fichier de sortie
                    img_filename = os.path.join(output_folder, f'image_url_{i+1}.jpg')

                    # Enregistrer l'image à partir de l'URL
                    with open(img_filename, 'wb') as img_file:
                        img_file.write(img_response.content)

                    print(f'Image URL {i+1} téléchargée et sauvegardée sous {img_filename}')
                except requests.exceptions.RequestException as e:
                    print(f'Erreur lors du téléchargement de l\'image URL à la ligne {i+1}: {e}')
            else:
                print(f'Ligne {i+1} ignorée : pas de données d\'image ou URL valide.')
