from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from filtro_fourier import procesar_imagen
from PIL import Image
import numpy as np

app = Flask(__name__)

# Carpetas para las imágenes subidas y procesadas

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Verificar si se seleccionó un archivo
    if 'image' not in request.files:
        return "No se seleccionó ninguna imagen", 400

    file = request.files['image']
    if file.filename == '':
        return "El archivo no tiene nombre", 400

    # Guardar la imagen subida
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Leer parámetros del formulario
    filtro = request.form.get('filter')
    radio = int(request.form.get('radius', 25))
    ancho_banda = int(request.form.get('bandwidth', 40))

    # Procesar la imagen
    resultado = procesar_imagen(file_path, filtro, radio, ancho_banda)

    # Guardar la imagen procesada
    result_path = os.path.join(RESULT_FOLDER, f"resultado_{filtro}_{file.filename}")
    Image.fromarray(resultado.astype(np.uint8)).save(result_path)

    # Enviar la imagen procesada al usuario como archivo descargable
    return send_file(result_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
