#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import Optional


def get_show_input(name: str) -> Optional[str]:
    while True:
        try:
            episode = str(input(f'Add series and episode "{name}" (eg: S01E02) or c to skip : '))
            if episode.upper().startswith('S') and episode.upper()[3] == 'E':
                return episode.upper()
            if episode.lower() == 'c':
                return None
        except ValueError:
            print("The input was not a valid series and episode")


def get_year_input(name: str) -> Optional[int]:
    while True:
        try:
            year = int(input(f'Add series year "{name}" (0 to skip) : '))
            if year > 1880:
                return year
            if year == 0:
                return None
            else:
                raise ValueError
        except ValueError:
            print("The input was not a valid integer")


def choose_year(name: str, file_year: str, folder_year: str) -> Optional[int]:
    while True:
        try:
            choice = int(input(f'Choose year 1:"{file_year}", 2:"{folder_year}" OR 3: add my own : '))
            if choice == 1:
                year = file_year
            elif choice == 2:
                year = folder_year
            elif choice == 3:
                year = get_year_input(name)
            else:
                raise ValueError
            return int(year)
        except ValueError:
            print("The input was not a valid integer")