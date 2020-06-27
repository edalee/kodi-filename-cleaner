#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os
import re
import shutil
from typing import List


class UnsplittableError(Exception):
    pass


def remove_additional_spacing(name):
    return re.sub(' +', ' ', name)


def extract_year(title):
    avoid_list = ['480', '720', '1080']
    for i in avoid_list:
        new_title = title.replace(i, '')
    match = re.match(r'.*([1-3][0-9]{3})', new_title)
    if match is not None:
        # Then it found a match!
        return match.group(1)


def clean_name(name: str, year: int) -> str:
    torrent_names = [
        'anoXmous',
        'Afg',
        '-AMIABLE',
        'BOGiEman',
        'bm11',
        '-cg',
        '-CG',
        'cg',
        'cc',
        'C4Tv',
        'cinefile',
        'CM8',
        'Criterion',
        'Ctbx',
        'CriterionBluRay',
        'ehhhh',
        'ETRG',
        "Ettv",
        'EVO',
        'ExtraTorrent',
        'Gspot',
        'FH-loyal-ity',
        'Hammer71',
        'Hevc',
        'Hevc Psa',
        '-Hive',
        'JYK',
        'Juggs',
        'mfcorrea',
        '-muxed',
        'mrn',
        'nesmeured',
        'nf',
        '(None)',
        'Ozlem',
        'organic()',
        "PSYPHER",
        'Remastered',
        'RARBG',
        'Repack',
        'SiRiUs sHaRe',
        'Schizo',
        'Sujaidr',
        'Sticky83'
        'tahi',
        'TiTAN',
        'Uk Organic()',
        '-UNRATED',
        '-usury',
        "WAZZ",
        'WRD',
        "Vip3R",
        'X0R',
        'YIFY',
        'Y83',
        "2hd",
    ]
    codings = [
        '2ch',
        '4ch',
        '6ch',
        '8ch',
        '480p',
        '720p',
        '1080p',
        '480',
        '570',
        '720',
        '1080',
        'AAC',
        'AC3',
        'AVC',
        'BluRay',
        'Blueray',
        'bdrip',
        'BRRip',
        'DC',
        'UNRATED',
        'DD5.1',
        'DVDScr',
        'DVDRip',
        'Hdtv',
        'H264',
        'HDB',
        'HDRip',
        'HQ',
        'Mb',
        'MP3',
        'Mp3',
        'MVGroup.org',
        ' P ',
        'Tvrip',
        'WEB-DL',
        "Webrip",
        'x264',
        'X265',
        'XVID',
    ]
    name = name.replace(str(year), '')
    name = name.replace('()', '')
    name = name.replace('[]', '')
    name = name.replace('( )', '')
    name = name.replace('[', '(').replace(']', ')')
    for i in codings:
        name = name.lower().replace(i.lower(), '')
    for i in torrent_names:
        name = name.lower().replace(i.lower(), '')
    name = name.replace('.', ' ').replace('_', ' ').replace('–', ' ').replace('-', ' ')
    name = remove_additional_spacing(name).strip().title()
    return name


def split_name(name: str, character: str) -> List:
    if character in name:
        return name.split(character)
    else:
        raise UnsplittableError


def check_int(year):
    return isinstance(year, int)


def find_series_and_episode(findings: List) -> str:
    check = 's'
    check_two = 'e'
    result_1 = [idx for idx in findings if idx[0].lower() == check.lower()]
    result_2 = [idx for idx in findings if idx[0].lower() == check_two.lower()]
    if len(result_1[0]) == 3 and len(result_2[0]) == 3:
        return "".join(findings).lower()
    elif len(result_1[0]) == 2 and len(result_2[0]) == 2:
        return result_1[0].replace('s', 's0')+result_2[0].replace('e', 'e0')
    else:
        return


def find_series(findings: List) -> str:
    check = 's'
    result_1 = [idx for idx in findings if idx[0].lower() == check.lower()]
    if len(result_1[0]) == 3:
        return "".join(findings).lower()
    elif len(result_1[0]) == 2:
        return result_1[0].replace('s', 's0')
    else:
        return


def get_series_info(cleaned_filename):
    ses = re.findall("[a-zA-Z]\d{2}", cleaned_filename.lower())
    if not ses:
        ses = re.findall("[a-zA-Z]\d{1}", cleaned_filename.lower())
    series = find_series(ses)
    if not series:
        series = get_show_input(cleaned_filename)
    removed_episode = cleaned_filename.lower().replace(series, '')
    title_cased_name = remove_additional_spacing(removed_episode.title())
    return series.upper(), title_cased_name


def get_episode_info(cleaned_filename):
    ses = re.findall("[a-zA-Z]\d{2}", cleaned_filename.lower())
    if not ses:
        ses = re.findall("[a-zA-Z]\d{1}", cleaned_filename.lower())
    series_episode = find_series_and_episode(ses)
    if not series_episode:
        series_episode = get_show_input(cleaned_filename)
    removed_episode = cleaned_filename.lower().replace(series_episode, '')
    title_cased_name = remove_additional_spacing(removed_episode.title())
    return series_episode.upper(), title_cased_name


def make_new_filename(old_filename: str, ext: str, _year: int, episodes: bool = False) -> str:
    year = extract_year(old_filename)
    if not year:
        year = _year
    cleaned_filename = clean_name(old_filename, year)

    if episodes:
        show_number, episode_less_filename = get_episode_info(cleaned_filename)
        file_name = f"{episode_less_filename.title()} ({year}) {show_number}{ext}"
        return remove_additional_spacing(file_name).strip()
    else:
        file_name = f"{cleaned_filename.title()} ({year}){ext}"
        return remove_additional_spacing(file_name).strip()


def get_year_input(name) -> int:
    while True:
        try:
            year = int(input(f'Add season year: "{name}"?  '))
            return year
        except ValueError:
            print("The input was not a valid integer")


def get_show_input(name) -> str:
    while True:
        try:
            episode = str(input(f'Add season and episode (like this S01E02: "{name}"?  '))
            if episode.upper().startswith('S') and episode.upper()[3] == 'E':
                return episode
        except ValueError:
            print("The input was not a valid integer")


def make_new_dir_name(old_name, episodes=False) -> tuple:
    print(f"`{old_name}`")
    year = extract_year(old_name)
    cleaned_name = clean_name(old_name, year)
    if not year:
        year = get_year_input(cleaned_name)
    if episodes:
        series, episode_less_dirname = get_series_info(cleaned_name)
        return remove_additional_spacing(f"{episode_less_dirname} ({year}) {series}"), year
    else:
        return remove_additional_spacing(f"{cleaned_name} ({year})"), year


def rename_file(source, dest) -> bool:
    try:
        os.rename(source, dest)
        print(f"Source path renamed to destination path successfully: {dest}")
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


def back_up_rename(from_dir, to_dir):
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


def make_subtitle_filename(new_filename, file_extension):
    countries = [
        'english', 'eng',
        'swedish', 'swe', 'sv',
        'danish', 'dan',
        'french', 'fra', 'fre',
        'spanish', 'spa', 'esp',
        'dutch', 'dut',
        'italian', 'ita',
    ]
    filename_txt, file_extension = os.path.splitext(new_filename.lower())
    for i in countries:
        empty_lang = filename_txt.replace(i, '', 8)
        cleaned_white_space = remove_additional_spacing(empty_lang)
        add_space_on_year = cleaned_white_space.replace('(', ' (')
        name = remove_additional_spacing(add_space_on_year)
        if i in new_filename.lower():
            return f"{name.title()} – {i}{file_extension}"
    else:
        return f"{name.title()} – eng{file_extension}"


def rename_dir_files(path: str, blacklist: List, year: int, episodes: bool) -> int:
    file_types = ['.m4v', '.mpeg', '.mpg', '.mp4', '.mpe', '.avi', '.mkv', '.mxf', '.wmv', '.ogg', '.divx', '.nfo',
                  '.srt', '.sub', ]
    ext_to_keep = ['.jpg', '.png', '.vob', '.ifo', '.bup', '.sfv', '.rar', '.subs', '.idx']
    print(f"Path: {path}")
    count: int = 0
    print(f"Path for files: {path}")
    for root, sub_dirs, file_names in os.walk(path):
        print(f"Subdirectories: {len(sub_dirs)}")

        for filename in file_names:
            renamed_state = False
            print(f"File location: {path}")
            print(f"Evaluating renaming of file: {filename}")

            if filename[0] == '.':
                continue

            if filename in blacklist:
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

            filename_txt, file_extension = os.path.splitext(filename)

            is_rar_sequence = re.search(r'(.*?)((part\[\d+\])?\.r[0-9]+)', file_extension)
            if is_rar_sequence:
                continue

            if file_extension.lower() in file_types:
                new_filename = make_new_filename(filename_txt, file_extension, year, episodes)
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

            if file_extension.lower() not in file_types and file_extension.lower() not in ext_to_keep:
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
    black_list = [
        'Godzilla Complete Boxset (1954)–(2004)',
        'James Stewart Pack',
        'VIDEO_TS',
        'Zatoichi Collection (1962-1989)',
    ]
    count:int = 0
    files_renamed: int = 0
    dirs_renamed: int = 0
    path = path if path.endswith('/') else f'{path}/'
    for root, dirs, filenames in os.walk(path):
        print(f"Root: {root}")
        print(f"Dir Total: {len(dirs)}")

        for dir_name in dirs:
            print(f"Evaluating renaming of directory: {dir_name}")
            renamed_state = False
            if dir_name in black_list:
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
            renamed_file_count = rename_dir_files(path, black_list, year, episodes)
            files_renamed += renamed_file_count

            count += 1
        else:
            folder = root.split('/')[-2]
            year = extract_year(folder)
            renamed_file_count = rename_dir_files(root, black_list, year, episodes)
            files_renamed += renamed_file_count
            print(f"Path for files renaming: {root}")

    print(f"Total folder count: {count}")
    print(f"Total renamed folder count: {dirs_renamed}")
    print(f"Total renamed files count: {files_renamed}")


def parse_args():
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
    args = parser.parse_args()
    return args.filepath, args.epidsodes


def main():
    file_path, episodes = parse_args()
    rename_dirs(file_path, episodes)


if __name__ == "__main__":
    # main()
    # my_path = '/Volumes/archived/TV/'
    my_path = '/Volumes/Tv/'
    rename_dirs(my_path, True)
