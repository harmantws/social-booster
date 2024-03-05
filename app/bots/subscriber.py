from googleapiclient.discovery import build


def subscribe_channel(youtube, video_id):
    try:
        channel_id = youtube.videos().list(part='snippet', id=video_id).execute()['items'][0]['snippet']['channelId']
        youtube.subscriptions().insert(part='snippet', body={'snippet': {'resourceId': {'channelId': channel_id}}}).execute()
        print("Subscribed to the channel successfully!")
        return True
    except Exception as e:
        print(f"Error subscribing to the channel: {e}")
        return False

def search_and_interact(credentials, search_query):
    youtube = build('youtube', 'v3', credentials=credentials)
    try:
        video_id = search_query.split("v=")[1]
        print(f"Video ID: {video_id}")
        subscribe_result = subscribe_channel(youtube, video_id)
        if not subscribe_result:
            print("not subscribed the channel!!")
        elif subscribe_result:
            print("Successfully subscribed the channel.")
    except Exception as e:
        print(f"Exception occurred: {e}")
    finally:
        pass

def add_subscribers(credentials, video_url):
    search_and_interact(credentials, video_url)