import os
import google.oauth2.credentials
from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload
# from googleapiclient.errors import HttpError

DRIVE_AUTHORIZED_USER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/credentials.json')
API_KEY = 'AIzaSyBMNx5aAONSIqm3NCFrC_YoEoDT98bwKjE'

try:
    credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(
        DRIVE_AUTHORIZED_USER_FILE,
        scopes = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file ', 'https://www.googleapis.com/auth/drive.appdata'])
except FileNotFoundError:
    print('Credentials not created')
    pass

API_SERVICE_NAME = "drive"
API_VERSION = "v3"

# THESE API CALLS REQUIRE AUTHORIZATION
try:
    AUTH_DRIVE = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
except NameError:
    pass

def upload_pdf_to_drive(score_data, file_location_on_disk):
    file_metadata = score_data
    media = MediaFileUpload(
        file_location_on_disk, mimetype='application/pdf')

    file = AUTH_DRIVE.files().create(
        body=file_metadata,
        media_body=media,
        fields="id,webViewLink,webContentLink,thumbnailLink,hasThumbnail"
        ).execute()
    return file

def upload_audio_to_drive(score_data, file_location_on_disk, mimetype):
    file_metadata = score_data
    media = MediaFileUpload(
        file_location_on_disk, mimetype=mimetype)

    file = AUTH_DRIVE.files().create(
        body=file_metadata,
        media_body=media,
        fields="id,webViewLink,webContentLink,thumbnailLink,hasThumbnail"
        ).execute()
    return file

def share_file_permission(file_id):
    """Set a file as shareable"""
    body = {
        'role' : 'reader',
        'type' : 'anyone',
        }
    permission = AUTH_DRIVE.permissions().create(
        fileId=file_id,
        body=body,
        ).execute()
    return permission


