from typing import List
from unittest import TestCase, mock

from file_tools import Directory, Filename


class TestFileState(TestCase):

    def setUp(self) -> None:
        self.not_allowed_files: List[str] = [
            "john smith.txt",
            "john smith.rtf"
            "WWW.YTS.RE.jpg",
            "sample.mp4",
            ".sum_hidden_file.config",
        ]
        self.rars: List[str] = ["test.r00", "test.r01", "test.r02"]
        self.dvd_folder = "VIDEO_TS"

    @mock.patch('builtins.input', return_value=1983)
    def test_junk_files(self, mock_input):
        directory = Directory("Bob's Folder ()")

        for filename in self.not_allowed_files:
            file = Filename(filename, directory)
            self.assertTrue(file.is_junk)

    @mock.patch('builtins.input', return_value=0)
    def test_should_rename_files(self, mock_input):
        directory = Directory(self.dvd_folder)
        self.assertFalse(directory.should_rename)

        for rar in self.rars:
            rar_file = Filename(rar, directory)
            self.assertFalse(rar_file.should_rename)
