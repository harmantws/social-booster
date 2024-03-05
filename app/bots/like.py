from googleapiclient.discovery import build
  
  
def like_video(youtube, video_id):
    print("Video id", video_id)
    try:
        response = youtube.videos().rate(id=video_id, rating='like').execute()
        print("Video liked successfully!")
        print("API Response:", response)
        print(response)
        return True
    except Exception as e:
        print(f"Error liking video: {e}")
        return False

def search_and_interact(credentials, search_query):
    youtube = build('youtube', 'v3', credentials=credentials)
    
    try:
        video_id = search_query.split("v=")[1]
        like = like_video(youtube, video_id)
        if like:
            print("like video successfully")
        else:
            print("not like the video!")
    except Exception as e:
        print(f"Exception occurred during dislike: {e}")
    finally:
        pass
    
def add_likes(credentials, video_url):
    search_and_interact(credentials, video_url)

