import cv2
from pathlib import Path


def show_image(
    image_full_path: Path, window_name: str, max_width: int, max_height: int
):
    image = cv2.imread(str(image_full_path))
    image_height = image.shape[0]
    image_width = image.shape[1]

    width_factor = max_width / image_width
    height_factor = max_height / image_height
    factor = min(width_factor, height_factor)

    target_width = int(image_width * factor)
    target_height = int(image_height * factor)
    resized_image = cv2.resize(image, (target_width, target_height))

    cv2.imshow(window_name, resized_image)
