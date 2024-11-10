from dataclasses import dataclass

@dataclass
class Album:
  date: str
  name: str
  image_filenames: list[str]