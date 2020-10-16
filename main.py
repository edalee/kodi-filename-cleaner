#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
from typing import List, Tuple, Optional, Union

import models
from utils.file_actions import FileActions
from utils.user_input import string_to_bool

logger = logging.getLogger(__name__)


def file_action_interface(
        file: Optional[Union[models.Filename, models.SeriesFilename]],
        file_name: str,
        path: str
) -> int:
    if file.is_renamable:
        file.is_updated = FileActions.change_file_name(
            source=os.path.join(path, file_name),
            destination=os.path.join(path, file.__str__())
        )

    if file.is_removable:
        is_directory: bool = False if file.parent_dir else True
        delete = FileActions.ask_user_before_delete(path=path, filename=file_name, is_directory=is_directory)
        logger.error(f"{type(file).__name__}: {file.original_name} deleted attempt = {delete}")
        return 0

    if file.is_updated and file.is_renamable:
        return 1
    elif not file.is_updated and file.is_renamable:
        logger.error(f"{type(file).__name__} was not Updated: {file.original_name}",
                     extra=dict(file_name=file.original_name, new_name=file.__str__()))
        return 0
    else:
        logger.error(f"Won't change {type(file).__name__}: {file.original_name}",
                     extra=dict(file_name=file.original_name))
        return 0


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
    parser.add_argument(
        "-t",
        "--tv_show",
        help="If TV show specify a boolean flag: yes/no, y/n, 1/0",
        type=string_to_bool,
        nargs="?",
        const=True,
        default=False
    )
    args = parser.parse_args(argv)
    return args.filepath, args.tv_show


def rename_files(file_path: str, _is_tv_show: bool) -> Tuple[int, int]:
    run = 0
    file_count = 0
    dir_count = 0
    if _is_tv_show:
        file_path = file_path + 'shows/'
    else:
        file_path = file_path + 'films/'

    for root, sub_dirs, files in os.walk(file_path):
        logger.info(f"Running from Root: {root}")
        logger.info(f"Sub Directories Total: {len(sub_dirs)}")
        logger.info(f"Filename: {len(files)}")

        for name in files:
            if root == file_path:
                logger.warning("Won't rename file name, does not have a parent folder. Please create one.")
                break

            if _is_tv_show:
                file = models.SeriesFilename(name, root)
                file_count += file_action_interface(file=file, file_name=name, path=root)

            else:
                dir = models.Directory(root.split('/')[-1])
                file = models.Filename(name, dir)
                file_count += file_action_interface(file=file, file_name=name, path=root)

            logger.info(f"Filename: {name}")

        for name in sub_dirs:
            logger.info(f"Sub Folder: {name}")
            if _is_tv_show:
                folder = models.SeriesDirectory(name)
                dir_count += file_action_interface(file=folder, file_name=name, path=root)
            else:
                folder = models.Directory(name)
                dir_count += file_action_interface(file=folder, file_name=name, path=root)

    return dir_count, file_count


def test_entry_point() -> None:
    test_path: str = "/Volumes/complete/Stage/"
    test_is_tv_show: bool = False
    argv: List[str, bool] = ['-f', test_path, '-t', test_is_tv_show]
    main(argv)


def main(argv=None) -> None:
    file_path, is_tv_show = parse_args(argv)
    dir_count, file_count = rename_files(file_path, is_tv_show)
    logger.info(f"directories renamed count: {dir_count}")
    logger.info(f"files renamed count: {file_count}")


if __name__ == "__main__":
    test_entry_point()
    # main(sys.argv[1:])
