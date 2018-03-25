import os
import json
from django.shortcuts import render, redirect, reverse
from django.conf import settings

import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

CLIENT_SECRETS_FILE = "universal/client.json"
CHORAL_CENTRAL_CHANNEL_ID = 'UCetUQLixYoAu3iQnXS7H0_Q'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

API_KEY = "AIzaSyBMNx5aAONSIqm3NCFrC_YoEoDT98bwKjE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
# flow = google_auth_oauthlib.flow.Flow.from_client_config(CLIENT_SECRETS_FILE, SCOPES)

def get_youtube_permissions(request, flow=FLOW):
    
    # flow.redirect_uri = 'http://localhost:8000/'
    redirect_uri = request.build_absolute_uri(reverse('youtube:youtube_callback'))
    flow.redirect_uri = redirect_uri
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        login_hint='choralcentral@gmail.com',
        prompt='consent',
        # state=settings.SECRET_KEY,
        include_granted_scopes='true')
    return redirect(authorization_url)

def youtube_callback(request, flow=FLOW):
    # Disable https checks
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    template = 'youtube_access.html'
    context = {}
    authorization_response = request.get_full_path()

    print("**********", authorization_response)

    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.

    credentials = flow.credentials
    
    user_auth_data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}
    with open('youtube/credentials.json', 'w+') as fh:
        json.dump(user_auth_data, fh)

    return render(request, template, context)

