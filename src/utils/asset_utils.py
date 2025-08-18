from pathlib import Path
from src.constants.file_constants import UNCATEGORIZED_ALBUM
from src.models.album import Album


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
