import os
from pathlib import Path
from src.constants.file_constants import UNCATEGORIZED_ALBUM
from src.models.album import Album
from src.utils.file_utils import files_are_identical


def compute_asset_filename(
    album: Album, asset_fullpath: Path, read_directory: Path
) -> str:
    original_filename: str = asset_fullpath.name
    if album.name == UNCATEGORIZED_ALBUM:
        relative_read_path = asset_fullpath.relative_to(read_directory)

        directory_parts = relative_read_path.parent.parts
        key = " - ".join(directory_parts)

        original_filename = f"{key} - {original_filename}"

    return original_filename


def check_copy_creates_conflict(
    path_to_file: Path,
    write_path: Path,
) -> bool:
    destination_already_exists = os.path.isfile(write_path)
    if not destination_already_exists:
        return False

    same_content = files_are_identical(path_to_file, write_path)
    return not same_content
