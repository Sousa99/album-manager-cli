import os
import shutil
from typing import Dict, List
from pathlib import Path
from loguru import logger
import argparse

from src.models.album import Album
from src.utils.image_non_graphic_utils import is_image, group_images
from src.utils.video_non_graphic_utils import group_videos, is_video

parser = argparse.ArgumentParser(
    prog="Group Photos - Non Interactive",
    description="This program splits a directory, searching recursively, images into their corresponding dates",
    epilog="Please mindful that although this program does not remove the original date it should be used with cautions",
)
parser.add_argument("read")
parser.add_argument("write")

logger.info("Application starting up 🚀")

# Retrieving parameters
args = parser.parse_args()
read_directory = Path(args.read).absolute()
write_directory = Path(args.write).absolute()
logger.trace("Some parameters were retrieved!")

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
directory_entries = [
    os.path.join(dirpath, filename)
    for dirpath, _, filenames in os.walk(read_directory)
    for filename in filenames
]
directory_images = list(
    filter(lambda x: is_image(read_directory, x), directory_entries)
)
directory_videos = list(
    filter(lambda x: is_video(read_directory, x), directory_entries)
)

logger.info(f"From directory '#{len(directory_images)}' images were found")
logger.info(f"From directory '#{len(directory_videos)}' videos were found")

# Group images and videos accordingly
grouped_images = group_images(directory_images)
grouped_videos = group_videos(directory_videos)

logger.info(f"Script generated '#{len(grouped_images.keys())}' groups of images")
logger.info(f"Script generated '#{len(grouped_videos.keys())}' groups of videos")

grouped_assets: Dict[str, List[str]] = {}
for d in (
    grouped_images,
    grouped_videos,
):  # you can list as many input dicts as you want here
    for key, value in d.items():
        if key not in grouped_assets:
            grouped_assets[key] = []

        grouped_assets[key].extend(value)

# For each group associate the correct information
albums: List[Album] = []
for album_date, assets in grouped_assets.items():
    album = Album(album_date, None, assets)

    logger.debug("A new album has been generated:")
    logger.debug(f"\tDate: {album.date}")
    logger.debug(f"\tAssets: #{len(album.asset_fullpaths)}")

    albums.append(album)

logger.info(f"Script generated '#{len(albums)}' albums")

# For each album save in the appropriate folder the images
for album in albums:
    fully_qualified_album = f"{album.date}"
    logger.debug(f"Preparing to save album '{fully_qualified_album}'")

    album_path = write_directory.joinpath(fully_qualified_album)
    album_path.mkdir(parents=True, exist_ok=True)
    logger.debug("Album folder created")

    for asset_fullpath_str in album.asset_fullpaths:
        asset_fullpath = Path(asset_fullpath_str)
        asset_filename = asset_fullpath.name

        shutil.copy(asset_fullpath, album_path)
        logger.debug(
            f"Asset '{asset_filename}' copied into album '{fully_qualified_album}'"
        )

    logger.debug("Album fully generated")

logger.info(f"Script saved '#{len(albums)}' albums")
