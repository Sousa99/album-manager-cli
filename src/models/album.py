from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Album:
    date: str
    name: Optional[str]
    image_filenames: List[str]
