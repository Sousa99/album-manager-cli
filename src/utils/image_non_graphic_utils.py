import mimetypes
from datetime import datetime
from typing import Any, Dict, List
from PIL import Image, ExifTags
from pathlib import Path
from pillow_heif import register_heif_opener

# Add some unsuported mimetypes into the recognized formats
mimetypes.add_type('image/heic', '.heic')
mimetypes.add_type('image/heif', '.heif')
# Register heif opener for pillow
register_heif_opener()

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

def group_images(images: List[Path]) -> Dict[str, List[Path]]:
    images_grouped: Dict[str, List[str]] = {}
    for image_filepath in images:
        image = Image.open(image_filepath)
        image_exif = get_image_exif(image)

        image_key = "UNKNOWN"
        if "DateTime" in image_exif:
            image_datetime_str = image_exif["DateTime"]
            image_datetime = datetime.strptime(image_datetime_str, "%Y:%m:%d %H:%M:%S")

            image_key = datetime.strftime(image_datetime, "%Y.%m.%d")

        if image_key not in images_grouped:
            images_grouped[image_key] = []
        images_grouped[image_key].append(image_filepath)

    return images_grouped
