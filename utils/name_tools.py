import logging
import re
import string
from contextlib import contextmanager
from typing import Optional

from settings import constants
from utils.utils import read_file_json


class FileException(Exception):
    pass


logger = logging.getLogger(__name__)


class Cleaner(object):
    def __init__(self, filename):
        self.file_name = filename

    @contextmanager
    def open_file(self):
        try:
            file = open(self.file_name, "r")
            lines = [line.replace("\n", "") for line in file]
            yield lines
        finally:
            file.close()

    def clean_name(self, name: str):
        name = name
        with self.open_file() as file:
            for line in file:
                name = name.lower().replace(line.lower(), "")
        return name

    def check_name(self, name: str):
        with self.open_file() as file:
            for line in file:
                if line.lower() in name.lower():
                    return True
            else:
                return False


def extract_year(title) -> Optional[int]:
    match = re.findall(r"([1-2][0-9]{3})", title)
    for i in match:
        if int(i) > 1900:
            return int(i)
    return None


def check_for_language(name: str) -> str:
    try:
        languages = read_file_json(constants.LANGUAGES_JSON)
    except FileException as err:
        logger.error("Fail to read language json", extra=dict(error=err))
        raise

    words = name.split(" ")

    for language in languages:
        for identifier in language.values():
            identifier = identifier.lower()
            file_name = name.lower()
            if (" " + identifier + " ") in (" " + file_name + " "):
                return str(identifier)
            else:
                for word in words:
                    if word.lower() == identifier:
                        return str(identifier)
    return ""


def remove_additional_spacing(name) -> str:
    return str(re.sub(" +", " ", name))


def clean_punctuation(name: str) -> str:
    characters = ["(", ")", "()", "( )", "[]"]
    for character in characters:
        name = name.replace(character, "")
    name = name.replace("[", "(").replace("]", ")")
    return name.replace(".", " ").replace("_", " ").replace("–", " ").replace("-", " ")


def clean_name(name: str, year: int) -> str:
    name = name.replace(str(year), "")

    cleaner = Cleaner(filename=constants.CODINGS)
    name = cleaner.clean_name(name)
    cleaner = Cleaner(filename=constants.TORRENT_DATA)
    name = cleaner.clean_name(name)
    name = clean_punctuation(name)
    name = remove_additional_spacing(name).strip()
    name = string.capwords(name, " ")
    return name
