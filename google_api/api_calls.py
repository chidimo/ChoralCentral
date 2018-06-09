# https://support.google.com/cloud/answer/7454865
import os
from random import choice
import google.oauth2.credentials
from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload
# from googleapiclient.errors import HttpError

DRIVE_FOLDER_COLORS = [
    "#ac725e", "#d06b64", "#f83a22", "#fa573c", "#ff7537", "#ffad46", "#fad165",
    "#fbe983", "#b3dc6c", "#7bd148", "#16a765", "#42d692", "#92e1c0", "#9fe1e7",
    "#9fc6e7", "#4986e7", "#9a9cff", "#b99aff", "#a47ae2", "#cd74e6", "#f691b2",
    "#cca6ac", "#cabdbf", "#8f8f8f"]

DRIVE_API_KEY = 'AIzaSyBMNx5aAONSIqm3NCFrC_YoEoDT98bwKjE'
DRIVE_API_VERSION = "v3"
DRIVE_API_SERVICE_NAME = "drive"
DRIVE_AUTHORIZED_USER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/drive_credentials.json')

YOUTUBE_API_KEY = 'AIzaSyBMNx5aAONSIqm3NCFrC_YoEoDT98bwKjE'
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_AUTHORIZED_USER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/youtube_credentials.json')
API_ONLY_YOUTUBE = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)

CHORAL_CENTRAL_CHANNEL_ID = 'UCetUQLixYoAu3iQnXS7H0_Q'

try:
    drive_credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(
        DRIVE_AUTHORIZED_USER_FILE,
        scopes = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file ', 'https://www.googleapis.com/auth/drive.appdata'])
except FileNotFoundError:
    print('Credentials not created')
    pass

try:
    AUTH_DRIVE = build(DRIVE_API_SERVICE_NAME, DRIVE_API_VERSION, credentials=drive_credentials)
except NameError:
    pass

try:
    youtube_credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(
        YOUTUBE_AUTHORIZED_USER_FILE, scopes = ['https://www.googleapis.com/auth/youtube.forcessl'])
except FileNotFoundError:
    print('Credentials not created')
    pass

try:
    AUTH_YOUTUBE = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=youtube_credentials)
except NameError:
    pass

def create_song_folder(folder_name):
    """Return folder id"""

    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'folderColorRgb' : choice(DRIVE_FOLDER_COLORS),
    }
    print(file_metadata)

    folder = AUTH_DRIVE.files().create(
        body=file_metadata,
        fields="id"
        ).execute()
    return folder.get("id")

def upload_pdf_to_drive(score_data, file_location_on_disk):
    file_metadata = score_data
    media = MediaFileUpload(
        file_location_on_disk, mimetype='application/pdf')

    file = AUTH_DRIVE.files().create(
        body=file_metadata,
        media_body=media,
        fields="id,size,webViewLink,webContentLink,thumbnailLink,hasThumbnail"
        ).execute()
    return file

def upload_audio_to_drive(score_data, file_location_on_disk, mimetype):
    file_metadata = score_data
    media_body = MediaFileUpload(
        file_location_on_disk, mimetype=mimetype)

    response = AUTH_DRIVE.files().create(
        body=file_metadata,
        media_body=media_body,
        fields="id,size,webViewLink,webContentLink,thumbnailLink,hasThumbnail"
        ).execute()
    return response

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

# Youtube API

def get_youtube_video_id(video_url):
    """Return a youtube video ID"""
    return video_url.split('v=')[-1].strip()

def get_video_information(video_ids, part='snippet,contentDetails,statistics'):
    """Get information about a single youtube video"""
    response = API_ONLY_YOUTUBE.videos().list(
    part=part, id=video_ids).execute()
    return response

def get_playlist_using_id(playlist_id, part='snippet,status'):
    """Return a playlist id if such a playlist exists. Else return None"""
    response = AUTH_YOUTUBE.playlists().list(part=part, id=playlist_id).execute()
    try:
        return response['items'][0]['id']
    except KeyError:
        return None

def create_playlist(title, part='snippet,status'):
    """Create a new playlist and return its ID"""
    title = title.strip()
    resource = {}
    resource['snippet'] = {'title' : title, 'description' : 'playlist for {}'.format(title)}
    resource['status'] = {'privacyStatus' : 'public'}
    response = AUTH_YOUTUBE.playlists().insert(part=part, body=resource).execute()
    return response['id']

def get_playlist_id(playlist_id, title):
    """Get the id of a playlist, whether it exists or not"""
    if (playlist_id is None) or (playlist_id == ""):
        playlist_id = ""
    try:
        return get_playlist_using_id(playlist_id, part='snippet,status') is None
    except IndexError:
        return create_playlist(title, part='snippet,status')

def add_video_to_playlist(video_id, playlist_id):
    """Add a youtube video to a youtube playlist"""
    resource = {}

    resource['snippet'] = {
        'playlistId': playlist_id,
        'resourceId': {'kind' : 'youtube#video', 'videoId': video_id}
    }
    response = AUTH_YOUTUBE.playlistItems().insert(body=resource,part='snippet').execute()
    return response
