#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import re
import string
from os import PathLike
from typing import List, Optional, Union, Dict

from constants import CODINGS, TORRENT_DATA, SUBTITLE_EXTENSIONS, BLACK_LIST, FILE_TYPES, EXT_TO_KEEP, LANGUAGES_JSON
from user_input import choose_year, get_year_input, check_delete_file


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


def get_languages(languages_json: Union[str, bytes, PathLike]) -> List[Dict]:
    with open(languages_json) as f:
        return json.load(f)


def check_for_language(name: str) -> str:
    languages = get_languages(LANGUAGES_JSON)
    for language in languages:
        for identifier in language.values():
            if (' ' + identifier + ' ') in (' ' + name.lower() + ' '):
                return identifier


def clean_punctuation(name: str) -> str:
    characters = ['(', ')', '()', '( )', '[]']
    for character in characters:
        name = name.replace(character, '')
    name = name.replace('[', '(').replace(']', ')')
    return name.replace('.', ' ').replace('_', ' ').replace('–', ' ').replace('-', ' ')


def clean_name(name: str, year: int) -> str:
    name = name.replace(str(year), '')
    with open(CODINGS) as file:
        for line in file:
            line = line.replace('\n', '')
            name = name.lower().replace(line.lower(), '')
    with open(TORRENT_DATA) as file:
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


def clean_subtitle(filename: str) -> Optional[str]:
    filename_txt, extension = os.path.splitext(filename)

    if extension.lower() in SUBTITLE_EXTENSIONS:
        language_identifier = check_for_language(filename_txt)
        if language_identifier:
            filename_txt = filename_txt.lower().replace(language_identifier, '')
            filename_txt = remove_additional_spacing(filename_txt).strip()
            filename_txt = string.capwords(filename_txt, ' ')
        return f"{filename_txt} – {language_identifier or ''}{extension or ''}"
    else:
        None


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
                return f"({self.file_year})"
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
        self.should_rename: bool = self.can_rename()
        self.is_junk: bool = self.can_remove()
        self.subtitle_filename: Optional[str] = clean_subtitle(self.cleaned_name)

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
