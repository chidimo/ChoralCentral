"""Youtube API"""

import os

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import pprint

API_KEY = "AIzaSyBMNx5aAONSIqm3NCFrC_YoEoDT98bwKjE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

CLIENT_SECRETS_FILE = "universal/client_secret_native.json"
CHORAL_CENTRAL_CHANNEL_ID = 'UCetUQLixYoAu3iQnXS7H0_Q'

def get_authenticated_service():
    """Get credentials for authenticated API requests"""
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

# AUTH_YOUTUBE = get_authenticated_service()
API_YOUTUBE = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=API_KEY)

def get_youtube_video_id(video_url):
    return video_url.split('watch?v=')[-1].strip()

def get_video_information(youtube, video_ids, part='snippet,contentDetails,statistics'):
    response = API_YOUTUBE.videos().list(
    part=part, id=video_ids).execute()
    return response

def get_playlist_by_id(youtube, playlist_id, part='snippet,status'):    
    response = AUTH_YOUTUBE.playlists().list(part=part, id=playlist_id).execute()
    return response

def create_playlist(youtube, title, part='snippet,status'):
    title = title.strip()
    resource = {}
    resource['snippet'] = {'title' : title, 'description' : 'playlist for {}'.format(title)}
    resource['status'] = {'privacyStatus' : 'public'}
    
    response = AUTH_YOUTUBE.playlists().insert(
        part=part, body=resource).execute()
    return response

def get_or_create_playlist(youtube, playlist_id, title):
    response = get_playlist_by_id(AUTH_YOUTUBE, playlist_id, part='snippet,status')
    if response['items'] == []:
        response = create_playlist(AUTH_YOUTUBE, title, part='snippet,status')
    return response

def get_playlist_id(youtube, playlist_id, title):
    try:
        return get_playlist_by_id(AUTH_YOUTUBE, playlist_id, part='snippet,status')['items'][0]['id']
    except IndexError:
        return create_playlist(AUTH_YOUTUBE, title, part='snippet,status')['id']
