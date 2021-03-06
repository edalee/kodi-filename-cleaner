#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


def get_year_input(name: str) -> Optional[int]:
    while True:
        try:
            year = int(input(f'Add film/series year "{name}" (0 to skip) : '))
            if year <= 1880:
                pass
            if year > 1880:
                return year
            if year == 0:
                return None
            else:
                raise ValueError
        except ValueError:
            print("The input was not a valid integer")
        except Exception as err:
            logger.error("Failed year input", extra=dict(error=err))
            raise


def choose_year(name: str, file_year: int, folder_year: int) -> Optional[int]:
    while True:
        try:
            choice = int(
                input(
                    f'Choose year: File (1) = "{file_year}",'
                    f' Folder (2) = "{folder_year}" OR (3) add my own : '
                )
            )
            if choice == 1:
                year: Optional[int] = file_year
            elif choice == 2:
                year = folder_year
            elif choice == 3:
                year = get_year_input(name)
            else:
                raise ValueError
            return year
        except ValueError:
            print("The input was not a valid integer")
        except Exception as err:
            logger.error("Failed choose year input", extra=dict(error=err))
            raise


def check_delete_file(directory: str, filename: str) -> bool:
    yes_answers = ["yes", "y", "yeah", "yep"]
    no_answers = ["no", "n", "na", "non", "nope"]
    while True:
        response = str(
            input(f'Delete this file (y or n): "{directory}/{filename}"?  ')
        ).strip()
        if response.lower() in yes_answers:
            return True
        elif response.lower() in no_answers:
            return False
        else:
            print("sorry didn't get that")


def get_show_input(name: str, series: bool = False) -> List[str]:
    while True:
        try:
            if series:
                _input = str(
                    input(
                        f'Add series and episode "{name}" (eg: S01E02) or c to skip : '
                    )
                )
            else:
                _input = str(
                    input(f'Add series (eg: S01, for "{name}" or c to skip : ')
                )

            if (
                len(_input) == 3
                and _input.lower().startswith("s")
                or len(_input) == 6
                and _input.upper().startswith("S")
                and _input.upper()[3] == "E"
            ):
                return [_input.upper()]

            if _input.lower() == "c":
                return [""]
        except ValueError:
            print("The input was not a valid series and episode")
        except Exception as err:
            logger.error("Failed show input", extra=dict(error=err))
            raise


def string_to_bool(_value) -> bool:
    if isinstance(_value, bool):
        return _value
    if _value.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif _value.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")
