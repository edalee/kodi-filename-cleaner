#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import shutil
from typing import Union

from utils.user_input import check_delete_file

logger = logging.getLogger(__name__)


class FileActions:

    renamed: bool = False

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
            cls.renamed_state = cls.rename_file(source, destination)
        except Exception as err:
            logger.warning("Failed rename attempt, will try again", extra=dict(error=err))
            try:
                cls.renamed_state = cls.back_up_rename(source, destination)
                logger.info(f"Renamed file: {destination} ", extra=dict(renamed_state=renamed_state))
            except Exception as err:
                logger.error("Failed rename attempt 2, will not retry", extra=dict(error=err))
                cls.renamed_state = False
        return cls.renamed_state

    @staticmethod
    def delete_file(path: Union[str, bytes, os.PathLike]) -> bool:
        logger.info(f"Deleting file: {path} ", extra=dict(file_name=path))
        try:
            os.remove(path)
            logger.info(f"Removed file: {path} ", extra=dict(file_name=path))
            return True
        except Exception as err:
            logger.error(f"Failed to delete file: {path} ", extra=dict(file_name=path))
            return False

    @staticmethod
    def delete_directory(path: Union[str, bytes, os.PathLike]) -> bool:
        logger.info(f"Deleting folder: {path} ", extra=dict(file_name=path))
        try:
            os.rmdir(path)
            logger.info(f"Removed file: {path} ", extra=dict(file_name=path))
            return True
        except Exception as err:
            logger.error(f"Failed to delete folder: {path} ", extra=dict(file_name=path))
            return False

    @classmethod
    def ask_user_before_delete(
            cls,
            path: Union[str, bytes, os.PathLike],
            filename: str,
            is_directory: bool = False
    ) -> bool:
        if is_directory:
            if check_delete_file(path.__str__(), filename):
                return cls.delete_directory(path=os.path.join(path, filename))
            else:
                logger.info("Skipped file deletion", extra=dict(file_name=filename))
                return False
        else:
            if check_delete_file(path.__str__(), filename):
                return cls.delete_file(path=os.path.join(path, filename))
            else:
                logger.info("Skipped file deletion", extra=dict(file_name=filename))
                return False
