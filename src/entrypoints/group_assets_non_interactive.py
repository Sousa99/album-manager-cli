from datetime import datetime
import os
import shutil
from pathlib import Path
from loguru import logger
import argparse
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from src.models.album import Album
from src.models.manifest import Manifest
from src.utils.asset_utils import compute_asset_filename
from src.utils.image_non_graphic_utils import is_image, group_images
from src.utils.video_non_graphic_utils import group_videos, is_video

parser = argparse.ArgumentParser(
    prog="Group Photos - Non Interactive",
    description="This program splits a directory, searching recursively, images into their corresponding dates",
    epilog="Please mindful that although this program does not remove the original date it should be used with cautions",
)
parser.add_argument("read")
parser.add_argument("write")

# Logger configurations
logger_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> [<level>{level: ^12}</level>] <level>{message}</level>"
logger.configure(
    handlers=[
        dict(
            sink=lambda msg: tqdm.write(msg, end=""),
            format=logger_format,
            colorize=True,
        )
    ]
)
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

grouped_assets: dict[str, list[str]] = {}
for d in (
    grouped_images,
    grouped_videos,
):
    for key, value in d.items():
        if key not in grouped_assets:
            grouped_assets[key] = []

        grouped_assets[key].extend(value)

# For each group associate the correct information
albums: list[Album] = []
for album_date, assets in grouped_assets.items():
    album = Album(album_date, None, assets)

    logger.debug("A new album has been generated:")
    logger.debug(f"\tDate: {album.date}")
    logger.debug(f"\tAssets: #{len(album.asset_fullpaths)}")

    albums.append(album)

logger.info(f"Script generated '#{len(albums)}' albums")

# For each album save in the appropriate folder the images
manifest = Manifest(str(read_directory), str(write_directory))
failed_copies: int = 0
with logging_redirect_tqdm():
    progress_bar_albums = tqdm(albums, desc="Processing albums", leave=False)
    for album in progress_bar_albums:
        fully_qualified_album = album.get_qualified_name()
        logger.debug(f"Preparing to save album '{fully_qualified_album}'")

        album_path = write_directory.joinpath(fully_qualified_album)
        album_path.mkdir(parents=True, exist_ok=True)
        logger.debug("Album folder created")

        progress_bar_assets = tqdm(
            album.asset_fullpaths, desc="Processing assets", leave=False
        )
        for asset_fullpath_str in progress_bar_assets:
            asset_fullpath = Path(asset_fullpath_str)
            asset_filename = compute_asset_filename(
                album, asset_fullpath, read_directory
            )
            asset_fullpath_destination = album_path.joinpath(asset_filename)

            destination_already_exists = os.path.isfile(asset_fullpath_destination)
            if destination_already_exists:
                failed_copies += 1
                logger.error(
                    f"Asset '{asset_filename}' could not be copied to album '{fully_qualified_album}' as the file already exists"
                )

            shutil.copy2(asset_fullpath, album_path)
            manifest.add_entry(
                album=fully_qualified_album,
                source=asset_fullpath,
                destination=asset_fullpath_destination,
            )
            logger.debug(
                f"Asset '{asset_filename}' copied into album '{fully_qualified_album}'"
            )

        logger.debug("Album fully generated")

logger.info(f"Script saved '#{len(albums)}' albums")
logger.info(f"Script had '#{failed_copies}' failed copies")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
manifest_file = f"manifest_{timestamp}.json"
manifest_path = write_directory.joinpath(manifest_file)
manifest.save(manifest_path)
