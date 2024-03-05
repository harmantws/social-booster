# import os
# from googleapiclient.discovery import build
# from selenium import webdriver
# import time
# import streamlit as st
# from .like import like_video
# from .comment import add_comment, check_video_settings
# from .subscriber import subscribe_channel


# def track_watch_time(video_duration):
#     print("video duration------", video_duration)
#     # Simulate watching the entire video
#     time.sleep(video_duration)
#     st.success("Watch time tracked successfully!")

# def get_video_duration(browser):
#     try:
#         # Find the video duration element
#         duration_element = browser.find_element(By.CLASS_NAME, 'ytp-time-duration')
#         # Extract the duration in seconds
#         duration_text = duration_element.text.split(':')
#         minutes = int(duration_text[0])
#         seconds = int(duration_text[1])
#         return minutes * 60 + seconds
#     except Exception as e:
#         st.warning(f"Error retrieving video duration: {e}")
#         return 0

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# credentials_path = 'C:/Users/Md. Saqulain/Downloads/secret.json'
credentials_path = 'C:/Users/Md. Saqulain/Downloads/secret.json'


def get_credentials():
    token_path = 'token.json'
    if os.path.exists(token_path):
        credentials = Credentials.from_authorized_user_file(token_path, scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
        credentials = flow.run_local_server(port=0)

        # Save the credentials to a file
        with open(token_path, 'w') as token_file:
            token_file.write(credentials.to_json())

    return credentials

try:
    credentials = get_credentials()
except FileNotFoundError as e:
    print("error=-----", e)


# from google_auth_oauthlib.flow import InstalledAppFlow

# credentials_content = {
#     "installed": {
#         "client_id": "501507667423-14ok8tka1bdkfrjneeg0rkihvbjbt7pr.apps.googleusercontent.com",
#         "project_id": "youtube-bot-405718",
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://oauth2.googleapis.com/token",
#         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#         "client_secret": "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",
#         "redirect_uris": ["http://localhost"]
#     }
# }

# scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']  # Example scope, modify as needed

# def get_access_token():
#     flow = InstalledAppFlow.from_client_config(credentials_content, scopes=scopes)
#     credentials = flow.run_local_server(port=0)

#     # Print access token and expiration details
#     access_token = credentials.token
#     expires_at = credentials.expiry

#     print("Access Token:", access_token)
#     print("Expires At:", expires_at)

#     return access_token, expires_at

# if __name__ == "__main__":
#     access_token, expiration = get_access_token()

# from google.oauth2.credentials import Credentials

# def search_and_interact(credentials, search_query):
#     # Build the YouTube Data API service with OAuth credentials
#     youtube = build('youtube', 'v3', credentials=credentials)

#     st.info("Performing actions, please wait a minute...")

#     st.text(f"Searching for videos on '{search_query}'...")
#     # browser = webdriver.Chrome(ChromeDriverManager().install())
#     browser = webdriver.Chrome()
#     browser.delete_all_cookies()
    
#     try:
#         browser.get(search_query)
#         time.sleep(2)

#         current_url = browser.current_url
#         print(f"Current URL: {current_url}")
#         time.sleep(2)
        
#         # Extract video ID from the URL
#         video_id = current_url.split("v=")[1]
#         print(f"Video ID: {video_id}")
#         time.sleep(2)

#         # Like the video
#         like_result = like_video(youtube, video_id)
#         if not like_result:
#             print("not Liked the video!!")
#         elif like_result:
#             print("Successfully Liked the video.")
            
#         video_setting = check_video_settings(youtube, video_id)
        
#         if video_setting:
#             print("comment allowed in this video")
#             # Add a comment
#             comment_result = add_comment(youtube, video_id, "This is a great video!")
#             if not comment_result:
#                 print("not comment on video!!")
#             elif comment_result:
#                 print("Successfully comment on video.")
#         else:
#             print("comment not allowed in this video")

#         # Subscribe to the channel
#         subscribe_result = subscribe_channel(youtube, video_id)
#         if not subscribe_result:
#             print("not subscribed the channel!!")
#         elif subscribe_result:
#             print("Successfully subscribed the channel.")

#     except Exception as e:
#         print(f"Exception occurred: {e}")

#     finally:
#         browser.quit()
#         st.success("All actions performed successfully!")






