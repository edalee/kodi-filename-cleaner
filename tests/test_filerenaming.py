from unittest import TestCase, mock

from main import make_new_dir_name, make_new_filename
import user_input


class TestEndpoints(TestCase):
    def setUp(self) -> None:
        self.test_file_name: str = "2000 Bobs Homemade Movie HDCAM 1280P 1080 Hevc Psa -Hive JYK Juggs Pdtv Megusta mfcorrea Mkv.Com"
        self.test_dir_name: str = "1990 Bobs Homemade Movie folder HDCAM 1280P 1080 Hevc Psa -Hive JYK Juggs Pdtv Megusta mfcorrea Mkv.Com"

    def test_make_new_dir_name(self):
        result = make_new_dir_name(self.test_dir_name, False)
        expected_result = ("Bobs Homemade Movie Folder (1990)", 1990)
        self.assertEqual(result, expected_result)

    @mock.patch('builtins.input', return_value=1)
    def test_make_new_filename_with_file_year(self, mock_input):
        result = make_new_filename(self.test_file_name, '.mov', 1990)
        expected_result = "Bobs Homemade Movie (2000).mov"
        self.assertEqual(result, expected_result)

    @mock.patch('builtins.input', return_value=2)
    def test_make_new_filename_with_folder_year(self, mock_input):
        result = make_new_filename(self.test_file_name, '.mov', 1990)
        expected_result = "Bobs Homemade Movie (1990).mov"
        self.assertEqual(result, expected_result)

    @mock.patch('builtins.input', return_value=2)
    def test_make_new_filename_with_no_folder_year(self, mock_input):
        result = make_new_filename(self.test_file_name, '.mov')
        expected_result = "Bobs Homemade Movie (2000).mov"
        self.assertEqual(result, expected_result)

