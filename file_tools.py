#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import string
from os import PathLike
from pathlib import Path
from typing import List, Optional, Union

from user_input import choose_year, get_year_input, check_delete_file

FILE_TYPES = ['.m4v', '.mpeg', '.mpg', '.mp4', '.mpe', '.avi', '.mkv', '.mxf', '.wmv', '.ogg', '.divx', '.srt', '.sub',
              ".ssa", ".ass", ".usf", ".ssf"]
EXT_TO_KEEP = ['.jpg', '.png', '.vob', '.ifo', '.bup', '.sfv', '.rar', '.subs', '.idx', '.iso']
BLACK_LIST = ['VIDEO_TS']
SUBTITLE_EXTENSIONS = ['.sub', '.srt', ".ssa", ".ass", ".usf", ".ssf"]


def get_project_root() -> Union[str, bytes, os.PathLike]:
    return Path(__file__).parent


root: Union[str, bytes, PathLike] = get_project_root()

torrent_data = os.path.join(root, "names_to_clean.txt")
codings = os.path.join(root, "audio_video_information.txt")


class UnsplittableError(Exception):
    pass


def remove_additional_spacing(name) -> str:
    return re.sub(' +', ' ', name)


def extract_year(title) -> Optional[int]:
    match = re.findall(r'([1-2][0-9]{3})', title)
    for i in match:
        if int(i) > 1900:
            return int(i)


def split_name(name: str, character: str) -> List:
    if character in name:
        return name.split(character)
    else:
        raise UnsplittableError


def check_int(year) -> bool:
    return isinstance(year, int)


def clean_punctuation(name: str) -> str:
    characters = ['(', ')', '()', '( )', '[]']
    for character in characters:
        name = name.replace(character, '')
    name = name.replace('[', '(').replace(']', ')')
    return name.replace('.', ' ').replace('_', ' ').replace('–', ' ').replace('-', ' ')


def clean_name(name: str, year: int) -> str:
    name = name.replace(str(year), '')
    with open(codings) as file:
        for line in file:
            line = line.replace('\n', '')
            name = name.lower().replace(line.lower(), '')
    with open(torrent_data) as file:
        for line in file:
            line = line.replace('\n', '')
            name = name.lower().replace(line.lower(), '')
    name = clean_punctuation(name)
    name = remove_additional_spacing(name).strip()
    name = string.capwords(name, ' ')
    return name


def delete_file(path: Union[str, bytes, os.PathLike]) -> None:
    try:
        os.remove(path)
    except Exception as e:
        print(e)


class FileMaster:
    def __init__(self, original_name: str) -> None:
        self.original_name = original_name
        self.cleaned_name = self.parse_file_name(original_name)

    is_removable: bool = False
    is_updated: bool = False
    is_filename: bool = False
    extension: str = ''
    file_year: Optional[int] = None
    parent_dir = None

    def parse_file_name(self, name: str) -> str:
        if self.is_filename:
            filename_txt, self.extension = os.path.splitext(name)
        else:
            filename_txt = name

        self.file_year: Optional[int] = extract_year(filename_txt)
        set_year = self.set_file_year_for_string()
        cleaned_filename = clean_name(filename_txt, self.file_year)
        titlecase_filename = string.capwords(cleaned_filename, ' ')
        titlecase_filename = titlecase_filename.replace("'S", "'s")

        file_name = f"{titlecase_filename} {set_year or ''}{self.extension or ''}"

        return remove_additional_spacing(file_name).strip()

    def set_file_year_for_string(self) -> str:
        # Write test for this
        if self.parent_dir and self.parent_dir.file_year:
            if not self.file_year:
                return f"({self.parent_dir.file_year})"
            elif self.parent_dir.file_year != self.file_year:
                chosen_year = choose_year(
                    name=self.original_name,
                    file_year=self.file_year,
                    folder_year=self.parent_dir.file_year
                )
                return f"({chosen_year})"
        else:
            if self.file_year:
                return f"({self.file_year})"
            else:
                return f"({get_year_input(self.original_name)})"

    def set_is_filename(self):
        self.is_filename = True


class Directory(FileMaster):
    def __init__(self, original_name: str) -> None:
        super().__init__(original_name)
        self.should_rename = self.can_rename()

    def can_rename(self) -> bool:
        if self.original_name in BLACK_LIST:
            return False
        else:
            return True


class Filename(FileMaster):
    def __init__(self, original_name: str, parent_dir: Directory) -> None:
        self.parent_dir = parent_dir
        self.set_is_filename()
        super().__init__(original_name)
        self.should_rename = self.can_rename()
        self.is_junk = self.can_remove()

    def can_rename(self) -> bool:
        if self.original_name in BLACK_LIST:
            return False

        if self.extension:
            is_rar_sequence = re.search(r'(.*?)((part\[\d+\])?\.r[0-9]+)', self.extension)
            if is_rar_sequence:
                return False
            else:
                return True

    def can_remove(self) -> bool:
        ext = self.extension.lower()
        filename = self.original_name

        if self.original_name[0] == '.':
            return True

        if ext.lower() == 'jpg' and filename == 'WWW.YIFY - TORRENTS.COM' or 'WWW.YTS.RE':
            return True

        if self.original_name.lower() == 'sample.mp4':
            return True

        if ext not in FILE_TYPES and ext not in EXT_TO_KEEP:
            if ext == '.txt' or ext == '.rtf':
                return True
            else:
                return check_delete_file(self.parent_dir.original_name, self.original_name)

    # def clean_subtitle(self) -> str:
    #     ext = self.extension.lower()
    #     filename = self.cleaned_name
    #     if ext in SUBTITLE_EXTENSIONS:
    #         filename_txt, self.extension = os.path.splitext(filename)
    #
    #         self.subtitle_file = f"{titlecase_filename} {set_year or ''} – {self.extension or ''}"


