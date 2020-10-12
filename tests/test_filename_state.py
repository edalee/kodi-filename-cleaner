import unittest
from typing import List
from unittest import mock

from models import Directory, Filename


class TestFileState(unittest.TestCase):

    def setUp(self) -> None:
        self.not_allowed_files: List[str] = [
            "john smith.txt",
            "john smith.rtf"
            "WWW.YTS.RE.jpg",
            "sample.mp4",
            ".sum_hidden_file.config",
        ]
        self.rars: List[str] = ["test.r00", "test.r01", "test.r02"]

        self.dvd_folder: str = "VIDEO_TS"

    @unittest.mock.patch('builtins.input', return_value=1983)
    def test_removable_file(self, mock_input):
        directory = Directory("Bob's Folder ()")

        for filename in self.not_allowed_files:
            file = Filename(filename, directory)
            self.assertTrue(file.is_removable)

    @unittest.mock.patch('builtins.input', return_value=0)
    def test_should_rename_files(self, mock_input):
        directory = Directory("Bob's Folder ()")

        for rar in self.rars:
            rar_file = Filename(rar, directory)
            self.assertFalse(rar_file.should_rename)

    @unittest.mock.patch('builtins.input', return_value=0)
    def test_should_not_rename_file(self, mock_input):
        directory = Directory("Bob's Folder (1980)")
        file = Filename("Bob's Film (1980).avi", directory)

        self.assertFalse(file.should_rename)


class TestFolderState(unittest.TestCase):

    def setUp(self) -> None:
        self.not_allowed_folders: List[str] = [
            ".DS_folder",
            ".cache"
            "extras",
            "EXTRAS",
        ]
        self.dvd_folder = "VIDEO_TS"

    @unittest.mock.patch('builtins.input', return_value=0)
    def test_remove_files(self, mock_input):
        for folder in self.not_allowed_folders:
            folder_name = Directory(folder)
            self.assertTrue(folder_name.is_removable)

    @unittest.mock.patch('builtins.input', return_value=0)
    def test_should_rename_folder(self, mock_input):
        directory = Directory(self.dvd_folder)
        self.assertFalse(directory.should_rename)

    @unittest.mock.patch('builtins.input', return_value=0)
    def test_should_not_rename_folder(self, mock_input):
        directory = Directory("Bob's Folder (1980)")

        self.assertFalse(directory.should_rename)