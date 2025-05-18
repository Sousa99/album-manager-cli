import mimetypes
from typing import Any
import ffmpeg  # type: ignore
from datetime import datetime
from pathlib import Path


def is_video(directory: Path, file: str) -> bool:
    full_path = directory.joinpath(file)

    # If not a file, immediately return
    if not full_path.is_file():
        return False

    mimetypes_guess = mimetypes.guess_type(full_path)
    first_guess = mimetypes_guess[0]
    if not first_guess:
        return False

    return first_guess.startswith("video")


def get_video_info(video: str) -> dict[str, Any]:
    video_information = ffmpeg.probe(video)
    return video_information


def group_videos(videos: list[str]) -> dict[str, list[str]]:
    videos_grouped: dict[str, list[str]] = {}
    for video_filepath in videos:
        try:
            video_info = get_video_info(video_filepath)
        except Exception:
            video_info = {}

        video_key = "UNKNOWN"
        video_creation_time = (
            video_info.get("format", {}).get("tags", {}).get("creation_time", None)
        )
        if video_creation_time:
            video_datetime = datetime.strptime(
                video_creation_time, "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            video_key = datetime.strftime(video_datetime, "%Y.%m.%d")

        if video_key not in videos_grouped:
            videos_grouped[video_key] = []
        videos_grouped[video_key].append(video_filepath)

    return videos_grouped
