import os
import shutil
from typing import Dict, List
import questionary
from datetime import datetime
from loguru import logger
from pathlib import Path
from PIL import Image

from src.models.album import Album
from src.utils.image_non_graphic_utils import is_image, get_image_exif
from src.utils.album_utils import show_album

logger.info("Application starting up 🚀")

# Retrieving parameters
logger.trace("Some parameters need to be retrieved!")
read_directory = Path(
    questionary.path("From which folder should photos be retrieved?").ask()
)
write_directory = Path(
    questionary.path("Where should the grouped photos be written to?").ask()
)

# Write out parameters
logger.debug("The following parameters are being used:")
logger.debug(f"\tRead Directory: {read_directory}")
logger.debug(f"\tWrite Directory: {write_directory}")

# Checking if directory exists
logger.info("Checking if read directory exists")
if not read_directory.is_dir():
    logger.error("Read directory does not exist or can't be accessed")
    raise BaseException(
        f"Read directory '{read_directory}' does not exist or can't be accessed"
    )

# Getting all images within directory
logger.info("Retrieving all images within read directory")
directory_entries = os.listdir(read_directory)
directory_images = list(
    filter(lambda x: is_image(read_directory, x), directory_entries)
)
logger.info(f"From directory '#{len(directory_images)}' images were found")

# Iterating images and group accordingly
images_grouped: Dict[str, List[str]] = {}
for image_filename in directory_images:
    image_full_path = read_directory.joinpath(image_filename)

    image = Image.open(image_full_path)
    image_exif = get_image_exif(image)

    image_datetime_str = image_exif["DateTime"]
    image_datetime = datetime.strptime(image_datetime_str, "%Y:%m:%d %H:%M:%S")

    image_date = datetime.strftime(image_datetime, "%Y.%m.%d")
    if image_date not in images_grouped:
        images_grouped[image_date] = []

    images_grouped[image_date].append(image_filename)

logger.info(f"Script generated '#{len(images_grouped.keys())}' groups of images")

# For each group associate the correct information
albums: List[Album] = []
for album_date, images in images_grouped.items():
    show_photos = questionary.confirm(
        "Do you wish to see the photos from this group?"
    ).ask()
    if show_photos:
        max_width = int(
            questionary.text(
                "What is the maximum pixel width of a window to show?", "1250"
            ).ask()
        )
        max_height = int(
            questionary.text(
                "What is the maximum pixel height of a window to show?", "750"
            ).ask()
        )

        image_full_paths = list(map(lambda x: read_directory.joinpath(x), images))
        show_album(image_full_paths, album_date, max_width, max_height)

    album_name = questionary.text(
        "What description do you want to associate with the album?"
    ).ask()
    album = Album(album_date, album_name, images)

    logger.debug("A new album has been generated:")
    logger.debug(f"\tDate: {album.date}")
    logger.debug(f"\tName: {album.name}")
    logger.debug(f"\tPhotos: #{len(album.asset_fullpaths)}")

    albums.append(album)

logger.info(f"Script generated '#{len(albums)}' albums")

# For each album save in the appropriate folder the images
for album in albums:
    fully_qualified_album = f"{album.date} - {album.name}"
    logger.debug(f"Preparing to save album '{fully_qualified_album}'")

    album_path = write_directory.joinpath(fully_qualified_album)
    album_path.mkdir(parents=True, exist_ok=True)
    logger.debug("Album folder created")

    for image_fullpath_str in album.asset_fullpaths:
        image_fullpath = Path(image_fullpath_str)
        image_filename = image_fullpath.name

        shutil.copy(image_fullpath, album_path)
        logger.debug(
            f"Asset '{image_filename}' copied into album '{fully_qualified_album}'"
        )

    logger.debug("Album fully generated")

logger.info(f"Script saved '#{len(albums)}' albums")
