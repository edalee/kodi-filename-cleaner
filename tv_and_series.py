#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import string
from typing import Tuple, Optional

from file_tools import remove_additional_spacing, clean_name
from user_input import get_show_input


def get_series_episode_info(cleaned_filename: str, year: int, series_search: bool) -> Tuple[str, str]:
    reg = re.compile(
        r'''[a-zA-Z]\d{1,2} | \bseason\s?\d+\b | \bseries\s?\d+\b | 
            \bepisode\s?\d+\b | \d{1,2}[x|X]\d{1,2} | [x|X]\d{1,2}''',
        flags=re.I | re.X
    )
    original_find = re.findall(reg, cleaned_filename)
    formatted_series_episode = []

    for i in original_find:
        x = i.lower()
        if 'season' in x or 'series' in x:
            num = list(map(int, re.findall(r'\d+', x)))
            ser = f"s{num[0]:02d}"
            if ser not in formatted_series_episode:
                formatted_series_episode.append(ser)
                continue
        if 'episode' in x or 'x' in x:
            num = list(map(int, re.findall(r'\d+', x)))
            epi = f"e{num[0]:02d}"
            if epi not in formatted_series_episode:
                formatted_series_episode.append(epi)
                continue
        if 'x' in x and x[0].isdigit():
            ser = f"s{x}"
            if ser not in formatted_series_episode:
                formatted_series_episode.append(ser)
                continue
        if 'x' in x and not x[0].isalpha:
            ser = f"s{x}"
            if ser not in formatted_series_episode:
                formatted_series_episode.append(ser)
                continue
        if 's' in x and x not in formatted_series_episode or 'e' in x and x not in formatted_series_episode:
            if len(x) == 2:
                ser_epi = x.replace('s', 's0').replace('e', 'e0')
            else:
                ser_epi = x
            formatted_series_episode.append(ser_epi)

    if not original_find:
        if series_search:
            formatted_series_episode = get_series_input(cleaned_filename)
        else:
            formatted_series_episode = get_show_input(cleaned_filename)

    if formatted_series_episode:
        formatted_series_episode = list(formatted_series_episode)
        formatted_series_episode.sort(reverse=True)
        formatted_series_episode = ''.join([x.upper() for x in formatted_series_episode])

    removed_series_episode = cleaned_filename.lower()
    for x in original_find:
        removed_series_episode = removed_series_episode.replace(x.lower(), '')

    # removed_series_episode = [cleaned_filename.i for i in original_find]
    title_cased_name = remove_additional_spacing(removed_series_episode)
    clean_again_file_name = clean_name(title_cased_name, year)
    title_cased_name = string.capwords(clean_again_file_name, ' ')

    if series_search:
        return formatted_series_episode, title_cased_name
    else:
        return formatted_series_episode, title_cased_name


def get_series_input(name: str) -> Optional[str]:
    while True:
        try:
            series = str(input(f'Add series (eg: S01, for "{name}" or c to skip : '))
            if series.lower().startswith('s'):
                return series.upper()
            if series.lower() == 'c':
                return None
        except ValueError:
            print("The input was not a valid series")
