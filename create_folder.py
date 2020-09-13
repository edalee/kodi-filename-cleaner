#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os

my_path = '/Volumes/archived/Films/1970- Two Mules for Sister Sara.mp4'


def parse_args():
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group("required named arguments")
    requiredNamed.add_argument(
        "-f",
        "--filepath",
        type=str,
        nargs="+",
        help="add path",
        required=True,
    )
    args = parser.parse_args()

    return args.filepath


def create_new_folder(path):
    drive, file_name = os.path.split(path)
    ext = os.path.splitext(path)[1]

    new_name = file_name.replace(ext, '')
    new_name = new_name.replace("\'", "'")
    new_path = os.path.join(drive, new_name)
    try:
        os.mkdir(new_path)
    except Exception as e:
        print(e)
    print(f"Directory '{new_path}' created")
    moving_path = os.path.join(new_path, file_name)
    try:
        os.rename(path, moving_path)
    except Exception as e:
        print(e)
    try:
        moved_file = os.path.exists(moving_path)
    except Exception as e:
        print(e)
    print(f"File moved to new folder {moved_file}")
    return moved_file


def main():
    paths = parse_args()
    total_created: int = 0
    for path in paths:
        print(f"total: {len(paths)}")
        created = create_new_folder(path)
        if created:
            total_created += 1
    print(f"Total Created: {total_created}")


if __name__ == '__main__':
    main()
