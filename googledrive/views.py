import os
import json

from django.shortcuts import render, redirect, reverse
import google_auth_oauthlib.flow

DRIVE_SECRETS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/client_secret.json')
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file ', 'https://www.googleapis.com/auth/drive.appdata']

try:
    FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(DRIVE_SECRETS_FILE, SCOPES)
except FileNotFoundError:
    FLOW = ''

def authorize_drive(request, flow=FLOW):
    redirect_uri = request.build_absolute_uri(reverse('googledrive:drive_callback_url'))
    flow.redirect_uri = redirect_uri
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        login_hint='choralcentral@gmail.com',
        prompt='consent',
        # state=settings.SECRET_KEY,
        include_granted_scopes='true')
    return redirect(authorization_url)

def callback(request, flow=FLOW):
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

    save_credentials = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/credentials.json')

    with open(save_credentials, 'w+') as fh:
        json.dump(credentials, fh)

    return render(request, template, context)