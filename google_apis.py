# google_apis.py
import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def create_service(client_secret_data, api_name, api_version, *scopes, prefix=""):
    API_SERVICE_NAME = api_name
    API_VERSION = api_version

    SCOPES = list(scopes[0])

    creds = None
    working_dir = os.getcwd()
    token_dir = "token_files"

    # Include the prefix (email identifier) in the token file name
    token_file = f"token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.json"

    # Check if the token directory exists, create if not
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    # Load existing credentials if available
    if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
        creds = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file), SCOPES)

    # If no valid credentials, initiate the authentication flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(json.loads(client_secret_data), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(os.path.join(working_dir, token_dir, token_file), "w") as token:
            token.write(creds.to_json())

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        print(f"{API_SERVICE_NAME} {API_VERSION} service created successfully for {prefix}")
        return service
    except Exception as e:
        print(e)
        print(f"Failed to create service instance for {API_SERVICE_NAME}")
        # Remove corrupted token file if exists
        if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
            os.remove(os.path.join(working_dir, token_dir, token_file))
        return None
