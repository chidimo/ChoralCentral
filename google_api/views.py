import os
import json

from django.shortcuts import render, redirect, reverse
import google_auth_oauthlib.flow
# from django.conf import settings
# import google.oauth2.credentials
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

DRIVE_SECRETS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/drive_secret.json')
DRIVE_SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file ',
    'https://www.googleapis.com/auth/drive.appdata',]

YOUTUBE_SECRETS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/youtube_secret.json')
YOUTUBE_SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl']

try:
    DRIVE_FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(DRIVE_SECRETS_FILE, DRIVE_SCOPES)
except FileNotFoundError:
    DRIVE_FLOW = ''

try:
    YOUTUBE_FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(YOUTUBE_SECRETS_FILE, YOUTUBE_SCOPES)
except FileNotFoundError:
    YOUTUBE_FLOW = ''
# flow = google_auth_oauthlib.flow.Flow.from_client_config(YOUTUBE_SECRETS_FILE, SCOPES)

def drive_authorize(request, flow=DRIVE_FLOW):
    redirect_uri = request.build_absolute_uri(reverse('google-api:drive_callback'))
    flow.redirect_uri = redirect_uri
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        login_hint='choralcentral@gmail.com',
        prompt='consent',
        # state=settings.SECRET_KEY,
        include_granted_scopes='true')
    return redirect(authorization_url)

def drive_callback(request, flow=DRIVE_FLOW):
    # Disable https
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    template = 'drive_authorized.html'
    context = {}
    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    # Store the credentials in a json file
    credentials = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    save_credentials = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/drive_credentials.json')
    with open(save_credentials, 'w+') as fh:
        json.dump(credentials, fh)
    return render(request, template, context)

def youtube_authorize(request, flow=YOUTUBE_FLOW):
    redirect_uri = request.build_absolute_uri(reverse('google-api:youtube_callback'))
    flow.redirect_uri = redirect_uri
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        login_hint='choralcentral@gmail.com',
        prompt='consent',
        # state=settings.SECRET_KEY,
        include_granted_scopes='true')
    return redirect(authorization_url)

def youtube_callback(request, flow=YOUTUBE_FLOW):
    # Disable https
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    template = 'youtube_authorized.html'
    context = {}
    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    # Store the credentials in a json file
    credentials = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    save_credentials = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/youtube_credentials.json')
    with open(save_credentials, 'w+') as fh:
        json.dump(credentials, fh)
    return render(request, template, context)
