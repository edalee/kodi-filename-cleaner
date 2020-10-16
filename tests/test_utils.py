import unittest

from settings import constants
from utils.name_tools import Cleaner
from utils.utils import split_name, check_int


class TestHelperFunctions(unittest.TestCase):
    def test_split_name(self):
        expected = ["Sam", "and", "Dave"]
        result = split_name("Sam/and/Dave", "/")
        self.assertEqual(expected, result)

    def test_check_int(self):
        int_as_str_result = check_int("1")
        self.assertFalse(int_as_str_result)

        int_result = check_int(1)
        self.assertTrue(int_result)

    def test_txt_file_to_list(self):
        txt_file_reader = Cleaner(constants.DELETE_FILES)
        has_delete_name = txt_file_reader.check_name(
            "Bob's WWW.YIFY - TORRENTS.COM Movie"
        )
        self.assertTrue(has_delete_name)


if __name__ == "__main__":
    unittest.main()
