#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import re
import string
from os import PathLike
from typing import List, Optional, Union, Dict, Tuple

from constants import CODINGS, TORRENT_DATA, SUBTITLE_EXTENSIONS, BLACK_LIST, FILE_TYPES, EXT_TO_KEEP, LANGUAGES_JSON
from user_input import choose_year, get_year_input, check_delete_file, get_show_input


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


def parse_series_episode(name: str, is_file: bool) -> str:
    formatted_series_episodes: List[str] = []

    reg = re.compile(
        r'''[a-zA-Z]\d{1,2} | \bseason\s?\d+\b | \bseries\s?\d+\b | 
          \bepisode\s?\d+\b | \d{1,2}[x|X]\d{1,2} | [x|X]\d{1,2}''',
        flags=re.I | re.X
    )
    original_find = re.findall(reg, name)
    if not original_find:
        formatted_series_episodes: List[str] = get_show_input(name, is_file)

    for find in original_find:
        find_lower: str = find.lower()

        if 'season' in find_lower or 'series' in find_lower:
            number = list(map(int, re.findall(r'\d+', find_lower)))
            series = f"s{number[0]:02d}"
            if series not in formatted_series_episodes:
                formatted_series_episodes.append(series)
                continue
        if 'episode' in find_lower or 'x' in find_lower:
            number = list(map(int, re.findall(r'\d+', find_lower)))
            episode = f"e{number[0]:02d}"
            if episode not in formatted_series_episodes:
                formatted_series_episodes.append(episode)
                continue
        if 'x' in find_lower and find_lower[0].isdigit():
            series = f"s{find_lower}"
            if series not in formatted_series_episodes:
                formatted_series_episodes.append(series)
                continue
        if 'x' in find_lower and not find_lower[0].isalpha:
            series = f"s{find_lower}"
            if series not in formatted_series_episodes:
                formatted_series_episodes.append(series)
                continue
        if 's' in find_lower and find_lower not in formatted_series_episodes or 'e' in find_lower and find_lower not in formatted_series_episodes:
            if len(find_lower) == 2:
                series_episodes = find_lower.replace('s', 's0').replace('e', 'e0')
            else:
                series_episodes = find_lower
            formatted_series_episodes.append(series_episodes)

    if formatted_series_episodes:
        formatted_series_episodes.sort(reverse=True)
        uppercase_series_info = ''.join([x.upper() for x in formatted_series_episodes])

    return uppercase_series_info


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
    defined_year: Optional[int] = None
    parent_dir = None

    def parse_file_name(self, name: str) -> str:
        if self.is_filename:
            filename_txt, self.extension = os.path.splitext(name)
        else:
            filename_txt = name

        self.file_year: Optional[int] = extract_year(filename_txt)
        self.defined_year = self.set_file_year_for_string()
        cleaned_filename = clean_name(filename_txt, self.file_year)
        titlecase_filename = string.capwords(cleaned_filename, ' ')
        apostrophe_fixed = titlecase_filename.replace("'S", "'s")

        # file_name = f"{apostrophe_fixed} {self.defined_year or ''}{self.extension or ''}"

        return remove_additional_spacing(apostrophe_fixed).strip()

    def set_file_year_for_string(self) -> int:
        # Write test for this
        if self.parent_dir and self.parent_dir.file_year:
            if not self.file_year:
                return self.parent_dir.file_year
            elif self.parent_dir.file_year != self.file_year:
                chosen_year = choose_year(
                    name=self.original_name,
                    file_year=self.file_year,
                    folder_year=self.parent_dir.file_year
                )
                return chosen_year
            else:
                return self.file_year
        else:
            if self.file_year:
                return self.file_year
            else:
                return get_year_input(self.original_name)

    def set_is_filename(self):
        self.is_filename = True

    @staticmethod
    def clean_and_reformat_name(_filename_txt: str, item_to_remove: str):
        clean_filename = _filename_txt.lower().replace(item_to_remove, '')
        stripped_filename = remove_additional_spacing(clean_filename).strip()
        return string.capwords(stripped_filename, ' ')


class Directory(FileMaster):
    def __init__(self, original_name: str) -> None:
        super().__init__(original_name)
        self.should_rename = self.can_rename()

    def can_rename(self) -> bool:
        if self.original_name in BLACK_LIST:
            return False
        else:
            return True

    def __str__(self):
        file_name = f"{self.cleaned_name} ({self.defined_year or ''})"
        return remove_additional_spacing(file_name).strip()


class Filename(FileMaster):
    def __init__(self, original_name: str, parent_dir: Directory) -> None:
        self.parent_dir = parent_dir
        self.set_is_filename()
        super().__init__(original_name)
        self.should_rename: bool = self.can_rename()
        self.is_junk: bool = self.can_remove()
        self.subtitle_filename: Optional[str] = self.clean_subtitle()

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

    def clean_subtitle(self) -> Optional[str]:
        filename_txt = self.cleaned_name
        extension = self.extension.lower()
        if extension in SUBTITLE_EXTENSIONS:
            language_identifier = check_for_language(filename_txt)
            if language_identifier:
                filename_txt = self.clean_and_reformat_name(filename_txt, language_identifier.lower())
            return f"{filename_txt} ({self.defined_year}) – {language_identifier or ''}{extension or ''}"
        else:
            return None

    def __str__(self):
        file_name = f"{self.cleaned_name} ({self.defined_year or ''}){self.extension or ''}"
        return remove_additional_spacing(file_name).strip()


class SeriesMaster(FileMaster):
    def __init__(self, original_name: str, parent_dir: Directory) -> None:
        super().__init__(original_name, parent_dir)
        self.series_info: List[str] = parse_series_episode(self.cleaned_name, self.is_filename)

    def __str__(self):
        for find in self.series_info:
            removed_series_info_txt = self.clean_and_reformat_name(self.cleaned_name, find.lower())
        file_name = f"{removed_series_info_txt} {self.defined_year or ''} {self.series_info or ''}"

        return remove_additional_spacing(file_name).strip()

