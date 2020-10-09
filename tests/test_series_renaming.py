import unittest
from typing import List
from unittest import mock

from models import SeriesDirectory, SeriesFilename


class TestSeriesFilenameCleaning(unittest.TestCase):

    def setUp(self) -> None:
        self.test_file_name: str = "2000 Bob's show HDCAM 1280P 1080 Hevc Psa -Hive Pdtv Megusta Mkv.Com S01E02.srt"
        self.test_dir_name: str = "1990 Bob's show folder X0R Hc nf -cg cg cc -Hive JYK Juggs Pdtv Megusta Mkv.Com S01"
        self.test_file_names: List[str] = [
            "2000 Bob's Show HDCAM S01E02 1280P.ssa",
            "2000 fre Bob's Show HDCAM S01E02 1280P.ass",
            "2000 Bob's Show HDCAM S01E02 1280P.usf",
            "2000 Bob's Show nor HDCAM S01E02 1280P.ssf",
            "2000 Bob's Show HDCAM 1280P S01E02 eng.srt",
            "2000 Bob's Show HDCAM 1280P S01E02.sub",
        ]

    @unittest.mock.patch('builtins.input', return_value=1)
    def test_clean_series_filename(self, mock_input):
        directory = SeriesDirectory(self.test_dir_name)
        file_name = SeriesFilename(self.test_file_name, directory)

        expected_cleaned_name = "Bob's Show"
        expected_year = 2000
        expected_extension = ".srt"
        expected_string = "Bob's Show (2000) S01E02.srt"

        self.assertEqual(expected_cleaned_name, file_name.cleaned_name)
        self.assertEqual(expected_year, file_name.file_year)
        self.assertEqual(expected_extension, file_name.extension)
        self.assertEqual(expected_string, file_name.__str__())

    @unittest.mock.patch('builtins.input', return_value=1)
    def test_clean_subtitle_filename(self, mock_input):
        directory = SeriesDirectory(self.test_dir_name)

        expected_strings = [
            "Bob's Show (2000) S01E02 – eng.srt",
            "Bob's Show (2000) S01E02.ssa",
            "Bob's Show (2000) S01E02 – fre.ass",
            "Bob's Show (2000) S01E02.usf",
            "Bob's Show (2000) S01E02 – nor.ssf",
            "Bob's Show (2000) S01E02.srt",
            "Bob's Show (2000) S01E02.sub",
        ]
        for subtitle in self.test_file_names:
            file_name = SeriesFilename(subtitle, directory)
            self.assertIn(file_name.__str__(), expected_strings)


class TestSeriesFolderCleaning(unittest.TestCase):

    def setUp(self) -> None:
        self.test_dir_name: str = "1990 Bob's show folder X0R Hc nf -cg cg cc -Hive JYK Juggs Pdtv Megusta Mkv.Com S01"

    @unittest.mock.patch('builtins.input', return_value=1)
    def test_clean_series_directory_filename(self, mock_input):
        directory = SeriesDirectory(self.test_dir_name)

        expected_cleaned_name = "Bob's Show Folder"
        expected_year = 1990
        expected_extension = ""
        expected_string = "Bob's Show Folder (1990) S01"

        self.assertEqual(expected_cleaned_name, directory.cleaned_name)
        self.assertEqual(expected_year, directory.file_year)
        self.assertEqual(expected_extension, directory.extension)
        self.assertEqual(expected_string, directory.__str__())


if __name__ == '__main__':
    unittest.main()
