#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import shutil
from typing import Union

from utils.user_input import check_delete_file

logger = logging.getLogger(__name__)


class FileActions:

    @staticmethod
    def rename_file(source: Union[str, bytes, os.PathLike], destination: Union[str, bytes, os.PathLike]) -> bool:
        try:
            os.rename(source, destination)
            logger.info(f"Source path renamed to destination path successfully: {destination}")
            return True
        except IsADirectoryError:
            logger.warning("Source is a file but destination is a directory.")
            raise
        except NotADirectoryError:
            logger.warning("Source is a directory but destination is a file.")
            raise
        except PermissionError:
            logger.warning("Operation not permitted.")
            raise
        except OSError as error:
            logger.warning(error)
            raise

    @staticmethod
    def back_up_rename(source: Union[str, bytes, os.PathLike], destination: Union[str, bytes, os.PathLike]) -> bool:
        try:
            shutil.move(source, destination)
            logger.info(f"Source path renamed to destination path successfully: {destination}")
            return True
        except IsADirectoryError:
            logger.warning("Source is a file but destination is a directory.")
            raise
        except NotADirectoryError:
            logger.warning("Source is a directory but destination is a file.")
            raise
        except PermissionError:
            logger.warning("Operation not permitted.")
            raise
        except OSError as error:
            logger.warning(error)
            raise

    @classmethod
    def change_file_name(cls, source: Union[str, bytes, os.PathLike],
                         destination: Union[str, bytes, os.PathLike]) -> bool:

        try:
            renamed_state = cls.rename_file(source, destination)
        except Exception as err:
            logger.warning("Failed rename attempt, will try again", extra=dict(error=err))
            try:
                renamed_state = cls.back_up_rename(source, destination)
            except Exception as err:
                logger.error("Failed rename attempt 2, will not retry", extra=dict(error=err))
        return renamed_state or False

    @staticmethod
    def delete_file(path: Union[str, bytes, os.PathLike]) -> None:
        logger.info(f"Deleting file: {path} ", extra=dict(file_name=path))
        try:
            os.remove(path)
        except Exception as err:
            logger.error(f"Failed to delete file: {path} ", extra=dict(file_name=path))

    @classmethod
    def ask_user_before_delete(cls, directory: Union[str, bytes, os.PathLike], filename: str):
        if check_delete_file(directory.__str__(), filename):
            cls.delete_file(path=os.path.join(directory, filename))
        else:
            logger.info("Skipped file deletion", extra=dict(file_name=filename))
