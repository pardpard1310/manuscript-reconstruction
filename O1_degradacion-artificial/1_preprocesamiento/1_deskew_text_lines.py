"""
deskew_text_lines.py

Este script permite corregir la inclinación del texto en imágenes de manuscritos históricos.
El método se basa en el análisis de la proyección horizontal tras rotaciones leves, para estimar
el ángulo que maximiza la alineación de líneas textuales.

Autor: Lis Paredes
Ubicación: O1_degradacion-artificial/1_preprocesamiento/

Funciones:
- compute_skew_angle_via_projection: estima el ángulo óptimo de rotación
- deskew_image_precisely: aplica el enderezado si se supera un umbral mínimo
- batch_precise_deskew: corrige todas las imágenes en una carpeta de entrada

Uso:
Modificar las rutas en la llamada a 'batch_precise_deskew' al final del archivo.
"""

import cv2
import numpy as np
import os
from glob import glob

def compute_skew_angle_via_projection(gray: np.ndarray) -> float:
    """
    Estima el ángulo de inclinación del texto en una imagen binarizada (escala de grises invertida).
    Se prueba una serie de ángulos de rotación y se selecciona aquel que maximiza la varianza
    de la proyección horizontal.

    Parámetros:
    - gray: imagen en escala de grises invertida (texto en blanco sobre fondo negro)

    Retorna:
    - best_angle: ángulo que ofrece la mejor alineación horizontal
    """
    best_angle = 0
    max_variance = 0
    angles = np.arange(-5, 5.1, 0.5)  # Se prueban ángulos de -5° a +5° en pasos de 0.5°

    for angle in angles:
        h, w = gray.shape
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1)
        rotated = cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

        projection = np.mean(rotated, axis=1)
        variance = np.var(projection)

        if variance > max_variance:
            max_variance = variance
            best_angle = angle

    return best_angle

def deskew_image_precisely(input_path: str, output_path: str, threshold: float = 0.5):
    """
    Aplica corrección de inclinación a una imagen si el ángulo detectado supera el umbral.

    Parámetros:
    - input_path: ruta de la imagen original
    - output_path: ruta donde se guardará la imagen corregida
    - threshold: umbral mínimo (en grados) para aplicar la corrección
    """
    image = cv2.imread(input_path)
    if image is None:
        print(f"No se pudo cargar la imagen: {input_path}")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bw = cv2.bitwise_not(bw)

    angle = compute_skew_angle_via_projection(bw)

    if abs(angle) < threshold:
        print(f"Imagen ya alineada ({angle:.2f}°): {os.path.basename(input_path)}")
        result = image
    else:
        print(f"Corrigiendo inclinación: {os.path.basename(input_path)} ({angle:.2f}°)")
        h, w = image.shape[:2]
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1)
        result = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    cv2.imwrite(output_path, result)
    print(f"Guardado: {output_path}")

def batch_precise_deskew(input_folder: str, output_folder: str):
    """
    Aplica el enderezado a todas las imágenes de una carpeta de entrada.

    Parámetros:
    - input_folder: ruta a la carpeta que contiene las imágenes originales
    - output_folder: ruta a la carpeta donde se guardarán las imágenes corregidas
    """
    os.makedirs(output_folder, exist_ok=True)
    image_paths = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.tif', '*.tiff']:
        image_paths.extend(glob(os.path.join(input_folder, ext)))
    image_paths.sort()

    if not image_paths:
        print(f"No se encontraron imágenes en: {input_folder}")
        return

    print(f"Procesando {len(image_paths)} imágenes en: {input_folder}")

    for img_path in image_paths:
        filename = os.path.splitext(os.path.basename(img_path))[0]
        out_path = os.path.join(output_folder, f"{filename}_deskewed.png")
        deskew_image_precisely(img_path, out_path)

# Ruta de ejemplo (modificar antes de ejecutar)
# batch_precise_deskew("ruta/a/imagenes_entrada", "ruta/a/imagenes_enderezadas")
