from typing import List
from unittest import TestCase, mock

from file_tools import Directory, Filename


class TestFileFolderCleaning(TestCase):

    def setUp(self) -> None:
        self.test_file_name: str = "2000 Bob's Movie HDCAM 1280P 1080 Hevc Psa -Hive Pdtv Megusta Mkv.Com.mov"
        self.test_dir_name: str = "1990 Bob's folder X0R Hc nf -cg cg cc -Hive JYK Juggs Pdtv Megusta mfcorrea Mkv.Com"

    def test_clean_directory_name(self):
        dir_name = Directory(self.test_dir_name)

        expected_name = "Bob's Folder (1990)"
        expected_year = 1990
        expected_extension = ''

        self.assertEqual(dir_name.cleaned_name, expected_name)
        self.assertEqual(dir_name.file_year, expected_year)
        self.assertEqual(dir_name.extension, expected_extension)

    @mock.patch('builtins.input', return_value=1)
    def test_clean_filename_with_file_year(self, mock_input):
        dir_name = Directory(self.test_dir_name)
        file_name = Filename(self.test_file_name, dir_name)

        expected_name = "Bob's Movie (2000).mov"
        expected_year = 2000
        expected_extension = ".mov"

        self.assertEqual(expected_name, file_name.cleaned_name)
        self.assertEqual(expected_year, file_name.file_year)
        self.assertEqual(expected_extension, file_name.extension)

    @mock.patch('builtins.input', return_value=2)
    def test_clean_filename_with_directory_year(self, mock_input):
        dir_name = Directory(self.test_dir_name)
        file_name = Filename(self.test_file_name, dir_name)

        expected_name = "Bob's Movie (1990).mov"
        expected_year = 2000
        expected_extension = ".mov"

        self.assertEqual(expected_name, file_name.cleaned_name)
        self.assertEqual(expected_year, file_name.file_year)
        self.assertEqual(expected_extension, file_name.extension)

    @mock.patch('builtins.input', return_value=1992)
    def test_clean_filename_with_no_folder_year(self, mock_input):
        dir_name = Directory("Bob's Folder ()")
        file_name = Filename(self.test_file_name, dir_name)

        expected_folder_name = "Bob's Folder (1992).mov"
        expected_folder_year = None
        expected_folder_extension = ""

        expected_file_name = "Bob's Movie (2000).mov"
        expected_file_year = 2000
        expected_file_extension = ".mov"

        self.assertEqual(expected_file_name, file_name.cleaned_name)
        self.assertEqual(expected_file_year, file_name.file_year)
        self.assertEqual(expected_file_extension, file_name.extension)

        self.assertEqual(expected_folder_name, dir_name.cleaned_name)
        self.assertEqual(expected_folder_year, dir_name.file_year)
        self.assertEqual(expected_folder_extension, dir_name.extension)


class TestFileState(TestCase):

    def setUp(self) -> None:
        self.test_sub_file: str = "Logans Run (fra).sub"
        self.test_srt_file: str = "Logans Run (eng).srt"
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
        dir_name = Directory("Bob's Folder ()")

        for filename in self.not_allowed_files:
            file = Filename(filename, dir_name)
            self.assertTrue(file.is_junk)

    @mock.patch('builtins.input', return_value=0)
    def test_should_rename_files(self, mock_input):
        dir_name = Directory(self.dvd_folder)
        self.assertFalse(dir_name.should_rename)

        for rar in self.rars:
            rar_file = Filename(rar, dir_name)
            self.assertFalse(rar_file.should_rename)
