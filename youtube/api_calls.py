"""Youtube API"""

import os

import google.oauth2.credentials

from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

AUTHORIZED_USER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/credentials.json')

try:
    credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(
        AUTHORIZED_USER_FILE, scopes = ['https://www.googleapis.com/auth/youtube.force-ssl'])
except FileNotFoundError:
    print('Credentials not created')
    pass

API_KEY = "AIzaSyBMNx5aAONSIqm3NCFrC_YoEoDT98bwKjE"
CHORAL_CENTRAL_CHANNEL_ID = 'UCetUQLixYoAu3iQnXS7H0_Q'
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

API_ONLY_YOUTUBE = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)
try:
    AUTH_YOUTUBE = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
except NameError:
    pass

# These calls require only an API key
def get_youtube_video_id(video_url):
    """Return a video ID"""
    return video_url.split('v=')[-1].strip()

def get_video_information(youtube, video_ids, part='snippet,contentDetails,statistics'):
    """Get information about a particular video"""
    response = API_ONLY_YOUTUBE.videos().list(
    part=part, id=video_ids).execute()
    return response

# These API calls require user authorization
def get_playlist_by_id(youtube, playlist_id, part='snippet,status'):
    """Get a playlist using its unique ID"""
    response = AUTH_YOUTUBE.playlists().list(part=part, id=playlist_id).execute()
    return response

def create_playlist(youtube, title, part='snippet,status'):
    """Create a new playlist"""
    title = title.strip()
    resource = {}
    resource['snippet'] = {'title' : title, 'description' : 'playlist for {}'.format(title)}
    resource['status'] = {'privacyStatus' : 'public'}

    response = AUTH_YOUTUBE.playlists().insert(
        part=part, body=resource).execute()
    return response

def get_or_create_playlist(youtube, playlist_id, title):
    """Get a playlist if the playlist exists or creates it if not"""
    response = get_playlist_by_id(AUTH_YOUTUBE, playlist_id, part='snippet,status')
    if response['items'] == []:
        response = create_playlist(AUTH_YOUTUBE, title, part='snippet,status')
    return response

def get_playlist_id(youtube, playlist_id, title):
    """Get the id of a playlist, whether it exists or not"""
    if playlist_id is None:
        playlist_id = ''
    try:
        # return an existing playlist id
        return get_playlist_by_id(AUTH_YOUTUBE, playlist_id, part='snippet,status')['items'][0]['id']
    except IndexError:
        # create a new playlist and return its ID
        return create_playlist(AUTH_YOUTUBE, title, part='snippet,status')['id']

def add_video_to_playlist(youtube, video_id, playlist_id):
    """Add a youtube video to a youtube playlist"""
    resource = {}

    resource['snippet'] = {
        'playlistId': playlist_id,
        'resourceId': {'kind' : 'youtube#video', 'videoId': video_id}
    }
    response = youtube.playlistItems().insert(
        body=resource,
        part='snippet',).execute()
    return response
