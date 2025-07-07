from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Dict, List, TypedDict, Union


@dataclass
class ManifestEntry:
    source: str
    destination: str


@dataclass
class Manifest:
    albums: Dict[str, List[ManifestEntry]] = field(default_factory=dict)

    def add_entry(
        self, album: str, source: Union[str, Path], destination: Union[str, Path]
    ) -> None:
        """Add a file copy entry to a specific album."""
        entry = ManifestEntry(source=str(source), destination=str(destination))
        if album not in self.albums:
            self.albums[album] = []
        self.albums[album].append(entry)

    def save(self, path: Path) -> None:
        """Write the manifest to a JSON file."""
        with path.open("w", encoding="utf-8") as file:
            json.dump(asdict(self), file, indent=2, ensure_ascii=False)
