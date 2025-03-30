from dataclasses import dataclass
from typing import Optional

@dataclass
class Album:
  date: str
  name: Optional[str]
  image_filenames: list[str]