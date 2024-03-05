# urls.py

from django.urls import path
from .views import home_page, about, register, CustomLoginView, logout_user
from app.views import *

urlpatterns = [
    # path('', dashboard, name='dashboard'),
    path('about/', about, name='about'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('create_youtube_order/', create_youtube_order, name='create_youtube_order'),
    path('create_instagram_order/', create_instagram_order, name='create_instagram_order'),
    path('create_facebook_order/', create_facebook_order, name='create_facebook_order'),
    path('create_linkedIn_order/', create_linkedIn_order, name='create_linkedIn_order'),
    path('youtube-automate-orders/', youtube_auto_post, name='youtube_automate_order'),
    path('linkedin-login/', linkedin_login, name='linkedin_login'),
    path('linkedin-callback/', linkedin_callback, name='linkedin_callback'),
    path('schedule-linkedin-post/', LinkedInPostCreateView.as_view(), name='linkedin_post'),
    path('schedule-facebook-post/', FacebookPostCreateView.as_view(), name='facebook_post_schedule'),
    path('facebook-login/', facebook_login, name='facebook_login'),
    path('facebook-callback/', facebook_callback, name='facebook_callback'),
    path('facebook-pages/', facebook_pages, name='facebook_pages'),
    path('automate-services/', automate_services, name='auto_services'),
    path('instagram-login/', instagram_login, name='instagram_login'),
    path('instagram-callback/', instagram_callback, name='instagram_callback'),
    path('instagram-detail/', instagram_user_details, name='instagram_detail')

]
