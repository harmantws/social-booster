from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
import os
from django.contrib import messages
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime
from pytz import timezone
from django.contrib import messages




credentials_path = 'C:/Users/Md. Saqulain/Downloads/secret.json'


def delete_token_file():
    token_file = 'token.json'
    if os.path.exists(token_file):
        os.remove(token_file)
        print("Token file deleted.")
    else:
        print("Token file not found.")

def get_credentials():
    delete_token_file()

    token_path = 'token.json'
    if os.path.exists(token_path):
        credentials = Credentials.from_authorized_user_file(token_path, scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
        credentials = flow.run_local_server(port=0)

        with open(token_path, 'w') as token_file:
            token_file.write(credentials.to_json())

    return credentials

def get_authenticated_service():
    credentials = get_credentials()
    return build("youtube", "v3", credentials=credentials)


def upload_youtube_video(request, video_file, title, description, tags, privacy_status, publish_date, publish_time):
    try:
        youtube = get_authenticated_service()

        # Mapping for privacy status
        privacy_mapping = {
            'public': 'public',
            'private': 'private',
            'unlisted': 'unlisted',
        }
        privacy_status = privacy_mapping.get(privacy_status, 'private')  # Default to private if not found

        # Combine date and time, and ensure it is in the correct ISO format
        publish_datetime = datetime.datetime.combine(publish_date, publish_time)

        # Format the datetime in ISO format
        publish_at_iso = publish_datetime.isoformat() + "Z"

        # Upload video
        upload_body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags.split(','),
            },
            "status": {
                "privacyStatus": privacy_status,
                "publishAt": publish_at_iso
            }
        }

        media = MediaFileUpload(video_file)
        video_response = (
            youtube.videos()
            .insert(
                part="snippet,status",
                body=upload_body,
                media_body=media
            )
            .execute()
        )

        print(f"Video uploaded! Video ID: {video_response['id']}")
        return video_response['id']

    except Exception as e:
        error_message = str(e)
        if 'invalidPublishAt' in error_message:
            messages.error(request, 'Invalid scheduled publishing time. Please choose a valid date and time.')
        else:
            messages.error(request, f'Error uploading video: {error_message}')

        return None



