#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import re
import string
from typing import List, Optional

from settings.constants import SUBTITLE_EXTENSIONS, BLACK_LIST, FILE_TYPES, EXT_TO_KEEP
from utils import name_tools
from utils.user_input import choose_year, get_year_input, check_delete_file, get_show_input

logger = logging.getLogger(__name__)


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

        self.file_year: Optional[int] = name_tools.extract_year(filename_txt)
        self.defined_year = self.set_file_year_for_string()
        cleaned_filename = name_tools.clean_name(filename_txt, self.file_year)
        title_case_filename = string.capwords(cleaned_filename, ' ')
        apostrophe_fixed = title_case_filename.replace("'S", "'s")

        return name_tools.remove_additional_spacing(apostrophe_fixed).strip()

    def set_file_year_for_string(self) -> int:
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
        stripped_filename = name_tools.remove_additional_spacing(clean_filename).strip()
        return string.capwords(stripped_filename, ' ')


class Directory(FileMaster):
    def __init__(self, original_name: str) -> None:
        super().__init__(original_name)
        self.should_rename = self.can_rename()
        self.is_removable = self.can_remove()

    def can_rename(self) -> bool:
        if self.original_name in BLACK_LIST:
            return False
        else:
            return True

    def can_remove(self) -> bool:
        if self.original_name[0] == '.':
            return True

        if self.original_name.lower() == 'extras':
            return True

    def __str__(self):
        file_name = f"{self.cleaned_name} ({self.defined_year or ''})"
        return name_tools.remove_additional_spacing(file_name).strip()


class Filename(FileMaster):
    def __init__(self, original_name: str, parent_dir: Directory) -> None:
        self.parent_dir = parent_dir
        self.set_is_filename()
        super().__init__(original_name)
        self.should_rename: bool = self.can_rename()
        self.is_removable: bool = self.can_remove()
        self.subtitle_language: str = self.clean_subtitle()

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
            language_identifier = name_tools.check_for_language(filename_txt)
            if language_identifier:
                filename_txt = self.clean_and_reformat_name(filename_txt, language_identifier.lower())
                self.cleaned_name = filename_txt
                return f" – {language_identifier}"

    def __str__(self):
        file_name = (
            f"{self.cleaned_name} ({self.defined_year or ''}){self.subtitle_language or ''}{self.extension or ''}"
        )
        return name_tools.remove_additional_spacing(file_name).strip()


class SeriesMaster(FileMaster):
    def __init__(self) -> None:
        self.series_info: str = self.clean_series()

    def parse_series_episode(self) -> str:
        formatted_series_episodes: List[str] = []
        name = self.cleaned_name
        is_file = self.is_filename

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

        uppercase_series_info: str = ''.join([x.upper() for x in formatted_series_episodes])

        return uppercase_series_info

    def clean_series(self) -> str:
        series_info: str = self.parse_series_episode()
        removed_series_info_txt = self.clean_and_reformat_name(self.cleaned_name, series_info.lower())
        self.cleaned_name = name_tools.remove_additional_spacing(removed_series_info_txt).strip()
        return series_info.upper()


class SeriesDirectory(SeriesMaster, Directory):
    def __init__(self, original_name: str) -> None:
        Directory.__init__(self, original_name)
        SeriesMaster.__init__(self)

    def __str__(self):
        file_name = f"{self.cleaned_name} ({self.defined_year or ''}) {self.series_info.upper() or ''}"
        return name_tools.remove_additional_spacing(file_name).strip()


class SeriesFilename(SeriesMaster, Filename):
    def __init__(self, original_name: str, parent_dir: Directory) -> None:
        Filename.__init__(self, original_name, parent_dir)
        SeriesMaster.__init__(self)

    def __str__(self):
        file_name = (
            f"{self.cleaned_name} ({self.defined_year or ''}) {self.series_info.upper() or ''}"
            f"{self.subtitle_language or ''}{self.extension or ''}"
        )
        return name_tools.remove_additional_spacing(file_name).strip()
