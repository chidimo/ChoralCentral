import os
import json
import shelve
from django.shortcuts import render, redirect, reverse
from django.conf import settings

import google.oauth2.credentials
import google_auth_oauthlib.flow

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = "youtube/client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
# flow = google_auth_oauthlib.flow.Flow.from_client_config(CLIENT_SECRETS_FILE, SCOPES)

def get_youtube_permissions(request, flow=FLOW):
    redirect_uri = request.build_absolute_uri(reverse('youtube:youtube_callback'))
    flow.redirect_uri = redirect_uri
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        # login_hint='choralcentral@gmail.com',
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
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials

    credentials = flow.credentials
    credentials = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    shelf = shelve.open('youtube/credentials', 'wb')
    shelf['credentials'] = credentials
    shelf.close()

    return render(request, template, context)
