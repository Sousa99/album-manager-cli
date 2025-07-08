import hashlib
from pathlib import Path


def hash_file(path: Path, algorithm: str = "sha256") -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def files_are_identical(path1: Path, path2: Path) -> bool:
    return hash_file(path1) == hash_file(path2)
