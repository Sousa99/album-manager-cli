from dataclasses import dataclass, field
from pathlib import Path
from sys import version
from typing import Dict, Optional, TypeAlias

from src.constants.file_constants import UNCATEGORIZED_ALBUM
from src.utils.file_utils import hash_file

LedgerEntryHash: TypeAlias = str
AssetFilename: TypeAlias = str
AlbumName: TypeAlias = str


@dataclass
class LedgerEntry:
    version: str
    source: str
    destination: str


AssetEntries: TypeAlias = Dict[LedgerEntryHash, LedgerEntry]
AlbumEntries: TypeAlias = Dict[AssetFilename, AssetEntries]
LedgerInformation: TypeAlias = Dict[AlbumName, AlbumEntries]


@dataclass
class Ledger:
    """
    This class is used to keep track during code execution of the ongoing assets, where they are copied over, and to track repeats in assets.
    Attributes:
      information (LedgerInformation): Stores ledger information mapping album names to their respective asset entries.
    """

    information: LedgerInformation = field(default_factory=dict)

    def check_matching_entry(
        self, album_name: AlbumName, source: Path
    ) -> Optional[LedgerEntry]:
        """Check if there is a matching ledger entry for the given album and source path."""

        album: Optional[AlbumEntries] = self.information.get(album_name)
        if not album:
            return None

        asset_filename: str = source.name
        asset_entries: Optional[AssetEntries] = album.get(asset_filename)
        if not asset_entries:
            return None

        asset_hash: str = hash_file(source)
        asset_entry: Optional[LedgerEntry] = asset_entries.get(asset_hash)
        if asset_entry:
            return asset_entry

        return None

    def get_number_file_version(
        self, album_name: AlbumName, asset_filename: AssetFilename
    ) -> int:
        """Get the version number of a specific asset file in a given album."""

        album: Optional[AlbumEntries] = self.information.get(album_name)
        if not album:
            return 0

        asset_entries: Optional[AssetEntries] = album.get(asset_filename)
        if not asset_entries:
            return 0

        return len(asset_entries)

    def compute_version(
        self, album_name: AlbumName, source: Path, read_directory: Path
    ) -> str:
        """Compute the version string for a given asset file in a specific album."""

        if album_name == UNCATEGORIZED_ALBUM:
            relative_read_path = source.relative_to(read_directory)

            directory_parts = relative_read_path.parent.parts
            key = "_".join(directory_parts)
            return f"AM_{key}"

        else:
            number_versions: int = self.get_number_file_version(album_name, source.name)
            number_formatted: str = f"{number_versions + 1:04d}"

            return f"AM_{number_formatted}"

    def add_entry(
        self,
        album_name: AlbumName,
        asset_filename: AssetFilename,
        source: Path,
        destination: Path,
    ) -> LedgerEntry:
        """Add a new entry to the ledger."""

        check_existing = self.check_matching_entry(album_name, source)
        if check_existing:
            raise ValueError("Entry already exists in the ledger.")

        new_entry = LedgerEntry(
            version=version, source=str(source), destination=str(destination)
        )

        album: AlbumEntries = self.information.setdefault(album_name, {})
        asset_entries: AssetEntries = album.setdefault(asset_filename, {})

        computed_hash: str = hash_file(source)
        asset_entries[computed_hash] = new_entry

        return new_entry
