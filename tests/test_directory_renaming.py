from unittest import TestCase

from file_tools import Directory


class TestFileFolderCleaning(TestCase):

    def setUp(self) -> None:
        self.test_dir_name: str = "1990 Bob's folder X0R Hc nf -cg cg cc -Hive JYK Juggs Pdtv Megusta mfcorrea Mkv.Com"

    def test_clean_directory_name(self):
        dir_name = Directory(self.test_dir_name)

        expected_name = "Bob's Folder (1990)"
        expected_year = 1990
        expected_extension = ''

        self.assertEqual(dir_name.cleaned_name, expected_name)
        self.assertEqual(dir_name.file_year, expected_year)
        self.assertEqual(dir_name.extension, expected_extension)
