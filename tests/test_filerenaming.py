from unittest import TestCase

from main import make_new_dir_name


class TestEndpoints(TestCase):
    def setUp(self) -> None:
        self.test_file_name: str = ""
        self.test_dir_name: str = "1990 Bobs Homemade Movie HDCAM 1280P 1080 Hevc Psa -Hive JYK Juggs Pdtv Megusta mfcorrea Mkv.Com"

    def test_make_new_dir_name(self):
        result = make_new_dir_name(self.test_dir_name, False)
        expected_result = ("Bobs Homemade Movie (1990)", 1990)
        self.assertEqual(result, expected_result)


