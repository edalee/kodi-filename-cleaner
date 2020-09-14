#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import re
import shutil
import string
from typing import List, Tuple

from file_tools import extract_year, remove_additional_spacing, clean_name
from tv_and_series import get_series_episode_info
from user_input import choose_year, get_year_input

FILE_TYPES = ['.m4v', '.mpeg', '.mpg', '.mp4', '.mpe', '.avi', '.mkv', '.mxf', '.wmv', '.ogg', '.divx', '.srt', '.sub']
EXT_TO_KEEP = ['.jpg', '.png', '.vob', '.ifo', '.bup', '.sfv', '.rar', '.subs', '.idx', '.iso']
BLACK_LIST = [ 'VIDEO_TS']


def make_new_filename(old_filename: str, ext: str, parent_year: int = None, episodes: bool = False) -> str:
    original_year = None
    year = extract_year(old_filename)

    if parent_year:
        if not year and parent_year > 1900:
            year = parent_year if parent_year else None
        if parent_year != year:
            year, original_year = choose_year(name=old_filename, file_year=year, folder_year=parent_year)

    # clean title before reassigning year
    cleaned_filename = clean_name(old_filename, year, original_year)
    cleaned_filename = string.capwords(cleaned_filename, ' ')

    if episodes:
        show_number, episode_less_filename = get_series_episode_info(cleaned_filename, year, False)
        episode_less_filename = string.capwords(episode_less_filename, ' ')

        if not show_number:
            file_name = f"{episode_less_filename} ({year}){ext}"
        elif not year:
            file_name = f"{episode_less_filename} {show_number}{ext}"
        elif not year and not show_number:
            file_name = f"{episode_less_filename}{ext}"
        else:
            file_name = f"{episode_less_filename} ({year}) {show_number}{ext}"
        return remove_additional_spacing(file_name).strip()
    else:
        if not year:
            file_name = f"{cleaned_filename}{ext}"
        else:
            file_name = f"{cleaned_filename} ({year}){ext}"
        return remove_additional_spacing(file_name).strip()


def make_new_dir_name(old_name, episodes=False) -> Tuple[str, int]:
    print(f"`{old_name}`")
    year = extract_year(old_name)
    cleaned_name = clean_name(old_name, year)
    if not year:
        year = get_year_input(cleaned_name)
    if episodes:
        series, episode_less_dirname = get_series_episode_info(cleaned_name, year, series_search=True)
        if series:
            return remove_additional_spacing(f"{episode_less_dirname} ({year}) {series}"), year
        else:
            if year:
                return remove_additional_spacing(f"{episode_less_dirname} ({year})"), year
            else:
                return remove_additional_spacing(f"{episode_less_dirname}"), 0
    else:
        if year:
            return remove_additional_spacing(f"{cleaned_name} ({year})"), int(year)
        else:
            return remove_additional_spacing(f"{cleaned_name}"), 0


def rename_file(source, destination) -> bool:
    try:
        os.rename(source, destination)
        print(f"Source path renamed to destination path successfully: {destination}")
        return True
    except IsADirectoryError:
        print("Source is a file but destination is a directory.")
        return False
    except NotADirectoryError:
        print("Source is a directory but destination is a file.")
        return False
    except PermissionError:
        print("Operation not permitted.")
        return False
    except OSError as error:
        print(error)
        return False


def back_up_rename(from_dir, to_dir) -> bool:
    try:
        shutil.move(from_dir, to_dir)
        print(f"Source path renamed to destination path successfully: {to_dir}")
        return True
    except IsADirectoryError:
        print("Source is a file but destination is a directory.")
        return False
    except NotADirectoryError:
        print("Source is a directory but destination is a file.")
        return False
    except PermissionError:
        print("Operation not permitted.")
        return False
    except OSError as error:
        print(error)
        return False


def make_subtitle_filename(new_filename: str, file_extension: str) -> str:
    countries = [
        'english', 'eng',
        'swedish', 'swe', 'sv',
        'danish', 'dan', 'dn',
        'french', 'fra', 'fre',
        'norwegian', 'nor', 'no',
    ]
    filename_txt, file_extension = os.path.splitext(new_filename.lower())
    for i in countries:
        empty_lang = filename_txt.replace(i, '', 8)
        cleaned_white_space = remove_additional_spacing(empty_lang)
        add_space_on_year = cleaned_white_space.replace('(', ' (')
        name = remove_additional_spacing(add_space_on_year)
        name = string.capwords(name, ' ')
        if i in new_filename.lower():
            return f"{name} – {i}{file_extension}"
    else:
        return f"{name} – ? {file_extension}"


def rename_files(path: str, year: int, episodes: bool) -> int:
    print(f"Path: {path}")
    count: int = 0
    print(f"Path for files: {path}")
    for root, sub_dirs, file_names in os.walk(path):
        print(f"Subdirectories: {len(sub_dirs)}")

        for filename in file_names:
            if filename[0] == '.' or filename in BLACK_LIST:
                continue

            if 'sample' in filename.lower():
                if filename.lower() == 'sample.mp4':
                    try:
                        os.remove(f"{root}/{filename}")
                    except Exception as e:
                        print(e)
                    continue

                imp = str(input(f'Delete this file (y or n): "{path}/{filename}"?  '))
                if imp.lower() == 'y' or imp.lower() == 'yes':
                    try:
                        os.remove(f"{root}/{filename}")
                    except Exception as e:
                        print(e)
                    continue
                elif imp.lower() == 'n' or imp.lower() == 'no':
                    pass
                else:
                    print("didn't get that")
                    pass

            renamed_state = False
            print(f"File location: {path}")
            print(f"Evaluating renaming of file: {filename}")

            filename_txt, file_extension = os.path.splitext(filename)

            is_rar_sequence = re.search(r'(.*?)((part\[\d+\])?\.r[0-9]+)', file_extension)
            if is_rar_sequence:
                continue

            if file_extension.lower() in FILE_TYPES:
                new_filename = make_new_filename(filename_txt, file_extension, int(year), episodes)
                if file_extension == '.srt' or file_extension == '.sub':
                    new_filename = make_subtitle_filename(new_filename, file_extension)
                if new_filename != filename:
                    renamed_state = rename_file(os.path.join(root, filename), os.path.join(root, new_filename))
                    if not renamed_state:
                        print("Will try backup renaming")
                        renamed_state = back_up_rename(os.path.join(root, filename), os.path.join(root, new_filename))
                print(f"renamed: {renamed_state}")
                count += 1
                continue

            if file_extension.lower() == 'jpg' and filename == 'WWW.YIFY - TORRENTS.COM' or 'WWW.YTS.RE':
                try:
                    os.remove(f"{root}/{filename}")
                except Exception as e:
                    print(e)
                continue

            if file_extension.lower() not in FILE_TYPES and file_extension.lower() not in EXT_TO_KEEP:
                if file_extension == '.txt' or file_extension == '.rtf':
                    try:
                        os.remove(f"{root}/{filename}")
                    except Exception as e:
                        print(e)
                    continue

                imp = str(input(f'Delete this file (y or n): "{path}/{filename}"?  '))
                if 'y' in imp.lower():
                    try:
                        os.remove(f"{root}/{filename}")
                    except Exception as e:
                        print(e)
                elif imp.lower() == 'n' or imp.lower() == 'no':
                    continue
                else:
                    print("didn't get that")
                    continue
    return count


def rename_dirs(path, episodes=False) -> None:
    count: int = 0
    files_renamed: int = 0
    dirs_renamed: int = 0
    path = path if path.endswith('/') else f'{path}/'
    for root, dirs, filenames in os.walk(path):
        print(f"Root: {root}")
        print(f"Dir Total: {len(dirs)}")

        for dir_name in dirs:
            print(f"Evaluating renaming of directory: {dir_name}")
            renamed_state = False
            if dir_name in BLACK_LIST:
                print(f"Blacklisted Dir {dir_name}")
                continue

            new_name, year = make_new_dir_name(dir_name, episodes)
            new_name = new_name.strip()

            if new_name != dir_name:
                try:
                    renamed_state = rename_file(os.path.join(root, dir_name), os.path.join(root, new_name))
                    if not renamed_state:
                        print("Will try backup renaming")
                        renamed_state = back_up_rename(os.path.join(root, dir_name), os.path.join(root, new_name))
                    if renamed_state:
                        dirs_renamed += 1
                except Exception as e:
                    print(e)
                path = f"{root}/{new_name}"
                path = path.replace("//", "/")
            else:
                path = f"{root}/{dir_name}"
                path = path.replace("//", "/")

            print(f"Renamed dir: {renamed_state}")
            print(f"Path for files renaming: {path}")
            renamed_file_count = rename_files(path, BLACK_LIST, year, episodes)
            files_renamed += renamed_file_count

            count += 1
        else:
            folder = root.split('/')[-2]
            print(f"Evaluating Path for renaming: {folder}")
            year = extract_year(folder)
            if not year:
                year = 0
            renamed_file_count = rename_files(root, BLACK_LIST, int(year), episodes)
            files_renamed += renamed_file_count
            print(f"Path for files renaming: {root}")

    print(f"Total folder count: {count}")
    print(f"Total renamed folder count: {dirs_renamed}")
    print(f"Total renamed files count: {files_renamed}")


def parse_args(argv=None) -> Tuple[str, str]:
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group("required named arguments")
    requiredNamed.add_argument(
        "-f",
        "--filepath",
        type=str,
        help="add a file path",
        required=True,
    )
    parser.add_argument("-e", "--episodes", help="Supply episode to get the season and episode tag in the wrong place")
    args = parser.parse_args(argv)
    return args.filepath, args.epidsodes


def main(path: str, is_tv: bool = False) -> None:
    argv: List[str, bool] = [path, is_tv]
    file_path, episodes = parse_args(argv)
    rename_dirs(file_path, episodes)


if __name__ == "__main__":
    my_path: str = "/Volumes/complete/Stage/"
    is_tv_show: bool  = True
    main(my_path, is_tv_show)
