from __future__ import annotations

from pathlib import Path
import shutil

import loguru
from src.models.copy_status import CopyStatus
from src.models.manifest import Manifest


def update_manifest_with_copy_status(
    manifest: Manifest,
    copy_status: CopyStatus,
    asset_filename: str,
    asset_source: Path,
    asset_destination: Path,
    album_name: str,
    album_path: Path,
    logger: loguru.Logger,
) -> None:
    """Update the manifest with the result of a copy operation."""

    if copy_status == CopyStatus.FREE:
        update_manifest_free(
            manifest,
            asset_filename,
            asset_source,
            asset_destination,
            album_name,
            album_path,
            logger,
        )
    elif copy_status == CopyStatus.REPEAT:
        update_manifest_repeat(
            manifest,
            asset_filename,
            asset_source,
            asset_destination,
            album_name,
            logger,
        )
    elif copy_status == CopyStatus.CONFLICT:
        update_manifest_conflict(
            manifest,
            asset_filename,
            asset_source,
            asset_destination,
            album_name,
            logger,
        )


def update_manifest_free(
    manifest: Manifest,
    asset_filename: str,
    asset_source: Path,
    asset_destination: Path,
    album_name: str,
    album_path: Path,
    logger: loguru.Logger,
) -> None:
    """Update the manifest with a successful copy operation."""
    shutil.copy2(asset_source, album_path)
    manifest.add_album_entry(
        album=album_name,
        source=asset_source,
        destination=asset_destination,
    )
    logger.debug(f"Asset '{asset_filename}' copied into album '{album_name}'")


def update_manifest_repeat(
    manifest: Manifest,
    asset_filename: str,
    asset_source: Path,
    asset_destination: Path,
    album_name: str,
    logger: loguru.Logger,
) -> None:
    """
    Update the manifest when the file already exists and is identical (repeat copy).
    No copy is performed, but the manifest is updated and the event is logged.
    """
    manifest.add_repeat_entry(
        source=asset_source,
        destination=asset_destination,
    )
    logger.debug(
        f"Asset '{asset_filename}' already exists in album '{album_name}' (repeat copy)."
    )


def update_manifest_conflict(
    manifest: Manifest,
    asset_filename: str,
    asset_source: Path,
    asset_destination: Path,
    album_name: str,
    logger: loguru.Logger,
) -> None:
    """
    Update the manifest when there is a conflict (file exists but is different).
    Adds a failure entry and logs the conflict event.
    """
    manifest.add_failure_entry(
        source=asset_source,
        destination=asset_destination,
    )
    logger.error(
        f"Asset '{asset_filename}' could not be copied to album '{album_name}' as the file already exists"
    )
