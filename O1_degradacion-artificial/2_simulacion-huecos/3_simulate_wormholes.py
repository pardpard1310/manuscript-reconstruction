"""
simulate_wormholes.py

Este script simula daño físico en manuscritos históricos a través de la inserción de "túneles de polilla"
sobre una imagen de entrada. El efecto incluye una máscara con bordes difuminados que da la impresión de
profundidad, y genera dos salidas: una imagen en color con fondo dañado, y una versión en blanco y negro
optimizada para OCR o análisis binarizado.

Autor: Lis Paredes
Ubicación: O1_degradacion-artificial/2_simulacion-huecos/

Funciones:
- generate_tunnel_mask_and_apply_background_enhanced: aplica daño visual realista con bordes difusos
- convert_to_enhanced_bw: convierte una imagen dañada a binarizado con texto visible
- apply_final_tunnel_and_bw: proceso completo para una imagen: túneles + binarización

Uso:
Modificar las rutas de entrada, fondo de referencia y carpetas de salida al final del script.
"""

import cv2
import numpy as np
import random
import os

def generate_tunnel_mask_and_apply_background_enhanced(image, background, num_tunnels, length_range):
    """
    Genera una máscara con túneles simulados y la aplica a la imagen usando un fondo visible.
    Se agregan sombras suaves para realismo.

    Parámetros:
    - image: imagen original (color)
    - background: imagen de fondo para simular la base bajo el daño
    - num_tunnels: cantidad de túneles a generar
    - length_range: rango de longitud de cada túnel

    Retorna:
    - imagen dañada con túneles y sombras
    """
    h, w = image.shape[:2]
    mask = np.ones((h, w), dtype=np.uint8) * 255

    for _ in range(num_tunnels):
        x, y = random.randint(0, w - 1), random.randint(int(h * 0.1), int(h * 0.9))
        angle = random.uniform(-np.pi / 3, np.pi / 3)
        length = random.randint(*length_range)
        thickness = random.randint(60, 80)

        points = []
        for _ in range(length):
            dx = int(np.cos(angle) * random.randint(4, 6))
            dy = int(np.sin(angle) * random.randint(2, 4))
            x = np.clip(x + dx + random.randint(-1, 1), 0, w - 1)
            y = np.clip(y + dy + random.randint(-1, 1), 0, h - 1)
            points.append((x, y))
            angle += random.uniform(-0.15, 0.15)

        for pt in points:
            cv2.circle(mask, pt, thickness, 0, -1)

    # Generar efecto de sombra
    blurred_outer = cv2.GaussianBlur(255 - mask, (41, 41), 0)
    blurred_inner = cv2.GaussianBlur(255 - mask, (9, 9), 0)
    burn_ring = cv2.subtract(blurred_outer, blurred_inner)
    burn_ring = (burn_ring / 255.0)[:, :, None]

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if len(background.shape) == 2:
        background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)

    mask_3ch = cv2.merge([mask] * 3)
    tunnel_image = np.where(mask_3ch == 0, background, image).astype(np.float32)
    result = tunnel_image * (1 - burn_ring * 1.5)
    result = np.clip(result, 0, 255).astype(np.uint8)

    return result

def convert_to_enhanced_bw(image_color):
    """
    Convierte una imagen en color a blanco y negro con fondo claro y texto oscuro.

    Parámetros:
    - image_color: imagen original en color

    Retorna:
    - imagen binarizada con texto oscuro sobre fondo claro
    """
    gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invertir si es necesario para asegurar fondo blanco
    if np.mean(binary) < 127:
        binary = cv2.bitwise_not(binary)

    return binary

def apply_final_tunnel_and_bw(input_path, bg_path, output_path_color, output_path_bw, num_tunnels=20, length_range=(80, 160)):
    """
    Aplica el proceso completo a una imagen: túneles + binarización.

    Parámetros:
    - input_path: ruta de la imagen original
    - bg_path: ruta de la imagen de fondo
    - output_path_color: salida de imagen en color con túneles
    - output_path_bw: salida en blanco y negro
    - num_tunnels: cantidad de túneles
    - length_range: rango de longitud por túnel
    """
    image = cv2.imread(input_path)
    background = cv2.imread(bg_path)

    if image is None or background is None:
        print("Error cargando input o background.")
        return

    background = cv2.resize(background, (image.shape[1], image.shape[0]))
    result_color = generate_tunnel_mask_and_apply_background_enhanced(image, background, num_tunnels, length_range)
    result_bw = convert_to_enhanced_bw(result_color)

    cv2.imwrite(output_path_color, result_color)
    cv2.imwrite(output_path_bw, result_bw)

    print(f"Guardado: {output_path_color} | {output_path_bw}")

# === USO ===

input_folder = 'output_cropping'
output_folder_color = 'output_with_holes'
output_folder_bw = 'output_bw_with_holes'
bg_path = 'IMG/reference_image2.png'

os.makedirs(output_folder_color, exist_ok=True)
os.makedirs(output_folder_bw, exist_ok=True)

random.seed(0)
num_tunnels_range = (20, 40)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)
        output_path_color = os.path.join(output_folder_color, filename)
        output_path_bw = os.path.join(output_folder_bw, filename)
        num_tunnels = random.randint(*num_tunnels_range)
        apply_final_tunnel_and_bw(
            input_path,
            bg_path,
            output_path_color,
            output_path_bw,
            num_tunnels=num_tunnels,
            length_range=(20, 50)
        )
