import cv2
import numpy as np
import random
import os

def generate_tunnel_mask_and_apply_background_enhanced(image, background, num_tunnels, length_range):
    """
    Genera túneles realistas con fondo visible y bordes con sombra suave para simular profundidad.
    """
    h, w = image.shape[:2]
    mask = np.ones((h, w), dtype=np.uint8) * 255  # 255 = intacto, 0 = túnel

    for _ in range(num_tunnels):
        x, y = random.randint(0, w - 1), random.randint(int(h * 0.3), int(h * 0.7))  # zona más centrada verticalmente
        # x, y = random.randint(0, w - 1), random.randint(int(h * 0.4), int(h * 0.6))  # zona más centrada verticalmente
        angle = random.uniform(-np.pi / 3, np.pi / 3)  # dirección horizontal o diagonal suave
        length = random.randint(*length_range)
        # thickness = random.randint(4, 8)
        thickness = random.randint(10, 12)

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

    # Sombra realista (anillo de borde suave)
    blurred_outer = cv2.GaussianBlur(255 - mask, (15, 15), 0)
    blurred_inner = cv2.GaussianBlur(255 - mask, (5, 5), 0)
    burn_ring = cv2.subtract(blurred_outer, blurred_inner)
    burn_ring = (burn_ring / 255.0)[:, :, None]

    # Fondo visible solo en túneles
    mask_3ch = cv2.merge([mask] * 3)
    tunnel_image = np.where(mask_3ch == 0, background, image).astype(np.float32)

    # Oscurecer bordes del túnel
    result = tunnel_image * (1 - burn_ring * 1.3)
    result = np.clip(result, 0, 255).astype(np.uint8)

    return result


def apply_final_tunnel_effect(input_path, bg_path, output_path, num_tunnels=20, length_range=(80, 160)):
    """
    Aplica el efecto final a una imagen específica.
    """
    image = cv2.imread(input_path)
    background = cv2.imread(bg_path)

    if image is None or background is None:
        print("❌ Error loading input or background image.")
        return

    background = cv2.resize(background, (image.shape[1], image.shape[0]))
    result = generate_tunnel_mask_and_apply_background_enhanced(image, background, num_tunnels, length_range)

    cv2.imwrite(output_path, result)
    print(f"✅ Imagen generada: {output_path}")


# --- USO DE EJEMPLO ---

input_folder = 'cropped'
output_folder = 'degraded'
bg_path = 'IMG/reference_image.PNG'
# num_tunnels_range = (1, 4)
num_tunnels_range = (20, 40)

os.makedirs(output_folder, exist_ok=True)

random.seed(0)

for filename in os.listdir(input_folder):
    if filename.lower().endswith('.jpg'):
        input_path = os.path.join(input_folder, filename)
        # output_path = os.path.join(output_folder, f"tunnels_final_{filename}")
        output_path = os.path.join(output_folder, filename)
        num_tunnels = random.randint(*num_tunnels_range)
        apply_final_tunnel_effect(input_path, bg_path, output_path, num_tunnels=num_tunnels, length_range=(20, 50))
