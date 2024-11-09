from dataclasses import dataclass
from datetime import date

@dataclass
class Album:
  date: date
  name: str
  image_filenames: list[str]