from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from urllib.parse import urlencode
from datetime import datetime
from aiohttp import ClientSession
import json
import os
import requests
import asyncio


def linkedin_login(request):
    
    params = {
        'response_type': 'code',
        'client_id': settings.LINKEDIN_CLIENT_ID,
        'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
        # 'state': '/schedule-linkedin-post/',
        'scope': 'r_liteprofile w_member_social',
    }
    linkedin_auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
    return redirect(linkedin_auth_url)

def save_access_token(user, access_token):
    json_file_path = os.path.join(settings.BASE_DIR, 'linkedin_tokens.json')
    existing_users = set()

    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as existing_file:
            for line in existing_file:
                existing_data = json.loads(line.strip())
                existing_users.add(existing_data.get('user_id'))

    if user.id not in existing_users:
        with open(json_file_path, 'a') as json_file:
            data = {
                'user_id': user.id,
                'access_token': access_token,
            }
            json.dump(data, json_file)
            json_file.write('\n')


def handle_uploaded_file(uploaded_file):
    print("uploaded_file==", uploaded_file)
    file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
    
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return file_path


class LinkedinAutomate:
    def __init__(self, access_token, yt_url, title, description, publish_date, publish_time, request):
        self.access_token = access_token
        self.yt_url = yt_url
        self.title = title
        self.request = request
        self.description = description
        self.publish_date = publish_date
        self.publish_time = publish_time
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

    def post_on_linkedin(self, request, group_id=None):
        url = "https://api.linkedin.com/v2/ugcPosts"
        payload = self._build_post_payload(group_id)

        response = requests.post(url, headers=self.headers, data=payload)

        if response.status_code == 201:
            print("Successfully posted on LinkedIn!")
            messages.success(request, 'Successfully posted on LinkedIn!')
        else:
            print(f"Failed to post on LinkedIn. Status code: {response.status_code}, Response: {response.json()}")
            messages.error(request, 'Failed to post on LinkedIn. Please try again.')

    async def async_post_on_linkedin(self, session, url, payload):
        async with session.post(url, headers=self.headers, data=payload) as response:
            if response.status == 201:
                print("Successfully scheduled post on LinkedIn!")
                messages.success(self.request, 'Successfully scheduled post on LinkedIn!')
            elif response.status == 422:
                # Check if the error is due to a duplicate post
                error_response = await response.json()
                if "errorDetails" in error_response and "inputErrors" in error_response["errorDetails"]:
                    input_errors = error_response["errorDetails"]["inputErrors"]
                    for error in input_errors:
                        if error.get("code") == "DUPLICATE_POST":
                            print("This is a duplicate post!")
                            messages.warning(self.request, 'This is a duplicate post!')
                            return
                # If it's not a duplicate post error, print the general error
                print(f"Failed to schedule post on LinkedIn. Status code: {response.status}, Response: {await response.text()}")
                messages.error(self.request, 'Failed to schedule post on LinkedIn. Please try again.')
            else:
                # If it's not a duplicate post error, print the general error
                print(f"Failed to schedule post on LinkedIn. Status code: {response.status}, Response: {await response.text()}")
                messages.error(self.request, 'Failed to schedule post on LinkedIn. Please try again.')

    async def schedule_post_at_datetime(self, scheduled_datetime, request, group_id=None):
        url = "https://api.linkedin.com/v2/ugcPosts"
        payload = self._build_post_payload(group_id)

        time_difference_seconds = (scheduled_datetime - datetime.now()).total_seconds()

        async with ClientSession() as session:
            # Schedule the post using asyncio.sleep for demonstration purposes
            await asyncio.sleep(time_difference_seconds)

            # Make the asynchronous LinkedIn API request
            await self.async_post_on_linkedin(session, url, payload)

    def _build_post_payload(self, group_id=None):
        payload_dict = {
            "author": f"urn:li:person:{self._get_user_id()}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": self.title
                    },
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {
                                "text": self.description
                            },
                            "originalUrl": self.yt_url,
                            "title": {
                                "text": self.description
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" if not group_id else "CONTAINER"
            }
        }

        if group_id:
            payload_dict["containerEntity"] = f"urn:li:group:{group_id}"

        return json.dumps(payload_dict)

    def _get_user_id(self):
        url = "https://api.linkedin.com/v2/me"
        response = requests.get(url, headers=self.headers)
        jsonData = response.json()
        return jsonData["id"]






