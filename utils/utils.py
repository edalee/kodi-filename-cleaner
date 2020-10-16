#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from os import PathLike
from typing import List, Union, Any


class UnsplittableError(Exception):
    pass


def split_name(name: str, character: str) -> List:
    if character in name:
        return name.split(character)
    else:
        raise UnsplittableError


def check_int(year) -> bool:
    return isinstance(year, int)


def read_file_json(file_path: Union[str, bytes, PathLike]) -> Any:
    with open(file_path) as f:
        return json.load(f)
