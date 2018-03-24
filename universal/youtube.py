"""Youtube API"""

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pprint

API_KEY = "AIzaSyBMNx5aAONSIqm3NCFrC_YoEoDT98bwKjE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_youtube_video_id(video_url):
    return video_url.split('watch?v=')[-1].strip()

def get_video_information(video_ids, part='snippet,contentDetails,statistics'):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=API_KEY)
    response = youtube.videos().list(
    part=part, id=video_ids).execute()
    return response
