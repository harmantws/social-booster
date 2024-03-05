from googleapiclient.discovery import build


def write_comment(youtube, video_id, comment_text):
    try:
        comment_response = youtube.commentThreads().insert(
            part='snippet',
            body={
                'snippet': {
                    'videoId': video_id,
                    'topLevelComment': {
                        'snippet': {
                            'textOriginal': comment_text
                        }
                    }
                }
            }
        ).execute()
        print(f"Comment added successfully: {comment_response['snippet']['topLevelComment']['snippet']['textOriginal']}")
        return True
    except Exception as e:
        print(f"Error adding comment: {e}")
        return False
    
def check_video_settings(youtube, video_id):
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
    if video_response['items']:
        video_snippet = video_response['items'][0]['snippet']
        comments_enabled = video_snippet.get('comments', {}).get('allowComments', True)
        print(f"Video Title: {video_snippet['title']}")
        print(f"Comments Enabled: {comments_enabled}")
        return comments_enabled
    else:
        print(f"Video with ID {video_id} not found.")
        return False

def search_and_interact(credentials, search_query):
    youtube = build('youtube', 'v3', credentials=credentials)
    try:
        video_id = search_query.split("v=")[1]
        enabled = check_video_settings(youtube, video_id)
        if enabled:
            comment = write_comment(youtube, video_id, "great video!!")
            if comment:
                print("write comment successfully")
            else:
                print("not commnet on video!")
        else:
            print("comment not enabled on this video!!")
    except Exception as e:
        print(f"Exception occurred during dislike: {e}")
    finally:
        pass
    
def add_comments(credentials, video_url):
    search_and_interact(credentials, video_url)
