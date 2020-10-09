import re
import string
from typing import Optional

from constants import LANGUAGES_JSON, CODINGS, TORRENT_DATA
from utils.utils import read_file_json, clean_punctuation, remove_additional_spacing


def extract_year(title) -> Optional[int]:
    match = re.findall(r'([1-2][0-9]{3})', title)
    for i in match:
        if int(i) > 1900:
            return int(i)


def check_for_language(name: str) -> str:
    languages = read_file_json(LANGUAGES_JSON)
    file_words = name.split(' ')

    for language in languages:
        for identifier in language.values():
            identifier = identifier.lower()
            file_name = name.lower()
            if (' ' + identifier + ' ') in (' ' + file_name + ' '):
                return identifier
            else:
                for word in file_words:
                    if word.lower() == identifier:
                        return identifier


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


