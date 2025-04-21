import cv2
import mimetypes
from typing import Any, Dict
from PIL import Image, ExifTags
from pathlib import Path


def is_image(directory: Path, file: str) -> bool:
    full_path = directory.joinpath(file)

    # If not a file immediatelly return
    if not full_path.is_file():
        return False

    mimetypes_guess = mimetypes.guess_type(full_path)
    first_guess = mimetypes_guess[0]
    if not first_guess:
        return False

    return first_guess.startswith("image")


def get_image_exif(image: Image.Image) -> Dict[str, Any]:
    image_full_exif = image.getexif()
    image_treated_exif = {}

    for key, value in image_full_exif.items():
        # if key is not recognized
        if key not in ExifTags.TAGS:
            continue

        treated_key = ExifTags.TAGS[key]
        image_treated_exif[treated_key] = value

    return image_treated_exif


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
