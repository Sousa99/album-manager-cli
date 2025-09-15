from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Dict, List


@dataclass
class FileEntry:
    filename: str
    version: str


@dataclass
class ManifestEntry:
    source: str
    filename: str
    filename_version: str
    destination: str


@dataclass
class Manifest:
    """
    This class serves as a final report of the execution, tracking every single asset processed. It identifies which assets are copied to which locations and records any repeats found among the assets.
    Attributes:
        read (str): The source directory from which assets are read.
        write (str): The target directory to which assets are written.
        albums (Dict[str, List[ManifestEntry]]): Maps album names to lists of manifest entries, detailing assets copied for each album.
        repeats (List[ManifestEntry]): List of manifest entries representing assets identified as repeats.
    """

    read: str
    write: str
    albums: Dict[str, List[ManifestEntry]] = field(default_factory=dict)
    repeats: List[ManifestEntry] = field(default_factory=list)

    def add_album_entry(self, album: str, manifest_entry: ManifestEntry) -> None:
        """Add a file copy entry to a specific album."""
        if album not in self.albums:
            self.albums[album] = []
        self.albums[album].append(manifest_entry)

    def add_repeat_entry(self, manifest_entry: ManifestEntry) -> None:
        """Add a file copy entry to the repeats list."""
        self.repeats.append(manifest_entry)

    def save(self, path: Path) -> None:
        """Write the manifest to a JSON file."""
        with path.open("w", encoding="utf-8") as file:
            json.dump(asdict(self), file, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: Path) -> "Manifest":
        """Read a manifest from a JSON file."""
        with path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)

        read = raw_data["read"]
        write = raw_data["write"]
        albums: Dict[str, List[ManifestEntry]] = {
            album: [ManifestEntry(**entry) for entry in entries]
            for album, entries in raw_data["albums"].items()
        }
        repeats: List[ManifestEntry] = [
            ManifestEntry(**entry) for entry in raw_data["repeats"]
        ]

        return cls(read=read, write=write, albums=albums, repeats=repeats)
