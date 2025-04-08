import cv2
import os

def resize_to_fit_screen(image, screen_width=1280, screen_height=720):
    h, w = image.shape[:2]
    scale = min(screen_width / w, screen_height / h, 1.0)
    new_size = (int(w * scale), int(h * scale))
    resized = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    return resized, scale

def extract_manuscript_by_manual_contour_selection(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    valid_extensions = ['.jpg', '.jpeg', '.png']

    for filename in os.listdir(input_folder):
        if not any(filename.lower().endswith(ext) for ext in valid_extensions):
            continue

        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        height, width = image.shape[:2]

        # Preprocessing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                       cv2.THRESH_BINARY_INV, 15, 10)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # Try external first
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 1:
            contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filter
        contour_box_pairs = [(cnt, cv2.boundingRect(cnt)) for cnt in contours]
        min_w, min_h = width * 0.3, height * 0.3
        max_w, max_h = width * 0.95, height * 0.95

        filtered_contours = [
            (cnt, (x, y, w, h)) for cnt, (x, y, w, h) in contour_box_pairs
            if min_w < w < max_w and min_h < h < max_h
        ]

        filtered_contours = sorted(filtered_contours, key=lambda item: item[1][2] * item[1][3], reverse=True)
        candidates = [c for c, _ in filtered_contours]

        if not candidates:
            print(f"⚠️ No valid contours found in {filename}")
            continue

        print(f"📄 {filename} — {len(candidates)} candidate(s) found")

        index = 0
        selected = False

        while index < len(candidates):
            contour = candidates[index]
            x, y, w, h = cv2.boundingRect(contour)

            preview_img = image.copy()
            for c in candidates:
                cv2.drawContours(preview_img, [c], -1, (255, 0, 0), 2)
            cv2.rectangle(preview_img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            window_title = f"{filename} — Contour {index+1}/{len(candidates)} — 'y'/Enter=save, 'n'=next, 'm'=manual, other=skip"
            resized_preview, _ = resize_to_fit_screen(preview_img)
            cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
            cv2.imshow(window_title, resized_preview)
            key = cv2.waitKey(0)
            cv2.destroyWindow(window_title)

            if key in [ord('y'), 13]:  # y or Enter
                cropped = image[y:y+h, x:x+w]
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, cropped)
                print(f"✅ Saved: {output_path}")
                selected = True
                break

            elif key == ord('m'):
                print("✋ Manual selection activated (2 clicks para definir el rectángulo). Presiona 'm' para reiniciar.")
                clone = image.copy()
                cv2.namedWindow("Manual Selection", cv2.WINDOW_NORMAL)
                manual_points = []
                confirmed = False

                scale = 1.0  # será calculado en cada render

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
                        cv2.rectangle(temp, pt1, pt2, (0, 255, 255), 2)

                    resized_temp, scale = resize_to_fit_screen(temp)
                    cv2.imshow("Manual Selection", resized_temp)
                    k = cv2.waitKey(1) & 0xFF

                    if k in [13, ord('y')] and len(manual_points) == 2:
                        pt1, pt2 = manual_points
                        x1, y1 = min(pt1[0], pt2[0]), min(pt1[1], pt2[1])
                        x2, y2 = max(pt1[0], pt2[0]), max(pt1[1], pt2[1])
                        confirmed = True
                        cropped = image[y1:y2, x1:x2]
                        output_path = os.path.join(output_folder, filename)
                        cv2.imwrite(output_path, cropped)
                        print(f"✅ Manually saved: {output_path}")
                        break

                    elif k == ord('m'):
                        manual_points = []
                        print("🔁 Manual selection reset.")

                    elif k == 27:
                        print("❌ Manual selection canceled.")
                        break

                cv2.destroyWindow("Manual Selection")
                if confirmed:
                    selected = True
                break

            elif key == ord('n'):
                index += 1
            else:
                print(f"⏭️ Skipped: {filename}")
                break

        if not selected and index >= len(candidates):
            print(f"🚫 No contour selected for {filename}")

# === Uso ===
input_folder = "originals"
output_folder = "cropped"
extract_manuscript_by_manual_contour_selection(input_folder, output_folder)
