import os

# Répertoire contenant les images
folder_path = 'C:/Users/nabil/Desktop/MLP/dataset/machine_a_ecrire'  # Remplacez par le chemin de votre dossier

# Liste tous les fichiers dans le dossier
files = sorted(os.listdir(folder_path))

# Renomme les fichiers
for i, filename in enumerate(files, start=1):
    if filename.startswith("img"):
        old_file_path = os.path.join(folder_path, filename)
        new_file_name = f'img{i}.jpg'
        new_file_path = os.path.join(folder_path, new_file_name)
        
        os.rename(old_file_path, new_file_path)
        print(f'{old_file_path} renommé en {new_file_path}')
