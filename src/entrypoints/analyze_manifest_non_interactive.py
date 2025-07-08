from pathlib import Path
from loguru import logger
import argparse
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from src.models.manifest import Manifest
from src.utils.file_utils import files_are_identical

parser = argparse.ArgumentParser(
    prog="Analyze - Non Interactive",
    description="This program takes in a manifest file and analyzes wether the operation carried out was succesfull or not",
)
parser.add_argument("manifest")

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
manifest_path = Path(args.manifest).absolute()
logger.trace("Some parameters were retrieved!")

# Write out parameters
logger.debug("The following parameters are being used:")
logger.debug(f"\tManifest Path: {manifest_path}")

# The manifest file will be read from the path
manifest = Manifest.load(manifest_path)

# Iterate the album in manifest
with logging_redirect_tqdm():
    progress_bar_albums = tqdm(manifest.albums, desc="Processing albums", leave=False)

    for album in progress_bar_albums:
        logger.debug(f"Processing album '{album}'")
        assets = manifest.albums[album]

        progress_bar_assets = tqdm(assets, desc="Processing assets", leave=False)
        for asset in progress_bar_assets:
            file_source_path = Path(asset.source)
            file_destination_path = Path(asset.destination)

            identical = files_are_identical(file_source_path, file_destination_path)
            if not identical:
                logger.error("\tFile with discrepancies found:")
                logger.error(f"\t- source: {asset.source}")
                logger.error(f"\t- destination: {asset.destination}")
