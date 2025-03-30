import os
import shutil
from datetime import datetime
from typing import Dict, List
from loguru import logger
from PIL import Image
import argparse

from src.models.album import Album
from src.utils.image_utils import is_image, get_image_exif

parser = argparse.ArgumentParser(
  prog='Group Photos - Non Interactive',
  description='This program splits a directory, searching recursively, images into their corresponding dates',
  epilog='Please mindful that although this program does not remove the original date it should be used with cautions')
parser.add_argument('read')
parser.add_argument('write')

logger.info("Application starting up 🚀")

# Retrieving parameters
args = parser.parse_args()
read_directory = args['read']
write_directory = args['write']
logger.trace("Some parameters were retrieved!")

# Write out parameters
logger.debug("The following parameters are being used:")
logger.debug(f"\tRead Directory: {read_directory}")
logger.debug(f"\tWrite Directory: {write_directory}")

# Checking if directory exists
logger.info("Checking if read directory exists")
if not read_directory.is_dir():
  logger.error("Read directory does not exist or can't be accessed")
  raise BaseException(f"Read directory '{read_directory}' does not exist or can't be accessed")

# Getting all images within directory
logger.info("Retrieving all images within read directory")
directory_entries = [
    os.path.join(dirpath, filename)
    for dirpath, _, filenames in os.walk(read_directory)
    for filename in filenames
]
directory_images = list(filter(lambda x: is_image(read_directory, x), directory_entries))
logger.info(f"From directory '#{len(directory_images)}' images were found")

# Iterating images and group accordingly
images_grouped: Dict[str, List[str]] = {}
for image_filename in directory_images:
  image_full_path = read_directory.joinpath(image_filename)

  image = Image.open(image_full_path)
  image_exif = get_image_exif(image)

  image_datetime_str = image_exif['DateTime']
  image_datetime = datetime.strptime(image_datetime_str, "%Y:%m:%d %H:%M:%S")

  image_date = datetime.strftime(image_datetime, '%Y.%m.%d')
  if image_date not in images_grouped:
    images_grouped[image_date] = []

  images_grouped[image_date].append(image_filename)

logger.info(f"Script generated '#{len(images_grouped.keys())}' groups of images")

# For each group associate the correct information
albums: List[Album] = []
for (album_date, images) in images_grouped.items():
  album = Album(album_date, None, images)

  logger.debug("A new album has been generated:")
  logger.debug(f"\tDate: {album.date}")
  logger.debug(f"\tPhotos: #{len(album.image_filenames)}")

  albums.append(album)

logger.info(f"Script generated '#{len(albums)}' albums")

# For each album save in the appropriate folder the images
for album in albums:
  fully_qualified_album = f"{album.date}"
  logger.debug(f"Preparing to save album '{fully_qualified_album}'")

  album_path = write_directory.joinpath(fully_qualified_album)
  album_path.mkdir(parents=True, exist_ok=True)
  logger.debug("Album folder created")

  for image_filename in album.image_filenames:
    image_path = read_directory.joinpath(image_filename)

    shutil.copy(image_path, album_path)
    logger.debug(f"Image '{image_filename}' copied into album '{fully_qualified_album}'")
  
  logger.debug("Album fully generated")

logger.info(f"Script saved '#{len(albums)}' albums")
