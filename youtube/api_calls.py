"""Youtube API"""

import os

import google.oauth2.credentials

from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

YOUTUBE_AUTHORIZED_USER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/credentials.json')
API_KEY = 'AIzaSyBMNx5aAONSIqm3NCFrC_YoEoDT98bwKjE'

try:
    credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(
        YOUTUBE_AUTHORIZED_USER_FILE, scopes = ['https://www.googleapis.com/auth/youtube.force-ssl'])
except FileNotFoundError:
    print('Credentials not created')
    pass

CHORAL_CENTRAL_CHANNEL_ID = 'UCetUQLixYoAu3iQnXS7H0_Q'
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# THESE API CALLS ONLY REQUIRE AN API KEY
API_ONLY_YOUTUBE = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

# THESE API CALLS REQUIRE AUTHORIZATION
try:
    AUTH_YOUTUBE = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
except NameError:
    pass

def get_youtube_video_id(video_url):
    """Return a youtube video ID"""
    return video_url.split('v=')[-1].strip()

def get_video_information(youtube, video_ids, part='snippet,contentDetails,statistics'):
    """Get information about a single youtube video"""
    response = API_ONLY_YOUTUBE.videos().list(
    part=part, id=video_ids).execute()
    return response

def get_or_create_playlist(youtube, playlist_id, title, part='snippet,status'):
    """Get a playlist if given playlist_id exists or create new one with the given title"""
    response = AUTH_YOUTUBE.playlists().list(part=part, id=playlist_id).execute()

    if response['items'] == []:
        # create new playlist
        title = title.strip()
        resource = {}
        resource['snippet'] = {'title' : title, 'description' : 'playlist for {}'.format(title)}
        resource['status'] = {'privacyStatus' : 'public'}

        new_playlist_response = AUTH_YOUTUBE.playlists().insert(
            part=part, body=resource).execute()
        response = new_playlist_response
    return response

def get_playlist_id(youtube, playlist_id, title):
    """Return the id of a playlist whether it exists (using playlist_id) or not (user title)"""
    response = get_or_create_playlist(youtube, playlist_id, title, part='snippet,status')
    if playlist_id is None:
        playlist_id = ''
    try:
        return response['items'][0]['id']# return an existing playlist id
    except KeyError:
        return response['id']# create a new playlist and return its ID

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
