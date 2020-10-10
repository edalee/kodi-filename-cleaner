import logging
import re
import string
from typing import Optional

from settings.constants import LANGUAGES_JSON, CODINGS, TORRENT_DATA
from utils.utils import read_file_json


class FileException(Exception):
    pass


logger = logging.getLogger(__name__)


def extract_year(title) -> Optional[int]:
    match = re.findall(r'([1-2][0-9]{3})', title)
    for i in match:
        if int(i) > 1900:
            return int(i)


def check_for_language(name: str) -> str:
    try:
        languages = read_file_json(LANGUAGES_JSON)
    except FileException as err:
        logger.error(f'Fail to read language json', extra=dict(error=err))
        raise

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


def remove_additional_spacing(name) -> str:
    return re.sub(' +', ' ', name)


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
