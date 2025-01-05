import numpy as np
import cv2
from matplotlib import pyplot as plt

def aplicar_filtro(transformada, tipo_filtro, radio=25, ancho_banda=40):
    filas, columnas = transformada.shape
    centro_filas, centro_columnas = filas // 2, columnas // 2
    mascara = np.ones((filas, columnas), dtype=np.uint8)

    if tipo_filtro == 'pasa-bajas':
        for i in range(filas):
            for j in range(columnas):
                distancia = np.sqrt((i - centro_filas)**2 + (j - centro_columnas)**2)
                if distancia > radio:
                    mascara[i, j] = 0
    elif tipo_filtro == 'pasa-altas':
        for i in range(filas):
            for j in range(columnas):
                distancia = np.sqrt((i - centro_filas)**2 + (j - centro_columnas)**2)
                if distancia < radio:
                    mascara[i, j] = 0
    elif tipo_filtro == 'elimina-banda':
        for i in range(filas):
            for j in range(columnas):
                distancia = np.sqrt((i - centro_filas)**2 + (j - centro_columnas)**2)
                if radio - ancho_banda < distancia < radio + ancho_banda:
                    mascara[i, j] = 0

    return transformada * mascara


def procesar_imagen(ruta_imagen, tipo_filtro, radio, ancho_banda=40):
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    transformada = np.fft.fft2(img)
    transformada_centrada = np.fft.fftshift(transformada)
    transformada_filtrada = aplicar_filtro(transformada_centrada, tipo_filtro, radio, ancho_banda)
    transformada_inversa = np.fft.ifftshift(transformada_filtrada)
    imagen_reconstruida = np.fft.ifft2(transformada_inversa).real

    # Normalizar la imagen reconstruida
    imagen_normalizada = (imagen_reconstruida - np.min(imagen_reconstruida)) / (np.max(imagen_reconstruida) - np.min(imagen_reconstruida)) * 255
    return imagen_normalizada

