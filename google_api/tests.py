import unittest
from unittest import mock

from api_calls import create_song_folder

class TestAPICalls(unittest.TestCase):
    def setUp(self):
        pass

    @mock.patch('api_calls.AUTH_DRIVE')
    def test_create_song_folder(self, mocked_drive):
        mocked_drive.files().create.execute().return_value = {"id" : 1}
        folder = create_song_folder('some_folder_name')
        self.assertEqual(folder, 1)
