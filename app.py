import streamlit as st
import numpy as np
from PIL import Image
import os

# Classe MLP définie comme dans votre code précédent
class MLP:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize weights matrix and biases
        self.W_input_hidden = np.random.randn(self.input_size, self.hidden_size)
        self.b_input_hidden = np.zeros((1, self.hidden_size))
        self.W_hidden_output = np.random.randn(self.hidden_size, self.output_size)
        self.b_hidden_output = np.zeros((1, self.output_size))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, input_data):
        hidden_layer_input = np.dot(input_data, self.W_input_hidden) + self.b_input_hidden
        hidden_layer_output = self.sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, self.W_hidden_output) + self.b_hidden_output
        output = self.sigmoid(output_layer_input)
        return hidden_layer_output, output

    def predict(self, input_data):
        _, output = self.forward(input_data)
        return output

    def load_weights(self, file_path):
        data = np.load(file_path)
        self.W_input_hidden = data['W_input_hidden']
        self.b_input_hidden = data['b_input_hidden']
        self.W_hidden_output = data['W_hidden_output']
        self.b_hidden_output = data['b_hidden_output']
        print(f"Weights loaded from {file_path}")

# Fonction pour charger et prétraiter une image
def load_and_preprocess_image(image, image_size=(64, 64)):
    img = image.convert('L')  # Convertir en niveaux de gris
    img = img.resize(image_size)  # Redimensionner l'image
    img = np.array(img).flatten()  # Aplatir l'image
    img = img / 255.0  # Normaliser les pixels
    return img

# Application Streamlit
st.title("Classification des images à l'aide de PMC")

# Chargement des poids du modèle
model = MLP(input_size=64*64, hidden_size=100, output_size=3)
model.load_weights('mlp_weights.npz')

# Téléchargement de l'image
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    # Utilisation des colonnes pour afficher l'image à gauche et la prédiction à droite
    col1, col2 = st.columns([1, 1])  # Vous pouvez ajuster les ratios si nécessaire
    
    # Affichage de l'image téléchargée dans la première colonne
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', width=250)  # Réduction de la taille de l'image
    
    # Prétraitement de l'image
    processed_image = load_and_preprocess_image(image)
    
    # Prédiction
    prediction = model.predict(np.array([processed_image]))
    predicted_class = np.argmax(prediction, axis=1)[0]
    
    # Mapping des classes
    class_names = ['Piano', 'Clavier', 'Machine à Écrire']
    
    # Affichage de la prédiction dans la deuxième colonne
    with col2:
        st.markdown(f"<h2 style='text-align: center; color: green;'>Prédiction: {class_names[predicted_class]}</h2>", unsafe_allow_html=True)
