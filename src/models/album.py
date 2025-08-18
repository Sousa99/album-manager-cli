from dataclasses import dataclass
from typing import Optional


@dataclass
class Album:
    date: str
    name: Optional[str]
    asset_fullpaths: list[str]

    def get_qualified_name(
        self,
    ) -> str:
        """Get qualified name for album directory."""
        return f"{self.date}"
