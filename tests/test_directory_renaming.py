import unittest
from unittest import TestCase

from file_tools import Directory


class TestFileFolderCleaning(TestCase):

    def setUp(self) -> None:
        self.test_dir_name: str = "1990 Bob's folder X0R Hc nf -cg cg cc -Hive JYK Juggs Pdtv Megusta mfcorrea Mkv.Com"

    def test_clean_directory_name(self):
        dir_name = Directory(self.test_dir_name)

        expected_clean_name = "Bob's Folder"
        expected_year = 1990
        expected_extension = ''
        expected_str = f"{expected_clean_name} ({expected_year})"

        self.assertEqual(expected_clean_name, dir_name.cleaned_name)
        self.assertEqual(expected_year, dir_name.file_year)
        self.assertEqual(expected_extension, dir_name.extension)
        self.assertEqual(expected_str, dir_name.__str__())


if __name__ == '__main__':
    unittest.main()
