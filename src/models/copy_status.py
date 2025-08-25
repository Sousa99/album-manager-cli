from enum import Enum


class CopyStatus(Enum):
    """
    Enum representing the status of a file copy operation.

    Attributes:
        FREE: The file path is free for the file to be copied.
        REPEAT: The file path is occupied, but the file being copied is the same as the one already there.
        CONFLICT: The file path is occupied, and the file being copied is different from the one already there.
    """

    FREE = "FREE"
    REPEAT = "REPEAT"
    CONFLICT = "CONFLICT"
