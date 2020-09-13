#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import string
from pathlib import Path
from typing import List, Optional


def get_project_root() -> Path:
    return Path(__file__).parent


root = get_project_root()

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
