import unittest
from typing import List
from unittest import TestCase, mock

from constants import LANGUAGES_JSON
from file_tools import Directory, Filename, get_languages


class TestFileFolderCleaning(TestCase):
    @staticmethod
    def build_subtitle_test_list() -> List[str]:
        languages = get_languages(LANGUAGES_JSON)
        # flatten = lambda l: [item for sublist in l for item in sublist.values()]
        # return flatten(languages)
        return [item for sublist in languages for item in sublist.values()]

    def setUp(self) -> None:
        self.test_file_name: str = "2000 Bob's Movie HDCAM 1280P 1080 Hevc Psa -Hive Pdtv Megusta Mkv.Com.mov"
        self.test_dir_name: str = "1990 Bob's folder X0R Hc nf -cg cg cc -Hive JYK Juggs Pdtv Megusta mfcorrea Mkv.Com"
        self.test_subtitle_file_ext: List[str] = [
            "Logans Run (1980)(eng).sub",
            'Logans Run (1980)(eng).srt',
            "Logans Run (1980)(eng).ssa",
            "Logans Run (1980)(nor).ass",
            "Logans Run (1980)(vie).ass",
            "Logans Run (1980)(zha).usf",
            "Logans Run (1980)(Yoruba).ssf",
            "Logans Run 1980 – fra.sub",
            "Logans Run (1980)(xh).sub",
        ]
        self.test_non_sub_file: str = "Logans Run.txt"
        self.test_dirty_sub_file: str = "Logan's Run Afg Btn CM8 EVO Fgt Fum Ftp  Fov- nor.sub"

    @mock.patch('builtins.input', return_value=1)
    def test_clean_filename_with_file_year(self, mock_input):
        directory = Directory(self.test_dir_name)
        file_name = Filename(self.test_file_name, directory)

        expected_cleaned_name = "Bob's Movie"
        expected_year = 2000
        expected_extension = ".mov"
        expected_string = "Bob's Movie (2000).mov"

        self.assertEqual(expected_cleaned_name, file_name.cleaned_name)
        self.assertEqual(expected_year, file_name.file_year)
        self.assertEqual(expected_extension, file_name.extension)
        self.assertEqual(expected_string, file_name.__str__())

    @mock.patch('builtins.input', return_value=2)
    def test_clean_filename_with_directory_year(self, mock_input):
        directory = Directory(self.test_dir_name)
        file_name = Filename(self.test_file_name, directory)

        expected_cleaned_name = "Bob's Movie"
        expected_year = 2000
        expected_extension = ".mov"
        expected_set_year = 1990
        expected_string = "Bob's Movie (1990).mov"

        self.assertEqual(1990, directory.file_year)
        self.assertEqual(expected_cleaned_name, file_name.cleaned_name)
        self.assertEqual(expected_year, file_name.file_year)
        self.assertEqual(expected_set_year, file_name.defined_year)
        self.assertEqual(expected_extension, file_name.extension)
        self.assertEqual(expected_string, file_name.__str__())

    @mock.patch('builtins.input', return_value=1992)
    def test_clean_filename_with_no_folder_year(self, mock_input):
        directory = Directory("Bob's Folder ()")
        file_name = Filename(self.test_file_name, directory)

        expected_folder_cleaned_name = "Bob's Folder"
        expected_folder_year = None
        expected_folder_extension = ""
        expected_folder_set_year = 1992
        expected_folder_string = "Bob's Folder (1992)"

        expected_file_cleaned_name = "Bob's Movie"
        expected_file_year = 2000
        expected_file_extension = ".mov"
        expected_file_set_year = 2000
        expected_file_string = "Bob's Movie (2000).mov"

        self.assertEqual(expected_folder_cleaned_name, directory.cleaned_name)
        self.assertEqual(expected_folder_year, directory.file_year)
        self.assertEqual(expected_folder_extension, directory.extension)
        self.assertEqual(expected_folder_set_year, directory.defined_year)
        self.assertEqual(expected_folder_string, directory.__str__())

        self.assertEqual(expected_file_cleaned_name, file_name.cleaned_name)
        self.assertEqual(expected_file_year, file_name.file_year)
        self.assertEqual(expected_file_extension, file_name.extension)
        self.assertEqual(expected_file_set_year, file_name.defined_year)
        self.assertEqual(expected_file_string, file_name.__str__())

    @mock.patch('builtins.input', return_value=1992)
    def test_clean_filename_with_no_folder_or_file_year(self, mock_input):
        directory = Directory("Bob's Folder")
        file_name = Filename("Bob's Movie.mov", directory)

        expected_folder_cleaned_name = "Bob's Folder"
        expected_folder_year = None
        expected_folder_extension = ""
        expected_folder_set_year = 1992
        expected_folder_string = "Bob's Folder (1992)"

        expected_file_cleaned_name = "Bob's Movie"
        expected_file_year = None
        expected_file_extension = ".mov"
        expected_file_set_year = 1992
        expected_file_string = "Bob's Movie (1992).mov"

        self.assertEqual(expected_folder_cleaned_name, directory.cleaned_name)
        self.assertEqual(expected_folder_year, directory.file_year)
        self.assertEqual(expected_folder_extension, directory.extension)
        self.assertEqual(expected_folder_set_year, directory.defined_year)
        self.assertEqual(expected_folder_string, directory.__str__())

        self.assertEqual(expected_file_cleaned_name, file_name.cleaned_name)
        self.assertEqual(expected_file_year, file_name.file_year)
        self.assertEqual(expected_file_extension, file_name.extension)
        self.assertEqual(expected_file_set_year, file_name.defined_year)
        self.assertEqual(expected_file_string, file_name.__str__())

    @mock.patch('builtins.input', return_value=1)
    def test_subtitle_rename_files(self, mocked_choose_year):
        directory = Directory("Logan's Run - 1980")

        for subtitle_file in self.test_subtitle_file_ext:
            sub_file_name = Filename(subtitle_file, directory)
            self.assertTrue(sub_file_name.subtitle_filename)

        double_check_file_data = Filename(self.test_subtitle_file_ext[0], directory)
        self.assertEqual('Logans Run (1980) – eng.sub', double_check_file_data.subtitle_filename)

        for country_id in self.build_subtitle_test_list():
            country_file = f"logan Run 2018 - {country_id}.srt"
            sub_file_name = Filename(country_file, directory)
            self.assertTrue(sub_file_name.subtitle_filename)

        non_subtitle_file = Filename(self.test_non_sub_file, directory)
        self.assertFalse(non_subtitle_file.subtitle_filename)

        clean_subtitle_name = Filename(self.test_dirty_sub_file, directory)
        self.assertEqual("Logan's Run (1980) – nor.sub", clean_subtitle_name.subtitle_filename)


if __name__ == '__main__':
    unittest.main()
