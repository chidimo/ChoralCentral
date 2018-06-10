import unittest
from unittest import mock

import api_calls

class TestAPICalls(unittest.TestCase):

    @mock.patch('api_calls.google.oauth2.credentials')
    @mock.patch('api_calls.build')
    @mock.patch('api_calls.DRIVE_AUTHORIZED_USER_FILE')
    @mock.patch('api_calls.DRIVE_SCOPES')
    def test_drive_service_creation(self, mocked_scopes, mocked_file, mocked_build, mocked_drive_cred):
        api_calls.construct_drive_service()
        credentials = mocked_drive_cred.Credentials.from_authorized_user_file
        credentials.assert_called_with(mocked_file, scopes=mocked_scopes)
        mocked_build.assert_called_with('drive', 'v3', credentials=credentials(), cache_discovery=False)

    @mock.patch('api_calls.construct_drive_service')
    @mock.patch('api_calls.choice')
    def test_create_song_folder(self, mocked_choice, mocked_drive_service):
        mocked_choice.return_value = "#8f8f8f"
        metadata = {
            'name': 'some_folder_name',
            'mimeType': 'application/vnd.google-apps.folder',
            'folderColorRgb' : "#8f8f8f",
        }
        api_calls.create_song_folder('some_folder_name')
        request = mocked_drive_service().files().create
        request.assert_called_with(body=metadata, fields="id")
        request().execute.assert_called_with()

if __name__ == "__main__":
    unittest.main()
