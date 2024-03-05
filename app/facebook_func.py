import requests, os
import facebook as fb
from django.conf import settings
import uuid

# def facebook_auto_post(session):
#     page_id = session.get("page_id", "")
#     message = session.get("message", "")
#     token = session.get("token", "")
#     print("page_id", page_id)
#     print("token", token)
#     print("message", message)

#     graph = fb.GraphAPI(access_token=token, version='3.0')
#     page_info = graph.get_object(f'/{page_id}?fields=access_token')
#     page_access_token = page_info.get('access_token')

#     # Now use page_access_token for posting
#     post_url = f'https://graph.facebook.com/{page_id}/feed'
#     response = requests.post(post_url, params={'message': "hi hi", 'access_token': page_access_token})

#     if response.status_code == 200:
#         print(response.text)
#         print("Post successfully created!")
#     else:
#         print(response.text)
#         print("Error creating the post.")


import requests
import facebook as fb

def facebook_auto_post(session):
    page_id = session.get("page_id", "")
    message = session.get("message", "")
    token = session.get("token", "")
    publish_date = session.get("publish_date", "")
    publish_time = session.get("publish_time", "")
    # print("image", session.get("url", ""))
    image_url = "https://images.pexels.com/photos/674010/pexels-photo-674010.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    url = session.get("url", "")

    print("page_id", page_id)
    print("token", token)
    print("message", message)
    print("image", image_url)
    print("image", publish_date)
    print("image", publish_time)

    graph = fb.GraphAPI(access_token=token, version='3.0')
    page_info = graph.get_object(f'/{page_id}?fields=access_token')
    page_access_token = page_info.get('access_token')
    
    message_with_url = message + "\n" + url

    # Fetch the image content from the URL
    image_content = requests.get(image_url).content

    # Prepare the files parameter with the image content
    files = {'source': ('image.jpg', image_content)}

    # Include the message in the data parameter
    data = {'message': message_with_url, 'access_token': page_access_token}

    # Now use page_access_token for posting with the image content
    post_url = f'https://graph.facebook.com/{page_id}/photos'
    response = requests.post(post_url, data=data, files=files)

    if response.status_code == 200:
        result = response.json()
        print("Post with image successfully created!")
        print("Post ID:", result.get('id'))
        print("Post URL:", f"https://www.facebook.com/{page_id}_{result.get('id')}")
    else:
        print(response.text)
        print("Error creating the post with image.")


def handle_fb_uploaded_file(request, uploaded_file, media_type='facebook_posts'):
    # Construct the relative URL path using the original file name
    relative_path = os.path.join('media', media_type, uploaded_file.name)

    # Replace backslashes with forward slashes for the absolute URL
    absolute_url = f"{request.scheme}://{request.get_host()}/{relative_path.replace(os.path.sep, '/')}"

    file_path = os.path.join(settings.MEDIA_ROOT, media_type, uploaded_file.name)

    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return absolute_url

