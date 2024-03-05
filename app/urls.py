from django.urls import path
from .views import *

urlpatterns = [
    path('create-youtube-order/', create_youtube_order, name='create_youtube_order'),
    path('create-instagram-order/', create_instagram_order, name='create_instagram_order'),
    path('create-facebook-order/', create_facebook_order, name='create_facebook_order'),
    path('create-linkedIn-order/', create_linkedIn_order, name='create_linkedIn_order'),
    path('linkedin-login/', linkedin_login, name='linkedin_login'),
    path('linkedin-callback/', linkedin_callback, name='linkedin_callback'),
    # path('schedule-linkedin-post/', schedule_linkedin_post, name='linkedin_post'),
    path('schedule-linkedin-post/', LinkedInPostCreateView.as_view(), name='linkedin_post'),
    path('schedule-facebook-post/', FacebookPostCreateView.as_view(), name='facebook_post_schedule'),
    path('facebook-login/', facebook_login, name='facebook_login'),
    path('facebook-callback/', facebook_callback, name='facebook_callback'),
    path('facebook-pages/', facebook_pages, name='facebook_pages'),
    path('automate-services/', automate_services, name='auto_services'),
    path('instagram-login/', instagram_login, name='instagram_login'),
    # path('instagram-callback/', instagram_callback, name='instagram_callback'),
    path('instagram-detail/', instagram_user_details, name='instagram_detail')

]
