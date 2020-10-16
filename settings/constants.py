import os
from pathlib import Path
from typing import Union


def get_project_root() -> Union[str, bytes, os.PathLike]:
    return Path(__file__).parent


root: Union[str, bytes, os.PathLike] = get_project_root()


FILE_TYPES = [
    ".m4v",
    ".mpeg",
    ".mpg",
    ".mp4",
    ".mpe",
    ".avi",
    ".mkv",
    ".mxf",
    ".wmv",
    ".ogg",
    ".divx",
    ".srt",
    ".sub",
    ".ssa",
    ".ass",
    ".usf",
    ".ssf",
]
EXT_TO_KEEP = [
    ".jpg",
    ".png",
    ".vob",
    ".ifo",
    ".bup",
    ".sfv",
    ".rar",
    ".subs",
    ".idx",
    ".iso",
]
BLACK_LIST = ["VIDEO_TS", "subs"]
SUBTITLE_EXTENSIONS = [".sub", ".srt", ".ssa", ".ass", ".usf", ".ssf"]
TORRENT_DATA = os.path.join(root, "names_to_clean.txt")
CODINGS = os.path.join(root, "audio_video_information.txt")
LANGUAGES_JSON = os.path.join(root, "languages.json")
DELETE_FILES = os.path.join(root, "delete_files.txt")
