from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from google.oauth2.credentials import Credentials
from django.shortcuts import render, redirect
from requests_oauthlib import OAuth2Session
from .bots import like, comment, subscriber
from .forms import SocialPlatformOrderForm
from django.http import JsonResponse
from .forms import LinkedInPostForm
from django.contrib import messages
from django.conf import settings
from django.views import View
from datetime import datetime
from .facebook_func import *
from .linkedin_func import *
from .bots import automate
import concurrent.futures
from .forms import * 
import requests
import asyncio
import aiohttp
import os
from app.tasks import schedule_facebook_post


def get_credentials(num):
    token_path = os.path.join('all_profiles', f'token{num}.json')
    if os.path.exists(token_path):
        credentials = Credentials.from_authorized_user_file(token_path, scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
        return credentials
    else:
        print(f"File not found: {token_path}")
        return None

def create_youtube_order(request):
    if request.method == 'POST':
        form = SocialPlatformOrderForm(request.POST)
        if form.is_valid():
            social_platform_order = form.save(commit=False)
            social_platform_order.user = request.user
            social_platform_order.social_service = "Youtube"
            social_platform_order.save()
            messages.success(request, 'Social Platform Order created successfully!')
            return redirect('create_youtube_order')
    else:
        form = SocialPlatformOrderForm()

    return render(request, 'create_order.html', {'form': form, 'platform': 'YouTube'})

def create_instagram_order(request):
    if request.method == 'POST':
        form = SocialPlatformOrderForm(request.POST)
        if form.is_valid():
            social_platform_order = form.save(commit=False)
            social_platform_order.user = request.user
            social_platform_order.social_service = "Instagram"
            social_platform_order.save()
            messages.success(request, 'Social Platform Order created successfully!')
            return redirect('create_youtube_order')
    else:
        form = SocialPlatformOrderForm()

    return render(request, 'create_order.html', {'form': form, 'platform': 'Instagram'})

def create_facebook_order(request):
    if request.method == 'POST':
        form = SocialPlatformOrderForm(request.POST)
        if form.is_valid():
            social_platform_order = form.save(commit=False)
            social_platform_order.user = request.user
            social_platform_order.social_service = "Facebook"
            social_platform_order.save()
            messages.success(request, 'Social Platform Order created successfully!')
            return redirect('create_youtube_order')
    else:
        form = SocialPlatformOrderForm()

    return render(request, 'create_order.html', {'form': form, 'platform': 'Facebook'})

def create_linkedIn_order(request):
    if request.method == 'POST':
        form = SocialPlatformOrderForm(request.POST)
        if form.is_valid():
            social_platform_order = form.save(commit=False)
            social_platform_order.user = request.user
            social_platform_order.social_service = "LinkedIn"
            social_platform_order.save()
            messages.success(request, 'Social Platform Order created successfully!')
            return redirect('create_youtube_order')
    else:
        form = SocialPlatformOrderForm()

    return render(request, 'create_order.html', {'form': form, 'platform': 'LinkedIn'})

@login_required
def youtube_auto_post(request):
    if request.method == 'POST':
        form = YouTubeAutomationForm(request.POST, request.FILES)
        if form.is_valid():
            youtube_automate = form.save(commit=False)
            youtube_automate.user = request.user
            youtube_automate.save()

            # Authenticate the user and upload video
            try:
                automate.upload_youtube_video(
                    request,
                    video_file=youtube_automate.video_file.path,
                    title=youtube_automate.title,
                    description=youtube_automate.description,
                    tags=youtube_automate.tags,
                    privacy_status=youtube_automate.privacy_status,
                    publish_date=youtube_automate.publish_date,
                    publish_time=youtube_automate.publish_time,
                )
                messages.success(request, 'YouTube video scheduled successfully!')
            except Exception as e:
                messages.error(request, f'Error uploading YouTube video. {e}')

            return redirect('youtube_automate_order')
        else:
            # Form is not valid, log errors and inform the user
            messages.error(request, 'Invalid form. Please check your inputs.')
            print("Form errors:", form.errors)
            print("Cleaned data:", form.cleaned_data)
    else:
        form = YouTubeAutomationForm()

    return render(request, 'youtube_automate.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class LinkedInPostCreateView(View):
    template_name = 'create_linkedin_post.html'
    form_class = LinkedInPostForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            # Save the file to the server
            # attachment = form.cleaned_data['attachment_url']
            # file_path = handle_uploaded_file(attachment)
            # Save the form data to the database
            post = form.save(commit=False)
            post.user = request.user    
            # post.attachment_url = file_path  # Add a field in your model to store the file path
            post.save()

            # Store the form data in the session to use in callback
            request.session['linkedin_post_data'] = {
                'content': form.cleaned_data['content'],
                'title': form.cleaned_data['title'],
                'hashtags': form.cleaned_data['hashtags'],
                'attachment_path': form.cleaned_data['attachment_url'],
                'publish_time': str(form.cleaned_data['publish_time']),
                'publish_date': str(form.cleaned_data['publish_date']),
            }

            return redirect('linkedin_login')

        return render(request, self.template_name, {'form': form})


def linkedin_callback(request):
    authorization_code = request.GET.get('code')

    if authorization_code:
        access_token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        access_token_params = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
            'client_id': settings.LINKEDIN_CLIENT_ID,
            'client_secret': settings.LINKEDIN_CLIENT_SECRET,
        }

        response = requests.post(access_token_url, data=access_token_params)

        try:
            access_token_data = response.json()
        except ValueError:
            access_token_data = {}

        if 'access_token' in access_token_data:
            linkedin_post_data = request.session.get('linkedin_post_data', {})
            content_to_share = linkedin_post_data.get('content', '')
            title_to_share = linkedin_post_data.get('title', '')
            attachment = linkedin_post_data.get('attachment_path', '')
            publish_date_str = linkedin_post_data.get('publish_date', '')
            publish_time_str = linkedin_post_data.get('publish_time', '')

            current_datetime = datetime.now()

            current_date = current_datetime.date()
            current_time = current_datetime.time()

            if publish_date_str and publish_date_str != 'None':
                publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d').date()
            else:
                publish_date = current_date

            if publish_time_str and publish_time_str != 'None':
                publish_time = datetime.strptime(publish_time_str, '%H:%M:%S').time()
            else:
                publish_time = current_time

            linkedin_automate = LinkedinAutomate(access_token_data['access_token'], attachment, title_to_share, content_to_share, publish_date, publish_time, request)
            if publish_date and publish_time:
                scheduled_datetime = datetime.combine(publish_date, publish_time)
                asyncio.run(linkedin_automate.schedule_post_at_datetime(scheduled_datetime, request))
            else:
                linkedin_automate.post_on_linkedin(request)

            del request.session['linkedin_post_data']
            return redirect("linkedin_post")

        else:
            print("error in token")

    return render(request, 'create_linkedin_post.html')


@login_required
def automate_services(request):
    return render(request, 'auto_services.html')

@login_required
def facebook_login(request):
    redirect_uri = settings.FACEBOOK_REDIRECT_URI
    login_url = f'https://www.facebook.com/v19.0/dialog/oauth?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&scope=public_profile,email'
    return redirect(login_url)


def facebook_callback(request):
    redirect_uri = settings.FACEBOOK_REDIRECT_URI
    code = request.GET.get('code')

    token_url = f'https://graph.facebook.com/v19.0/oauth/access_token?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&client_secret={settings.FACEBOOK_APP_SECRET}&code={code}'
    response = requests.get(token_url)
    data = response.json()

    if 'access_token' in data:
        access_token = data['access_token']
        request.session['facebook_post_data'] = {'token': access_token}
        return fetch_and_render_pages(request, access_token)

    print(f'Error: {data}')
    return redirect('facebook_post_schedule')


def fetch_and_render_pages(request, access_token):
    pages_url = f'https://graph.facebook.com/v19.0/me/accounts?access_token={access_token}'
    pages_response = requests.get(pages_url)
    pages_data = pages_response.json()

    if 'data' in pages_data:
        user_pages = pages_data['data']

        # Assuming you want to save the first page_id in the session
        if user_pages:
            page_id = user_pages[0].get('id')
            request.session['facebook_post_data']['page_id'] = page_id

        return render(request, 'select_page.html', {'pages': user_pages})
    else:
        print(f'Error fetching user pages: {pages_data}')
        return redirect('facebook_post_schedule')


@login_required
def facebook_pages(request):
    redirect_uri = settings.FACEBOOK_REDIRECT_URI
    code = request.GET.get('code')

    token_url = f'https://graph.facebook.com/v19.0/oauth/access_token?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&client_secret={settings.FACEBOOK_APP_SECRET}&code={code}'
    response = requests.get(token_url)
    data = response.json()

    if 'access_token' in data:
        access_token = data['access_token']
        request.session['facebook_post_data']['access_token'] = access_token
        return fetch_and_render_pages(request, access_token)
    print(f'Error: {data}')
    return redirect('facebook_post_schedule')


@method_decorator(login_required, name='dispatch')
class FacebookPostCreateView(View):
    template_name = 'create_facebook_post.html'
    form_class = FacebookPostForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        print("form", form)
        uploaded_file = request.FILES.get('image')
        file_path = handle_fb_uploaded_file(request, uploaded_file) if uploaded_file else None
        print("file", file_path)
        
        if form.is_valid():
            request.session['facebook_post_data']['message'] = form.cleaned_data['message']
            request.session['facebook_post_data']['publish_date'] = form.cleaned_data['publish_date']
            request.session['facebook_post_data']['publish_time'] = form.cleaned_data['publish_time']
            request.session['facebook_post_data']['url'] = form.cleaned_data['link']
            request.session['facebook_post_data']['image'] = file_path
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # Schedule the post
            schedule_facebook_post.apply_async(args=[request.session['facebook_post_data']])

            # return render(request, self.template_name, {'form': form, 'scheduled': True})

            # return redirect("home")

        print("error----", form.errors)
        return render(request, self.template_name, {'form': form})
    

@login_required
def instagram_user_details(request):
    return render(request, 'user_profile.html')


@login_required
def instagram_login(request):
    scope = "instagram_basic,pages_show_list"
    redirect_uri = settings.INSTAGRAM_REDIRECT_URI
    login_url = f"https://www.facebook.com/dialog/oauth?client_id={settings.INSTAGRAM_APP_ID}&display=page&extras=%7B%22setup%22%3A%7B%22channel%22%3A%22IG_API_ONBOARDING%22%7D%7D&redirect_uri={redirect_uri}&response_type=token&scope={scope}"
    return redirect(login_url)


from urllib.parse import urlparse, parse_qs

def instagram_callback(request):
    # Get the current URL
    current_url = request.build_absolute_uri()
    print("---", current_url)
    
    # Parse the URL to extract the fragment
    url_components = urlparse(current_url)
    fragment = url_components.fragment
    print("---", fragment)
    
    # Parse the fragment to get the access token
    fragment_params = parse_qs(fragment)
    print("---", fragment_params)
    access_token = fragment_params.get('access_token')
    print("access_token", access_token)
    
    if access_token:
        # Use access token to fetch user data
        response = requests.get(f'https://graph.facebook.com/v19.0/me/accounts?fields=id,name,access_token,instagram_business_account&access_token={access_token[0]}')
        data = response.json()
        print("data", data)

        # Return the JSON data as a response
        return JsonResponse(data)
    else:
        # Access token not found in the URL
        return JsonResponse({'error': 'Access token not found'}, status=400)











