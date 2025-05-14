"""
crop_manuscript_region.py

Este script permite recortar automáticamente la región útil de manuscritos históricos
a partir de la detección de contornos externos. Cuando no se detectan regiones adecuadas,
se ofrece una opción manual para que el usuario defina el área de interés mediante dos clics.

Autor: Lis Paredes
Ubicación: O1_degradacion-artificial/1_preprocesamiento/

Funciones:
- resize_to_fit_screen: ajusta imágenes para visualización en pantalla sin distorsión
- extract_manuscript_by_manual_contour_selection: recorta automáticamente o manualmente
  las regiones relevantes del manuscrito a partir de contornos o selección del usuario

Uso:
Modificar las rutas en la sección final del archivo para definir las carpetas de entrada y salida.
"""

import cv2
import os
import numpy as np

def resize_to_fit_screen(image, screen_width=1280, screen_height=720):
    """
    Redimensiona una imagen para ajustarla a la pantalla sin perder proporciones.

    Parámetros:
    - image: imagen original
    - screen_width: ancho máximo de pantalla
    - screen_height: alto máximo de pantalla

    Retorna:
    - imagen redimensionada
    - escala usada para el redimensionamiento
    """
    h, w = image.shape[:2]
    scale = min(screen_width / w, screen_height / h, 1.0)
    new_size = (int(w * scale), int(h * scale))
    resized = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    return resized, scale

def extract_manuscript_by_manual_contour_selection(input_folder, output_folder):
    """
    Extrae la región principal del manuscrito utilizando contornos automáticos.
    Si no se detectan regiones adecuadas, permite al usuario definir manualmente el recorte.

    Parámetros:
    - input_folder: carpeta de entrada con imágenes
    - output_folder: carpeta donde se guardarán los recortes
    """
    os.makedirs(output_folder, exist_ok=True)
    valid_extensions = ['.jpg', '.jpeg', '.png']

    for filename in os.listdir(input_folder):
        if not any(filename.lower().endswith(ext) for ext in valid_extensions):
            continue

        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        height, width = image.shape[:2]

        # Conversión a escala de grises y binarización
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if np.mean(binary) > 127:
            binary = cv2.bitwise_not(binary)

        # Cierre morfológico para consolidar regiones
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        # Detección de contornos
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 1:
            contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contour_box_pairs = [(cnt, cv2.boundingRect(cnt)) for cnt in contours]
        min_w, min_h = width * 0.3, height * 0.3
        max_w, max_h = width * 0.95, height * 0.95

        # Filtro de contornos por tamaño razonable
        filtered_contours = [
            (cnt, (x, y, w, h)) for cnt, (x, y, w, h) in contour_box_pairs
            if min_w < w < max_w and min_h < h < max_h
        ]

        # Orden por área descendente
        filtered_contours = sorted(filtered_contours, key=lambda item: item[1][2] * item[1][3], reverse=True)
        candidates = [c for c, _ in filtered_contours]

        index = 0
        selected = False

        while index < max(1, len(candidates)):
            if candidates:
                contour = candidates[index]
                x, y, w, h = cv2.boundingRect(contour)
            else:
                x, y, w, h = 0, 0, width, height

            preview_img = image.copy()
            if candidates:
                for c in candidates:
                    cv2.drawContours(preview_img, [c], -1, (255, 0, 0), 2)
                cv2.rectangle(preview_img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            window_title = f"{filename} — Contour {index+1}/{len(candidates)}"
            resized_preview, _ = resize_to_fit_screen(preview_img)
            cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
            cv2.imshow(window_title, resized_preview)
            key = cv2.waitKey(0)
            cv2.destroyWindow(window_title)

            if key in [ord('y'), 13]:
                cropped = image[y:y+h, x:x+w]
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, cropped)
                print(f"Guardado: {output_path}")
                selected = True
                break

            elif key == ord('m'):
                print("Modo manual activado. Realiza dos clics para definir el rectángulo.")
                clone = image.copy()
                cv2.namedWindow("Manual Selection", cv2.WINDOW_NORMAL)
                manual_points = []
                confirmed = False
                scale = 1.0

                def click_callback(event, x, y, flags, param):
                    nonlocal manual_points
                    if event == cv2.EVENT_LBUTTONDOWN:
                        real_x = int(x / scale)
                        real_y = int(y / scale)
                        if len(manual_points) < 2:
                            manual_points.append((real_x, real_y))

                cv2.setMouseCallback("Manual Selection", click_callback)

                while True:
                    temp = clone.copy()
                    if len(manual_points) == 1:
                        cv2.circle(temp, manual_points[0], 5, (0, 255, 255), -1)
                    elif len(manual_points) == 2:
                        pt1, pt2 = manual_points
                        x1 = min(pt1[0], pt2[0])
                        y1 = min(pt1[1], pt2[1])
                        x2 = max(pt1[0], pt2[0])
                        y2 = max(pt1[1], pt2[1])
                        cv2.rectangle(temp, (x1, y1), (x2, y2), (0, 255, 255), 2)

                    resized_temp, scale = resize_to_fit_screen(temp)
                    cv2.imshow("Manual Selection", resized_temp)
                    k = cv2.waitKey(1) & 0xFF

                    if k in [13, ord('y')] and len(manual_points) == 2:
                        pt1, pt2 = manual_points
                        x1 = min(pt1[0], pt2[0])
                        y1 = min(pt1[1], pt2[1])
                        x2 = max(pt1[0], pt2[0])
                        y2 = max(pt1[1], pt2[1])
                        cropped = image[y1:y2, x1:x2]
                        output_path = os.path.join(output_folder, filename)
                        cv2.imwrite(output_path, cropped)
                        print(f"Guardado manual: {output_path}")
                        confirmed = True
                        break

                    elif k == ord('m'):
                        manual_points = []

                    elif k == 27:
                        break

                cv2.destroyWindow("Manual Selection")
                if confirmed:
                    selected = True
                break

            elif key == ord('n') and candidates:
                index += 1
            else:
                break

        if not selected and index >= len(candidates):
            print(f"No se recortó ninguna región para {filename}")

# === USO ===
input_folder = "output_deskewed"
output_folder = "output_cropping"
extract_manuscript_by_manual_contour_selection(input_folder, output_folder)
